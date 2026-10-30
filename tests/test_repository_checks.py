"""Confidentiality and hygiene checks. They run in CI and locally; they never need the survey data.

This repository must contain NO survey data, NO notebook outputs and NO private paths.
"""

import ast
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted((ROOT / "notebooks").glob("*.ipynb"))

APPROVED_IMAGES = {
    "yield_model_comparison_r2.png",
    "yield_model_comparison_rmse.png",
    "yield_model_comparison_mae.png",
    "yield_model_comparison_mae_labelled.png",
    "yield_prediction_error_distribution.png",
    "yield_feature_importance_LEAKAGE_FLAGGED.png",
    "production_v5_correlations_LEAKAGE_EVIDENCE.png",
}
FORBIDDEN_SUFFIXES = {".csv", ".dta", ".xlsx", ".xls", ".sav", ".parquet", ".feather", ".pkl", ".pickle",
                      ".joblib", ".h5", ".html", ".zip", ".sqlite", ".db"}  # fmt: skip


def tracked_files() -> list[Path]:
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return [ROOT / line for line in out.splitlines() if (ROOT / line).is_file()]


def test_there_are_six_notebooks():
    assert len(NOTEBOOKS) == 6


def test_notebooks_have_no_outputs_or_execution_counts():
    for path in NOTEBOOKS:
        nb = json.loads(path.read_text(encoding="utf-8"))
        for cell in nb["cells"]:
            if cell["cell_type"] == "code":
                assert cell.get("outputs") == [], f"{path.name} has stored outputs"
                assert cell.get("execution_count") is None, f"{path.name} has an execution count"


def test_every_notebook_starts_with_the_provenance_banner():
    for path in NOTEBOOKS:
        first = json.loads(path.read_text(encoding="utf-8"))["cells"][0]
        text = "".join(first["source"])
        assert first["cell_type"] == "markdown" and "NOT included" in text, path.name


def test_leaky_notebooks_are_flagged_in_their_banner():
    banners = {p.name: "".join(json.loads(p.read_text(encoding="utf-8"))["cells"][0]["source"]) for p in NOTEBOOKS}
    assert "SUPERSEDED" in banners["05_production_prediction_v5_SUPERSEDED.ipynb"]
    assert "Validity warning" in banners["04_yield_prediction_v4.ipynb"]


def test_all_notebook_code_compiles():
    for path in NOTEBOOKS:
        for cell in json.loads(path.read_text(encoding="utf-8"))["cells"]:
            if cell["cell_type"] != "code":
                continue
            source = "".join(cell["source"])
            source = "\n".join(line for line in source.splitlines() if not line.lstrip().startswith(("%", "!")))
            ast.parse(source)


def readable_text(path: Path) -> str:
    """Notebook JSON is decoded to its cell sources so escaped characters cannot look like paths."""
    if path.suffix == ".ipynb":
        cells = json.loads(path.read_text(encoding="utf-8"))["cells"]
        return "\n".join("".join(c["source"]) for c in cells)
    return path.read_text(encoding="utf-8", errors="ignore")


def test_no_private_absolute_paths_anywhere():
    drive = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/][^\s\"']+")
    home = re.compile(r"/(?:Users|home)/\w+|/content/drive")
    for path in tracked_files():
        if path.suffix in {".png"} or path.name == "test_repository_checks.py":
            continue
        text = readable_text(path)
        assert not drive.search(text), f"drive-letter path in {path.relative_to(ROOT)}"
        assert not home.search(text), f"home path in {path.relative_to(ROOT)}"


def test_no_data_or_model_files_are_tracked():
    bad = [p.name for p in tracked_files() if p.suffix.lower() in FORBIDDEN_SUFFIXES]
    assert bad == []
    data_dir = [p.name for p in tracked_files() if p.parent == ROOT / "data"]
    assert data_dir == ["README.md"]


def test_only_approved_charts_are_published():
    pngs = {p.name for p in tracked_files() if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".svg"}}
    assert pngs == APPROVED_IMAGES


def test_no_credentials_or_personal_contact_patterns():
    secret = re.compile(r"(sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|gh[pous]_[A-Za-z0-9]{30,}|BEGIN [A-Z ]*PRIVATE KEY)")
    email = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}")
    for path in tracked_files():
        if path.suffix == ".png":
            continue
        text = readable_text(path)
        assert not secret.search(text), f"secret-like string in {path.name}"
        assert not email.search(text), f"e-mail address in {path.name}"
