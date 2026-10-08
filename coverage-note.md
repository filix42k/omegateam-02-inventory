# Coverage notes

Run: `pytest tests/ --cov --cov-report=term-missing --cov-fail-under=85`

The coverage configuration measures the three Lab 5 modules: `inventory.py`, `pricing_refactored.py`, and `src/sales.py`. The final local run reported **100% line and branch coverage** for those modules and **56 passed**. It does not claim whole-repository coverage; the older CLI entry point and Lab 3/4 folders are outside this measurement scope.

1. **Which lines never ran, and why is that risky?** None of the lines in the three measured modules were missed in the final run. This only shows that execution visited them; tests can still use weak assertions or miss real user workflows.
2. **Why does 100% coverage not prove test quality?** A test can execute a line without checking the important result. For example, `download_link` has full line coverage, but a new test could still be needed to reject a confirmed URL with an unsafe scheme or unexpected host; the current service returns the configured URL as-is.
3. **Which three tests would be next?** First, reject a digital download URL that is not HTTPS or is outside the configured download host. Second, confirm repeated purchases for the same member and assert that points accumulate correctly across calls. Third, simulate two simultaneous confirmations against the same physical stock and verify that the final stock cannot become negative. These target security, persistent side effects, and concurrency risk rather than adding tests only to increase the percentage.
