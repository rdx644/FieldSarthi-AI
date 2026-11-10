# FieldSaarthi AI

**Judge dashboard is live.** [Open the live app](https://fieldsaarthi-ai.onrender.com)
and select **Open judge demo** to inspect the approved real report and provenance
in read-only mode. No password is required.
[Two-minute evaluation guide](docs/judge-guide.md)
| [Current verification and remaining participant gates](docs/evidence/judge-readiness.md)
| [15-recording instructions](docs/tests/recording-guide.md).

### Multilingual voice reports. Human-verified work. Accountable resolution.

Built for the Gnani AI internship challenge by **Shubham Putitundi and Shambhavi Kumar**, with AI-assisted implementation and testing. [Architecture](docs/architecture.md) | [Verification](docs/evidence/judge-readiness.md) | [Judge walkthrough](docs/judge-guide.md).

## What works
- Real Gnani **Prisma v2.5** transcription, with the original transcript and actual returned request/model provenance.
- Browser microphone capture (25-second soft stop) or consenting audio upload; bounded server-side FFmpeg conversion; 30-second provider ceiling.
- Catalog-backed Hindi/English/Tamil alias extraction, evidence phrases, correction and explicit human confirmation. Authentic speech evaluation covers Hindi/English/Hinglish; Tamil remains unverified.
- Versioned extraction preserves exact original-text evidence spans; conflicting assets stay unresolved. An accessible typed-report path is explicitly labelled MANUAL_TEXT with no speech-provider provenance.
- Exactly one durable PostgreSQL work order per intake, transactional idempotency, role/ownership checks, controlled assignment/priority/status changes and optimistic versions.
- Separate worker/supervisor sessions, HTTP-only cookies, CSRF protection, strict headers, private credentials and synthetic demo inventory.
- Public read-only judge access exposes only explicitly approved demonstration reports. Team accounts retain private recording and supervisor controls; cancellation requires an audited reason.
- Real optional **Gnani Timbre** Hindi WAV acknowledgment, independently generated after saving. TTS failure cannot undo an order.
- Immutable database audit/provenance protections, a responsive interface and tested desktop/mobile accessibility.

**Verified locally:** 190 backend tests, strict mypy/Ruff, frontend type/build/lint/format checks, six retained accessibility views plus ten full-workflow browser checks, and matching local/hosted-snapshot PostgreSQL restore drills. The genuine 15-recording development evaluation achieved **12/15 complete cases**, with all six safety cases blocked correctly; [results and limitations](docs/evidence/audio-evaluation.json). Ten consecutive automated workflows also pass with test-only speech responses. See [current verification](docs/evidence/judge-readiness.md) for exact scope and participant gates.

**Hosted app:** [Open FieldSaarthi AI](https://fieldsaarthi-ai.onrender.com). Free Render Docker + PostgreSQL 18 is live under Blueprint GNANI. Ten consecutive genuine Prisma -> confirmed order -> supervisor resolution workflows passed, with separate genuine Timbre WAV verification. A controlled restart preserved all ten resolved orders and the approved OPEN participant report. The public judge dashboard passed deployed desktop/mobile checks; [actual deployment evidence](docs/evidence/hosted/README.md). All 15 participant recordings were evaluated. Final participant contributions, video, public post and official form remain pending.

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

## Deployment and evaluation
[Render/Docker deployment](docs/deployment.md) | [Architecture](docs/architecture.md) | [RTM](docs/rtm.md) | [Full roadmap audit](docs/evidence/roadmap-audit.md) | [Task status](tasks/todo.md).

## Codebase graph
To use the interactive view, download [`graph.html`](graphify-out/graph.html) from GitHub (open the file, choose **Raw**, then save it) and open the downloaded file in a browser. It has a searchable offline fallback if the hosted visualization library is unavailable. [GraphRAG JSON](graphify-out/graph.json) | [Graph report and community index](graphify-out/GRAPH_REPORT.md) | [Coverage audit](graphify-out/coverage.json).
The graph covers every tracked repository file, including its four exported artifacts. On refresh, use `git ls-files` as the Graphify input list because a workspace scan can include ignored local files; exclude private audio, credentials and all untracked files.

The implementation roadmap and submission drafts are excluded from this repository at the team's request. Engineering status and measured verification remain public. Participant contributions, final media and the official form are handled separately by the team.

## Engineering context for future changes

See [complete project context](docs/final-project-context.md) and the [Downloads-roadmap audit](docs/evidence/end-to-end-roadmap-audit.md). The latest scoped review has 199 passing backend tests and 3/3 explicit correction replays; automatic ASR remains 12/15. Tamil is excluded from acceptance by the user. Production/release exceptions remain explicit in the report.

Temporary-demo engineering signoff: [actual hosted rollback/restoration and release proof](docs/evidence/demo-operational-release.json), frozen at tag `demo-verified-2026-11-10`. Credit observation and STT/TTS pause controls are verified; backups/DB expiry are user-managed.
