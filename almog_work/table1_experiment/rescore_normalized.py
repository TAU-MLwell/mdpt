"""Read-only: re-score a finished loop's dev predictions with label-normalized matching.

Strict    = the scorer's own matching (reproduced here; checked against scores.json).
Spacing   = strict + labels compared case-insensitively with all whitespace removed
            (so "(n = 20)" == "(n=20)" == "(n= 20)"). Values are unchanged.
Footnote  = Spacing + trailing footnote markers removed from labels: symbols
            (* # dagger, double dagger, section, pilcrow) and one lowercase letter or digit that
            directly follows a closing bracket, e.g. "(IQR)c" -> "(IQR)".
Nothing is sent to the scorer service and no gold path is exposed to any model;
only dev papers from config.json are read. Rules were written down before looking at holdout.
"""
import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from almog_work.validation.score_table_extraction import normalize_text

ROOT = Path(__file__).resolve().parents[1]
GOLD_DIR = ROOT / "data" / "gold_tables"
MARKERS = "*#\u2020\u2021\u00a7\u00b6"


def _spacing(text):
    return re.sub(r"\s+", "", normalize_text(text).lower())


def _footnote(text):
    t = normalize_text(text)
    t = t.rstrip(MARKERS + " ")
    t = re.sub(r"(?<=[\)\]])[a-z0-9]$", "", t)
    return _spacing(t)


LABEL_RULES = {"strict": lambda t: normalize_text(t), "spacing": _spacing, "footnote": _footnote}


def tuples(cells, rule):
    return Counter((rule(c["row_group"]), rule(c["row_label"]), rule(c["column_label"]),
                    normalize_text(c["value"])) for c in cells)


def f1_parts(gold, pred, rule):
    tp = sum((tuples(gold, rule) & tuples(pred, rule)).values())
    return tp, len(gold), len(pred)


def f1(tp, g, p):
    return 2 * tp / (g + p) if g + p else 0.0


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("loop_dir", type=Path)
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("config.json"))
    args = parser.parse_args()
    dev = json.loads(args.config.read_text(encoding="utf-8"))["splits"]["dev"]["papers"]
    gold = {k: json.loads((GOLD_DIR / f"{k}_table_1_gold.json").read_text(encoding="utf-8"))["cells"]
            for k in dev}
    runs = args.loop_dir / "runs"
    versions = sorted(p.name for p in runs.iterdir() if p.is_dir())
    rows, mismatch = [], 0.0
    for version in versions:
        log = {p["key"]: p for p in json.loads((runs / version / "run.json").read_text(encoding="utf-8"))["papers"]}
        report = json.loads((runs / version / "scores.json").read_text(encoding="utf-8"))
        official = {p["paper"]: p["cell_f1"] for p in report["per_paper"]}
        totals = {name: [0, 0, 0] for name in LABEL_RULES}
        for key in dev:
            pred_file = log[key].get("prediction")
            pred = json.loads((runs / version / pred_file).read_text(encoding="utf-8"))["cells"] if pred_file else []
            row = {"version": version, "paper": key}
            for name, rule in LABEL_RULES.items():
                tp, g, p = f1_parts(gold[key], pred, rule)
                row[f"f1_{name}"] = round(f1(tp, g, p), 4)
                for i, v in enumerate((tp, g, p)):
                    totals[name][i] += v
            mismatch = max(mismatch, abs(row["f1_strict"] - official[key]))
            rows.append(row)
        rows.append({"version": version, "paper": "ALL",
                     **{f"f1_{n}": round(f1(*totals[n]), 4) for n in LABEL_RULES}})
    out = args.loop_dir / "analysis"
    out.mkdir(exist_ok=True)
    with open(out / "rescored_normalized.csv", "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["version", "paper", "f1_strict", "f1_spacing", "f1_footnote"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Check: max |my strict F1 - scorer's F1| over all papers/versions = {mismatch:.4f}\n")
    print("Overall dev cell F1 per version (strict / spacing / spacing+footnote)")
    for r in rows:
        if r["paper"] == "ALL":
            print(f"  {r['version']:5} {r['f1_strict']:.3f} / {r['f1_spacing']:.3f} / {r['f1_footnote']:.3f}")
    print("\nPer paper, mean over versions (strict / spacing / spacing+footnote)")
    for key in dev:
        sel = [r for r in rows if r["paper"] == key]
        m = lambda n: sum(r[n] for r in sel) / len(sel)
        print(f"  {key:12} {m('f1_strict'):.2f} / {m('f1_spacing'):.2f} / {m('f1_footnote'):.2f}")
    print(f"\nWritten: {out / 'rescored_normalized.csv'}")


if __name__ == "__main__":
    main()
