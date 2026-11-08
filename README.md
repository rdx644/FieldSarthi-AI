# FieldSaarthi AI
Multilingual voice reports to human-reviewed maintenance work orders for the Gnani AI internship challenge.

## Current status
Scope executed: **WBS-00 / WBS-01**. Genuine cURL and backend HTTPX Prisma v2.5 calls both returned HTTP 200 with nonempty Hindi transcripts and actual model/request provenance. See [live evidence](docs/evidence/gnani-stt-live.md). **41 offline tests pass.** WBS-01 local spike is verified with the user-provided verification key. Exact eventual deployed-key proof remains pending deployment. WBS-00 still has participant attestation and GitHub/protected-main setup items open. No frontend, database, dashboard or deployed application is claimed.

## Setup (PowerShell)
Prerequisites: Python 3.11+, uv, Git; cURL for the direct provider test.
```powershell
cd C:\Users\putit\fieldsaarthi-ai\api
uv sync --locked
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
uv run mypy app
```
Exact versions and transitive hashes are in `api/uv.lock`. This slice has no web server; its runnable entry point is the opt-in CLI below.

## Private setup and live proof
1. Confirm registration/eligibility/team and form delivery in `docs/compliance.md`.
2. In the Gnani console, confirm active STT access and actual credits. Put the key in root `.env` as `GNANI_API_KEY_ID=...`. Environment variables take precedence. Never use a frontend `VITE_*` key.
3. To record directly on Windows (manual launch only), from `api` run:
```powershell
uv run python scripts/record_sample.py --record
```
This prompts before using the microphone and saves a 12-second private WAV. Device compatibility is not yet verified; if Windows MCI is unavailable, use the manual export below.

Record your own consenting voice saying: **?Block B second floor ka water pump leak ho raha hai, urgent repair chahiye.?** Keep it under 25 seconds, with no personal information. Save **mono, PCM signed 16-bit, 16000 Hz WAV** as `private/sample_hi.wav`. An editor such as Audacity can export this format. Do not use generated silence, TTS, stock audio or a prepared transcript as proof.
4. If FFmpeg is installed and your recording has another format, convert your actual file:
```powershell
ffmpeg -i ..\private\recording.m4a -ac 1 -ar 16000 -c:a pcm_s16le ..\private\sample_hi.wav
```
5. From `api`, run the two real requests sequentially (each can consume credits):
```powershell
uv run python -m app.integrations.smoke ..\private\sample_hi.wav --live --synthetic-consented --transport curl
uv run python -m app.integrations.smoke ..\private\sample_hi.wav --live --synthetic-consented --transport httpx
```
The cURL runner sends the secret via stdin config, not process arguments or shell history. Neither runner follows redirects. Raw transcripts are saved only to ignored `private/`; sanitized evidence JSON contains provider model/request ID, HTTP status, language, audio metadata and hashes. Share only reviewed evidence. The CLI does not mark G1 passed automatically. Confirm the same credential is used on the eventual deployed backend and re-smoke it there.

No retry occurs in live smoke. The adapter permits at most two configured retries for transient connection/429/502/503/504 failures, serializes calls on a shared instance, caps response size and uses bounded timeouts. Production audio validation/conversion beyond this strict WAV smoke is WBS-03 work; this adapter is not an upload endpoint.

## Project records
- `docs/roadmap.md`: original user roadmap, unchanged
- `docs/compliance.md`: official requirements and personal confirmations
- `docs/scope.md`: frozen product baseline and backlog
- `docs/rtm.md`: complete requirement index and evidence mapping
- `docs/risks.md`: open risks
- `docs/sources/`: retrieved source snapshots, hashes and retrieval limitations
- `tasks/todo.md`: item-level WBS status and blockers
- `docs/evidence/gnani-stt-live.md`: honest live gate record
- `docs/github-setup.md`: repository/protection instructions

Prisma transcribes; catalog extraction and workflow logic will belong to FieldSaarthi. Timbre is optional and unimplemented. No automatic language detection or Prisma v3 capability is claimed.
