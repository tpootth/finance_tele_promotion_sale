"""Build the static dashboard for GitHub Pages.

Reads the CSV/JSON/MD outputs written by Bank_Model_Storytelling.ipynb into
results_model_and_business/, embeds them as JSON in site/template.html and
writes everything to _site/.

Usage:  python site/build_site.py [--notebook-html path] [--out _site]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results_model_and_business"
MODEL = RES / "model"
BIZ = RES / "business_simulation"
EDA = MODEL / "eda"


def recs(path: Path, **kw) -> list[dict]:
    df = pd.read_csv(path, **kw)
    return json.loads(df.to_json(orient="records"))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "_site"))
    ap.add_argument("--notebook-html", default=None)
    args = ap.parse_args()
    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    (out / "figures").mkdir(parents=True)
    shutil.copytree(ROOT / "site" / "vendor", out / "vendor")

    summary = json.loads(text(BIZ / "summary.json"))
    selection = json.loads(text(RES / "model_selection.json"))

    data = {
        "built_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "summary": summary,
        "selection": selection,
        "test_metrics": recs(MODEL / "test_model_metrics.csv"),
        "val_metrics": recs(MODEL / "validation_model_metrics.csv"),
        "kpi": recs(MODEL / "kpi_20pct_test.csv"),
        "timeline": recs(MODEL / "monthly_timeline.csv"),
        "capacity": recs(MODEL / "test_capacity_comparison.csv"),
        "bands": recs(MODEL / "marginal_score_bands.csv"),
        "importance": recs(MODEL / "validation_importance.csv"),
        "per_call": recs(BIZ / "per_call_conversion.csv"),
        "channel": recs(BIZ / "channel_rates.csv"),
        "age": recs(BIZ / "age_band_rates.csv"),
        "adaptive": recs(BIZ / "adaptive_threshold_policy.csv"),
        "scenarios": recs(BIZ / "scenario_assumptions.csv"),
        "sensitivity": recs(BIZ / "scenario_sensitivity.csv"),
        "ab": recs(BIZ / "ab_test_sample_size.csv"),
        "stp": recs(BIZ / "stp_segment_table.csv"),
        "job": recs(EDA / "job_rates.csv"),
        "md": {
            "executive": text(RES / "executive_summary.md"),
            "insights": text(BIZ / "part3_insights.md"),
            "stp": text(BIZ / "stp_4ps.md"),
            "story": text(RES / "story_results.md"),
        },
    }

    # copy every figure the notebook produced, grouped for the gallery
    gallery = []
    for group, folder in [("Model", MODEL), ("EDA", EDA), ("Business", BIZ)]:
        for png in sorted(folder.glob("*.png")):
            dest = f"figures/{group.lower()}_{png.name}"
            shutil.copy2(png, out / dest)
            gallery.append({"group": group, "src": dest, "name": png.stem})
    data["gallery"] = gallery

    has_nb = False
    if args.notebook_html and Path(args.notebook_html).exists():
        shutil.copy2(args.notebook_html, out / "notebook.html")
        has_nb = True
    data["has_notebook"] = has_nb

    # downloadable results
    shutil.make_archive(str(out / "results"), "zip", RES)

    tpl = (ROOT / "site" / "template.html").read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    (out / "index.html").write_text(tpl.replace("__DATA__", payload), encoding="utf-8")
    (out / ".nojekyll").write_text("")
    print(f"Site written to {out} ({len(gallery)} figures, notebook={has_nb})")


if __name__ == "__main__":
    main()
