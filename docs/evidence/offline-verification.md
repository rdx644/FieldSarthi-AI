# WBS-00/01 offline verification
Date: 2026-11-08. Environment: Windows, Python 3.12.10, uv 0.11.1. Dependencies locked in api/uv.lock; isolated api/.venv created with uv sync --locked.

Actual final checks from api/:
- uv run pytest -q --tb=short: **41 passed in 1.19s**, no skips.
- uv run ruff check .: **All checks passed**.
- uv run ruff format --check .: **7 files already formatted**.
- uv run mypy app: **Success, 4 source files**.
- CLI --help: smoke and manual recorder both execute without microphone/API access.
- git check-ignore: .env and private/sample_hi.wav ignored.
- Original roadmap SHA256 equals the Downloads source.

TDD evidence: initial contract collection failed because gnani.py did not exist; 24 tests passed after implementation. Added regression for default cURL config showed --silent rather than --disable; fix disables implicit .curlrc. Numeric success=1 regression failed before strict boolean validator, passed after it. Windows test filename overflows were resolved with explicit readable parameter IDs. Project-root regression protects correct private .env resolution. Unicode Hindi fixtures are stored as actual UTF-8.

Scope: contract fixtures, strict WAV validation, cURL invocation safety, retry bounds, malformed/oversized responses, no-speech, auth/quota/rate-limit/provider timeout/errors. These checks do not prove actual API access or recognition quality. Microphone recording, genuine provider calls, deployed smoke and remote GitHub CI/protection have **not run**.

Review (code-review-and-quality skill): correctness checked against WBS-01 contract; real adapter has no fixture success path; public evidence excludes transcript/key; fixed endpoint and no redirects; request concurrency/retries/time/response bounded. No frontend/database/workflow feature is claimed. Production audio conversion, dependency vulnerability audit and full-system security/E2E remain future gates. CMMI certification is not claimed.
