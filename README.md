# FieldSaarthi AI
### Multilingual voice reports. Human-verified work. Accountable resolution.

Built for the Gnani AI internship challenge by **Shubham Putitundi and Shambhavi Kumar**, with AI-assisted implementation and testing. [One-page solution pitch](docs/submission/solution-pitch.pdf) | [Technical explanation](docs/submission/project-summary.md) | [Evidence](docs/evidence/release-gate.md).

## What works
- Real Gnani **Prisma v2.5** transcription, with the original transcript and actual returned request/model provenance.
- Browser microphone capture (25-second soft stop) or consenting audio upload; bounded server-side FFmpeg conversion; 30-second provider ceiling.
- Catalog-backed Hindi/English/Tamil alias extraction, evidence phrases, correction and explicit human confirmation. Hindi/Hinglish is the authentic speech baseline; other speech quality is not yet claimed.
- Exactly one durable PostgreSQL work order per intake, transactional idempotency, role/ownership checks, controlled assignment/priority/status changes and optimistic versions.
- Separate worker/supervisor sessions, HTTP-only cookies, CSRF protection, strict headers, private credentials and synthetic demo inventory.
- Real optional **Gnani Timbre** Hindi WAV acknowledgment, independently generated after saving. TTS failure cannot undo an order.
- Immutable database audit/provenance protections, a responsive interface and tested desktop/mobile accessibility.

**Verified locally:** 87 backend tests, strict mypy/Ruff, frontend type/build/lint/format checks, six WCAG axe/browser checks, genuine browser-to-Gnani-to-database supervisor workflow, real Timbre response, and a matching PostgreSQL backup/restore drill. Exact limits and outstanding external release checks are in [the release record](docs/evidence/release-gate.md).

**Hosted app:** [Open FieldSaarthi AI](https://fieldsaarthi-ai.onrender.com). Free Render Docker + PostgreSQL 18 is live under Blueprint GNANI. Genuine hosted Prisma -> order -> supervisor workflow, Timbre WAV and restart persistence are verified with an existing consented recording; [actual deployment evidence](docs/evidence/hosted/README.md). Fresh human speech/15-clip evaluation and the remaining roadmap gaps are open. No public social post or official form submission is claimed.

## Run locally (Windows / Python 3.12+, Node 26, PostgreSQL 18, uv 0.11.1)
```powershell
cd C:\Users\putit\fieldsaarthi-ai\web
npm.cmd ci --ignore-scripts
npm.cmd run build
cd ..\api
uv sync --locked
# Configure private root .env: DATABASE_URL, JWT_SECRET, GNANI_API_KEY_ID.
uv run alembic upgrade head
uv run python -m app.seed
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --no-access-log
```
Open **http://127.0.0.1:8000**. The existing local isolated PostgreSQL cluster uses port **55432**. See [operations](docs/operations.md) for restart instructions. Migrations are required; the app never silently creates tables at startup.

Seed credentials are generated privately in `private/demo-accounts.json`; never publish them. Synthetic accounts: `worker@fieldsaarthi.demo`, `worker2@fieldsaarthi.demo`, `supervisor@fieldsaarthi.demo`. Production requires strong `DEMO_WORKER_PASSWORD`, `DEMO_WORKER2_PASSWORD`, `DEMO_SUPERVISOR_PASSWORD` secret variables before seeding.

For frontend development, use `npm.cmd run dev` in `web` and keep the API at port 8000; Vite proxies API traffic. The production build is served by FastAPI at the same origin, with no frontend API credential.

## Verify
```powershell
cd api
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest -q
uv run pip-audit
uv run python scripts/browser_quality.py
uv run python -m scripts.backup_drill
cd ..\web
npm.cmd run lint
npm.cmd run format:check
npm.cmd run build
npm.cmd audit --audit-level=high
```
Tests require a separate `TEST_DATABASE_URL` ending in `fieldsaarthi_test`. Integration fixtures deliberately recreate **only that test database's public schema**; never point it at real data. Ordinary tests/browser quality checks make no billable provider calls.

Explicit live browser smoke (one paid STT request; consenting prerecorded sample, never claimed as freshly spoken audio):
```powershell
cd api
uv run python scripts/browser_smoke.py --live
```
The live sample and real response text stay in ignored `private/`; sanitized metadata and synthetic-data screenshots go in `docs/evidence/`. Use a new consenting microphone report for the final human demo. Uploaded audio is temporary and deleted after conversion, not stored as an application attachment.

## Deploy and submit
[Render/Docker deployment](docs/deployment.md) | [Architecture](docs/architecture.md) | [RTM](docs/rtm.md) | [Roadmap](docs/roadmap.md) | [Full roadmap audit](docs/evidence/roadmap-audit.md) | [Task status](tasks/todo.md).

The actual final Microsoft form requires a **2-3 minute video** and a project URL containing a pitch no longer than one page. Prepare a separate 60-second social showcase if desired. Include **#GnaniAI** and **#GreatIndianAIInternshipChallenge**, tag the official account and complete the actual form before **10 November 2026, 11:59 PM IST**. Posting alone is not submitting. [Final checklist](docs/submission/final-checklist.md).
