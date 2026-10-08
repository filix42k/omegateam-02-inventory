# Lab 5 — TDD, refactoring, and CI/CD

This lab work is in the existing team repository. The original root inventory functions remain available; the Lab 5 `Inventory` class and its tests were added alongside them.

## Deliverables

- `tests/test_inventory.py`: six `low_stock_items` cases plus `sell` edge cases; the history shows the initial failing commit, implementation, and separate refactor.
- `tests/test_sales.py` and `src/sales.py`: physical sales reject overselling and reduce stock once at confirmation; digital sales do not reduce stock, and the download link is unavailable before confirmation.
- `test-gap.md`: AI test-gap review and supplementary edge cases.
- `coverage-note.md`: measured coverage scope and three follow-up test priorities.
- `pricing_legacy.py`: unmodified instructor baseline; `smells.md` records the initial review.
- `tests/test_pricing_legacy.py` and `pricing_refactored.py`: characterization tests and behavior-preserving refactor kept beside the original.
- `pyproject.toml`, `requirements.txt`, `.github/workflows/ci.yml`: Ruff, pytest, and the coverage gate.
- `ethics.md` and `AI_USE_LOG.md`: system-specific ethics answers, team practice, and AI provenance.

## Run locally

```powershell
python -m pip install -r requirements.txt
ruff check .
pytest tests/ --cov --cov-report=term-missing --cov-fail-under=85
```

The current run is 56 passing tests, Ruff clean, and 100% line and branch coverage for the three modules listed in `pyproject.toml`.

## Remaining external evidence

The GitHub Actions workflow is configured, but screenshots of a green and red pull-request check require an actual PR workflow run. No screenshot is included until those states are captured from GitHub; do not present a local test result as a GitHub Actions screenshot. After the PR exists, add the verified screenshots under `screenshots/` and update this note.
