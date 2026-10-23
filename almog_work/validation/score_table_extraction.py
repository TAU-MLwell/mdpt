#!/usr/bin/env python3
"""Score table extraction predictions against gold files.

This script is deterministic and does not call any model.
It is designed to be used as an evaluation tool in an optimization loop, while
only returning aggregate metrics and a limited sample of error examples.

This CLI is operator-side, not a sandbox or an agent-facing filesystem tool.
Use scoring_service.py as the restricted interface for an isolated agent runner.
"""

from __future__ import annotations

import argparse
import json
import random
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


DASH_CHARS = "\u2010\u2011\u2012\u2013\u2014\u2015\u2212"
DASH_PATTERN = re.compile(f"[{DASH_CHARS}]")
SPACE_PATTERN = re.compile(r"\s+")


@dataclass(frozen=True)
class CellKey:
    row_group: str
    row_label: str
    column_label: str


@dataclass(frozen=True)
class CellTuple:
    row_group: str
    row_label: str
    column_label: str
    value: str


@dataclass
class PaperScore:
    paper: str
    gold_cells: int
    pred_cells: int
    tp_exact: int
    fp_exact: int
    fn_exact: int
    key_tp: int
    key_fp: int
    key_fn: int
    value_match_on_key_tp: int
    missing_prediction_file: bool


@dataclass
class ErrorExample:
    paper: str
    error_type: str
    row_group: str
    row_label: str
    column_label: str
    gold_value: Optional[str]
    pred_value: Optional[str]


def normalize_text(text: Optional[str]) -> str:
    """Normalize text for robust but deterministic comparison."""
    if text is None:
        return ""

    t = str(text)
    t = t.replace("\u00a0", " ")  # non-breaking space
    t = t.replace("\u2009", " ")  # thin space
    t = DASH_PATTERN.sub("-", t)
    t = t.replace("≥", ">=")
    t = t.replace("≤", "<=")
    t = t.replace("−", "-")
    t = SPACE_PATTERN.sub(" ", t).strip()

    # Standardize common p-value spacing variants: "< 0.001" vs "<0.001"
    t = re.sub(r"([<>]=?)\s+", r"\1", t)

    return t


def safe_get(cell: dict, key: str) -> str:
    return normalize_text(cell.get(key))


def cell_key(cell: dict) -> CellKey:
    return CellKey(
        row_group=safe_get(cell, "row_group"),
        row_label=safe_get(cell, "row_label"),
        column_label=safe_get(cell, "column_label"),
    )


def cell_tuple(cell: dict) -> CellTuple:
    return CellTuple(
        row_group=safe_get(cell, "row_group"),
        row_label=safe_get(cell, "row_label"),
        column_label=safe_get(cell, "column_label"),
        value=safe_get(cell, "value"),
    )


def precision(tp: int, fp: int) -> float:
    denom = tp + fp
    return (tp / denom) if denom else 0.0


def recall(tp: int, fn: int) -> float:
    denom = tp + fn
    return (tp / denom) if denom else 0.0


def f1(p: float, r: float) -> float:
    denom = p + r
    return (2 * p * r / denom) if denom else 0.0


def load_cells(path: Path) -> List[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "cells" not in data:
        raise ValueError("Table JSON must be an object with a cells list")
    cells = data["cells"]
    if not isinstance(cells, list):
        raise ValueError("Table cells must be a list")
    for index, cell in enumerate(cells):
        if not isinstance(cell, dict):
            raise ValueError(f"Cell {index} must be an object")
        for field in ("row_label", "row_group", "column_label", "value"):
            if field not in cell:
                raise ValueError(f"Cell {index} is missing field {field}")
            if not isinstance(cell[field], str) and not (
                field in ("row_group", "row_label") and cell[field] is None
            ):
                raise ValueError(f"Cell {index} has invalid type for {field}")
        if not normalize_text(cell["column_label"]):
            raise ValueError(f"Cell {index} requires a nonempty column label")
    return cells


def list_gold_files(gold_dir: Path) -> List[Path]:
    return sorted(gold_dir.glob("*_table_1_gold.json"))


def expected_pred_for_gold(gold_path: Path, pred_dir: Path) -> Path:
    return pred_dir / gold_path.name.replace("_gold.json", "_pred.json")


def compare_paper(gold_path: Path, pred_path: Optional[Path]) -> Tuple[PaperScore, List[ErrorExample]]:
    paper = gold_path.name.replace("_table_1_gold.json", "")
    gold_cells = load_cells(gold_path)
    gold_key_map: Dict[CellKey, str] = {cell_key(c): safe_get(c, "value") for c in gold_cells}
    if len(gold_key_map) != len(gold_cells):
        # Do not include reference cell content in validation errors.
        raise ValueError("Gold table contains duplicate normalized cell keys")

    if pred_path is None or not pred_path.exists():
        gold_count = len(gold_cells)
        paper_score = PaperScore(
            paper=paper,
            gold_cells=gold_count,
            pred_cells=0,
            tp_exact=0,
            fp_exact=0,
            fn_exact=gold_count,
            key_tp=0,
            key_fp=0,
            key_fn=gold_count,
            value_match_on_key_tp=0,
            missing_prediction_file=True,
        )
        examples = [
            ErrorExample(
                paper=paper,
                error_type="missing_prediction_file",
                row_group="",
                row_label="",
                column_label="",
                gold_value=None,
                pred_value=None,
            )
        ]
        return paper_score, examples

    pred_cells = load_cells(pred_path)

    # Multiset matching: each gold cell can match at most one prediction.
    gold_tuples = Counter(cell_tuple(c) for c in gold_cells)
    pred_tuples = Counter(cell_tuple(c) for c in pred_cells)
    tp_exact = sum((gold_tuples & pred_tuples).values())
    fp_exact = len(pred_cells) - tp_exact
    fn_exact = len(gold_cells) - tp_exact

    pred_values = defaultdict(list)
    for c in pred_cells:
        pred_values[cell_key(c)].append(safe_get(c, "value"))

    gold_key_set = set(gold_key_map.keys())
    pred_key_set = set(pred_values)

    key_tp_set = gold_key_set & pred_key_set
    key_fp_set = pred_key_set - gold_key_set
    key_fn_set = gold_key_set - pred_key_set

    value_match_on_key_tp = sum(1 for k in key_tp_set if gold_key_map[k] in pred_values[k])

    paper_score = PaperScore(
        paper=paper,
        gold_cells=len(gold_cells),
        pred_cells=len(pred_cells),
        tp_exact=tp_exact,
        fp_exact=fp_exact,
        fn_exact=fn_exact,
        key_tp=len(key_tp_set),
        key_fp=len(pred_cells) - len(key_tp_set),
        key_fn=len(key_fn_set),
        value_match_on_key_tp=value_match_on_key_tp,
        missing_prediction_file=False,
    )

    examples: List[ErrorExample] = []

    # Wrong value examples: key exists in both but value differs.
    for k in sorted(key_tp_set, key=lambda x: (x.row_group, x.row_label, x.column_label)):
        gv = gold_key_map[k]
        for pv in sorted(set(pred_values[k])):
            if gv == pv:
                continue
            examples.append(
                ErrorExample(
                    paper=paper,
                    error_type="wrong_value",
                    row_group=k.row_group,
                    row_label=k.row_label,
                    column_label=k.column_label,
                    gold_value=gv,
                    pred_value=pv,
                )
            )

    # Missing cell examples: present in gold key set, absent in pred key set.
    for k in sorted(key_fn_set, key=lambda x: (x.row_group, x.row_label, x.column_label)):
        examples.append(
            ErrorExample(
                paper=paper,
                error_type="missing_cell",
                row_group=k.row_group,
                row_label=k.row_label,
                column_label=k.column_label,
                gold_value=gold_key_map[k],
                pred_value=None,
            )
        )

    # Extra cell examples: present in pred key set, absent in gold key set.
    for k in sorted(key_fp_set, key=lambda x: (x.row_group, x.row_label, x.column_label)):
        examples.append(
            ErrorExample(
                paper=paper,
                error_type="extra_cell",
                row_group=k.row_group,
                row_label=k.row_label,
                column_label=k.column_label,
                gold_value=None,
                pred_value=sorted(pred_values[k])[0],
            )
        )

    for k in sorted(pred_key_set, key=lambda x: (x.row_group, x.row_label, x.column_label)):
        if len(pred_values[k]) > 1:
            examples.append(ErrorExample(
                paper=paper, error_type="duplicate_cell",
                row_group=k.row_group, row_label=k.row_label,
                column_label=k.column_label, gold_value=None,
                pred_value=sorted(pred_values[k])[0],
            ))

    return paper_score, examples


def sample_errors(errors: Sequence[ErrorExample], max_examples: int, seed: int) -> List[ErrorExample]:
    if max_examples < 0:
        raise ValueError("max_examples must be nonnegative")
    if len(errors) <= max_examples:
        return list(errors)
    rnd = random.Random(seed)
    return rnd.sample(list(errors), max_examples)


def aggregate_scores(scores: Iterable[PaperScore]) -> dict:
    scores = list(scores)
    tp = sum(s.tp_exact for s in scores)
    fp = sum(s.fp_exact for s in scores)
    fn = sum(s.fn_exact for s in scores)

    kp = sum(s.key_tp for s in scores)
    kfp = sum(s.key_fp for s in scores)
    kfn = sum(s.key_fn for s in scores)

    p = precision(tp, fp)
    r = recall(tp, fn)
    f = f1(p, r)

    kp_p = precision(kp, kfp)
    kp_r = recall(kp, kfn)
    kp_f = f1(kp_p, kp_r)

    value_acc = (sum(s.value_match_on_key_tp for s in scores) / kp) if kp else 0.0

    return {
        "papers_scored": len(scores),
        "cells": {
            "tp_exact": tp,
            "fp_exact": fp,
            "fn_exact": fn,
            "precision": round(p, 6),
            "recall": round(r, 6),
            "f1": round(f, 6),
        },
        "keys_only": {
            "tp": kp,
            "fp": kfp,
            "fn": kfn,
            "precision": round(kp_p, 6),
            "recall": round(kp_r, 6),
            "f1": round(kp_f, 6),
            "value_accuracy_on_matched_keys": round(value_acc, 6),
        },
        "missing_prediction_files": [s.paper for s in scores if s.missing_prediction_file],
    }


def build_per_paper(scores: Iterable[PaperScore]) -> List[dict]:
    out = []
    for s in scores:
        p = precision(s.tp_exact, s.fp_exact)
        r = recall(s.tp_exact, s.fn_exact)
        out.append(
            {
                "paper": s.paper,
                "gold_cells": s.gold_cells,
                "pred_cells": s.pred_cells,
                "missing_prediction_file": s.missing_prediction_file,
                "cell_precision": round(p, 6),
                "cell_recall": round(r, 6),
                "cell_f1": round(f1(p, r), 6),
                "key_precision": round(precision(s.key_tp, s.key_fp), 6),
                "key_recall": round(recall(s.key_tp, s.key_fn), 6),
                "value_accuracy_on_matched_keys": round((s.value_match_on_key_tp / s.key_tp) if s.key_tp else 0.0, 6),
            }
        )
    return out


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score table extraction predictions against gold JSON files")
    parser.add_argument(
        "--gold-dir",
        type=Path,
        default=Path("almog_work/data/gold_tables"),
        help="Directory containing *_table_1_gold.json files",
    )
    parser.add_argument(
        "--pred-dir",
        type=Path,
        required=True,
        help="Separate directory containing *_table_1_pred.json files",
    )
    parser.add_argument(
        "--max-error-examples",
        type=int,
        default=5,
        choices=range(0, 11),
        help="Number of sampled errors (0-10); reference values are never printed",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for sampling error examples",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output JSON path (defaults to stdout only)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    gold_dir = args.gold_dir
    pred_dir = args.pred_dir

    gold_root, pred_root = gold_dir.resolve(), pred_dir.resolve()
    if (gold_root == pred_root or gold_root in pred_root.parents
            or pred_root in gold_root.parents):
        raise ValueError("Gold and prediction directories must be separate and non-overlapping")
    if args.output:
        output = args.output.resolve()
        if output == gold_root or gold_root in output.parents:
            raise ValueError("Reports must not be written into the gold directory")

    if not gold_dir.exists():
        raise FileNotFoundError(f"gold dir not found: {gold_dir}")
    if not pred_dir.exists():
        raise FileNotFoundError(f"pred dir not found: {pred_dir}")

    gold_files = list_gold_files(gold_dir)
    if not gold_files:
        raise FileNotFoundError(f"no gold files found in {gold_dir}")

    scores: List[PaperScore] = []
    all_errors: List[ErrorExample] = []

    for g in gold_files:
        p = expected_pred_for_gold(g, pred_dir)
        score, errs = compare_paper(g, p)
        scores.append(score)
        all_errors.extend(errs)

    sampled = sample_errors(all_errors, args.max_error_examples, args.seed)

    result = {
        "summary": aggregate_scores(scores),
        "per_paper": build_per_paper(scores),
        "error_examples": [
            {
                "paper": e.paper,
                "error_type": e.error_type,
                "row_group": e.row_group,
                "row_label": e.row_label,
                "column_label": e.column_label,
                "pred_value": e.pred_value,
            }
            for e in sampled
        ],
    }

    payload = json.dumps(result, indent=2, ensure_ascii=False)
    print(payload)

    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
