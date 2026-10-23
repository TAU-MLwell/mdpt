"""Read-only analysis of a finished loop: why do some dev papers score high and others low?

Compares every saved dev prediction (all versions of one loop) with the dev gold tables and
writes summary CSVs to <loop>/analysis/. Only dev papers are used; holdout gold is never read
(the dev paper list comes from config.json and is checked against the loop's own run logs).

Each gold cell is put in exactly one category (first match wins):
  exact           predicted cell equals the gold cell (group, row, column, value)
  value_differs   same group/row/column, different value
  column_label    gold column label never appears among the prediction's column labels
  row_group       same row label exists in the prediction, under a different row group
  row_missing     row label never appears in the prediction
  other           row and column both exist but this cell was not predicted
"""
import argparse
import csv
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from almog_work.validation.score_table_extraction import cell_key, cell_tuple, normalize_text

ROOT = Path(__file__).resolve().parents[1]
GOLD_DIR = ROOT / "data" / "gold_tables"
CATEGORIES = ("exact", "value_differs", "column_label", "row_group", "row_missing", "other")


def classify(gold_cells, pred_cells):
    pred_tuples = {cell_tuple(c) for c in pred_cells}
    pred_keys = {cell_key(c) for c in pred_cells}
    pred_columns = {cell_key(c).column_label for c in pred_cells}
    pred_rows = {(cell_key(c).row_group, cell_key(c).row_label) for c in pred_cells}
    pred_row_labels = {cell_key(c).row_label for c in pred_cells}
    counts = Counter()
    for cell in gold_cells:
        t, k = cell_tuple(cell), cell_key(cell)
        if t in pred_tuples:
            counts["exact"] += 1
        elif k in pred_keys:
            counts["value_differs"] += 1
        elif k.column_label not in pred_columns:
            counts["column_label"] += 1
        elif (k.row_group, k.row_label) not in pred_rows and k.row_label in pred_row_labels:
            counts["row_group"] += 1
        elif k.row_label not in pred_row_labels:
            counts["row_missing"] += 1
        else:
            counts["other"] += 1
    return counts


def _squash(text):
    return re.sub(r"[^a-z0-9]", "", normalize_text(text).lower())


def near_miss(gold_cells, pred_cells):
    """For gold cells whose column or row label is absent from the prediction, say how far off it is.

    formatting_only  same letters/digits, differs only in spaces/punctuation/case
    text_added_or_cut one label contains the other (footnote letter, dropped '(n=..)' or ', n (%)')
    different        no similar predicted label
    """
    pred = {"column_label": {cell_key(c).column_label for c in pred_cells},
            "row_label": {cell_key(c).row_label for c in pred_cells}}
    counts = Counter()
    for cell in gold_cells:
        k = cell_key(cell)
        for field in ("column_label", "row_label"):
            label = getattr(k, field)
            if label in pred[field]:
                continue
            sq = _squash(label)
            others = [_squash(p) for p in pred[field]]
            if sq in others:
                kind = "formatting_only"
            elif sq and any(o and (sq in o or o in sq) for o in others):
                kind = "text_added_or_cut"
            else:
                kind = "different"
            counts[(field, kind)] += 1
    return counts


def paper_features(gold):
    cells = gold["cells"]
    values = [normalize_text(c["value"]) for c in cells]
    rows = {(c["row_group"], c["row_label"]) for c in cells}
    columns = {c["column_label"] for c in cells}
    n = len(cells) or 1
    return {
        "gold_cells": len(cells),
        "gold_rows": len(rows),
        "gold_columns": len(columns),
        "raw_text_chars": len(gold.get("raw_table_text") or ""),
        "pct_row_group_set": round(100 * sum(c["row_group"] is not None for c in cells) / n, 1),
        "pct_values_with_paren": round(100 * sum("(" in v for v in values) / n, 1),
        "pct_values_with_bracket": round(100 * sum("[" in v for v in values) / n, 1),
        "pct_values_plusminus": round(100 * sum("±" in v for v in values) / n, 1),
        "pct_values_numeric_only": round(100 * sum(bool(re.fullmatch(r"[-+<>=.\d,]+", v)) for v in values) / n, 1),
        "pct_columns_with_n": round(100 * sum(bool(re.search(r"n\s*=", c, re.I)) for c in columns) / max(len(columns), 1), 1),
        "pct_columns_nested": round(100 * sum(":" in c for c in columns) / max(len(columns), 1), 1),
        "avg_value_chars": round(sum(len(v) for v in values) / n, 1),
    }


def _ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks, i = [0.0] * len(xs), 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return ranks


def spearman(xs, ys):
    if len(xs) < 3 or len(set(xs)) < 2 or len(set(ys)) < 2:
        return None
    rx, ry = _ranks(xs), _ranks(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else None


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def sd(xs):
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs)) if xs else 0.0


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("loop_dir", type=Path)
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("config.json"))
    args = parser.parse_args()
    dev_papers = json.loads(args.config.read_text(encoding="utf-8"))["splits"]["dev"]["papers"]
    runs_dir = args.loop_dir / "runs"
    versions = sorted(p.name for p in runs_dir.iterdir() if p.is_dir())
    gold = {k: json.loads((GOLD_DIR / f"{k}_table_1_gold.json").read_text(encoding="utf-8"))
            for k in dev_papers}
    features = {k: paper_features(g) for k, g in gold.items()}

    # cell-level categories per (version, paper)
    rows, per_paper_f1 = [], defaultdict(dict)
    for version in versions:
        run = json.loads((runs_dir / version / "run.json").read_text(encoding="utf-8"))
        scores = json.loads((runs_dir / version / "scores.json").read_text(encoding="utf-8"))
        f1 = {p["paper"]: p["cell_f1"] for p in scores["per_paper"]}
        status = {p["key"]: p for p in run["papers"]}
        for key in dev_papers:
            pred_file = status[key].get("prediction")
            pred_cells = []
            if pred_file:
                pred_cells = json.loads((runs_dir / version / pred_file).read_text(encoding="utf-8"))["cells"]
            counts = classify(gold[key]["cells"], pred_cells)
            per_paper_f1[key][version] = f1.get(key, 0.0)
            rows.append({"version": version, "paper": key, "cell_f1": round(f1.get(key, 0.0), 4),
                         "status": status[key].get("status", "ok"),
                         "pred_cells": len(pred_cells), "gold_cells": len(gold[key]["cells"]),
                         "extra_pred_cells": len(pred_cells) - sum(counts[c] for c in ("exact", "value_differs")),
                         **{c: counts[c] for c in CATEGORIES}})
    out = args.loop_dir / "analysis"
    out.mkdir(exist_ok=True)

    def write(name, data):
        with open(out / name, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(data[0]))
            writer.writeheader()
            writer.writerows(data)

    write("cell_categories_by_run.csv", rows)

    # label near-misses over all versions (counts of gold cells whose label is absent)
    near_rows = []
    for key in dev_papers:
        total, n_cells = Counter(), 0
        for version in versions:
            run = json.loads((runs_dir / version / "run.json").read_text(encoding="utf-8"))
            pred_file = {p["key"]: p for p in run["papers"]}[key].get("prediction")
            pred_cells = json.loads((runs_dir / version / pred_file).read_text(encoding="utf-8"))["cells"] if pred_file else []
            total.update(near_miss(gold[key]["cells"], pred_cells))
            n_cells += len(gold[key]["cells"])
        near_rows.append({"paper": key, **{f"{f}:{kind}": round(100 * total[(f, kind)] / n_cells, 1)
                                           for f in ("column_label", "row_label")
                                           for kind in ("formatting_only", "text_added_or_cut", "different")}})
    write("label_near_misses.csv", near_rows)

    # paper-level table: stability and the dominant failure category across all versions
    paper_rows = []
    for key in dev_papers:
        f = list(per_paper_f1[key].values())
        mine = [r for r in rows if r["paper"] == key]
        total_gold = sum(r["gold_cells"] for r in mine)
        shares = {c: round(100 * sum(r[c] for r in mine) / total_gold, 1) for c in CATEGORIES}
        paper_rows.append({"paper": key, "mean_f1": round(mean(f), 3), "sd_f1": round(sd(f), 3),
                           "min_f1": round(min(f), 3), "max_f1": round(max(f), 3),
                           "invalid_runs": sum(r["status"] == "invalid_output" for r in mine),
                           **{f"pct_{c}": shares[c] for c in CATEGORIES}, **features[key]})
    paper_rows.sort(key=lambda r: -r["mean_f1"])
    write("paper_summary.csv", paper_rows)

    # which paper features go with a higher mean F1 (Spearman over the dev papers)
    corr = []
    for name in features[dev_papers[0]]:
        xs = [features[k][name] for k in dev_papers]
        ys = [mean(list(per_paper_f1[k].values())) for k in dev_papers]
        value = spearman(xs, ys)
        corr.append({"feature": name, "spearman_with_mean_f1": None if value is None else round(value, 2)})
    corr.sort(key=lambda r: -abs(r["spearman_with_mean_f1"] or 0))
    write("feature_correlations.csv", corr)

    print(f"Versions analysed: {', '.join(versions)}  (dev papers: {len(dev_papers)})\n")
    print("Per paper (all versions): mean F1 +- sd [min, max]; share of gold cells by outcome (%)")
    for r in paper_rows:
        print(f"  {r['paper']:12} {r['mean_f1']:.2f} +- {r['sd_f1']:.2f} [{r['min_f1']:.2f}, {r['max_f1']:.2f}]  "
              + " ".join(f"{c}={r['pct_' + c]:.0f}" for c in CATEGORIES)
              + f"  invalid_runs={r['invalid_runs']}  gold_cells={r['gold_cells']}")
    print("\nAbsent gold labels as % of gold cells (all versions): formatting_only / text_added_or_cut / different")
    for r in near_rows:
        parts = [f"{f}: " + " / ".join(f"{r[f + ':' + kind]:.0f}" for kind in ("formatting_only", "text_added_or_cut", "different"))
                 for f in ("column_label", "row_label")]
        print(f"  {r['paper']:12} " + "   ".join(parts))
    print("\nFeatures ranked by |Spearman| with mean F1 (n = 6 papers: descriptive only):")
    for r in corr:
        print(f"  {r['feature']:26} {r['spearman_with_mean_f1']}")
    print(f"\nFiles written to {out}")


if __name__ == "__main__":
    main()
