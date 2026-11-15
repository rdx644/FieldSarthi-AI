Current hosted completion - 2026-11-15: **migration, rollback and restoration
verified on Render**, application `241a063`. All 14 saved report details, audit
histories and original provider facts match the private pre-deploy baseline.
The sole approved judge report remains OPEN/version 1 with its original transcript,
provider provenance and one audit event. Hosted queue summaries reconcile with
saved data; six actual Chrome judge views pass accessibility/layout/keyboard
checks. No new Gnani calls or report mutations were made.

The participant confirmed a current restore-ready backup, then the service passed
compatibility stage at 0004 -> candidate at 0005 -> compatibility rollback at 0005
-> candidate restoration at 0005. Live speech was subsequently restored following
the participant's explicit current-balance confirmation. Automatic deployment
remains off. Direct SQL/SSH was unavailable; schema proof uses the exact deployed
source's database-backed readiness checks. Backup retention and the December 9
free-database expiry remain participant-owned. Independent audio evaluation is
still explicitly deferred; no 95/100 result is claimed.

See [current hosted evidence](evidence/improvement-hosted-release.json). Earlier checkpoints below retain their
historical scope and are superseded where they describe deployment/backup gates.

Current source completion - 2026-11-15: **specification engineering complete
and merged through protected PR #18**. Exact candidate and merged-application
main CI pass with 328 backend tests, 18 Chromium fixture accessibility/layout
views, dependency/static/build checks and the actual four-phase container
activation/rollback/restoration rehearsal. Read
[the source completion record](evidence/improvement-source-finalisation.json) for exact commits and CI links.

The accompanying maintenance change records the compatibility branch history
without changing any application file; its original deployable tip is preserved.
All future main updates continue through required CI and branch protection.
Production remains at `85e1a5e` with auto-deploy off, pending owner confirmation
of a current restore-ready backup and the staged release approval. Independent
held-out evaluation remains explicitly participant-deferred; no 95/100 result
is claimed. The earlier checkpoints below are historical and superseded for
source publication and local compatibility status.

Latest continuation ? 2026-11-15: **328 backend tests and 18 Chrome fixture
views pass; not deployed.** Follow-ups fix scarce-connection STT admission,
queue filter failure/retry, replay input protection, nested archive exclusions
and timeout cleanup. Strict checks and dependency audits pass. Fresh hosted
read-only checks preserve the sole approved sample, original transcript hash,
OPEN/version-1 state and one audit event. The hosted app remains `85e1a5e`.
See [current follow-up verification](evidence/improvement-continuation-verification.json). Exact follow-up CI and protected
source merge are next; production remains gated on owner backup confirmation.
Earlier checkpoint records below retain their historical scope.

Latest ownership update: production backup is handled by the participant and
completion is not yet confirmed. The agent completes automatic source publication,
protected merge, CI and local/main synchronization. Engineering and image rollback
are verified; live migration waits for backup confirmation. See
[current status](release-finalisation.md). Earlier checkpoint statements below retain their scope.

# Latest finalisation checkpoint

**307 backend tests and the real four-phase container rollback pass locally.**
The compatibility blocker is resolved for the prepared build; independent audio
evaluation is explicitly deferred by participant decision. Both source CI runs pass; production approval/backup/deployment remains pending. Read
[the current release finalisation](release-finalisation.md) and
[release evidence](evidence/improvement-finalisation-release.json).
The earlier checkpoint below is preserved as history and is superseded where it
calls the local compatibility build unavailable or reports 295 tests.

# Latest improvement verification — 2026-11-15

**LOCAL VERIFIED — NOT DEPLOYED.** Application/test source `84366153682af65f96874dc717e4aa6febed10be`,
branch `feature/95-improvements`: 295 backend tests, strict static/frontend gates,
clean dependency audits and 16 Chrome fixture accessibility/layout views pass.
Read the [complete handoff](improvement-handoff.md),
[34-ID plan](../tasks/improvements.md) and
[release manifest](evidence/improvement-release.json) for the current status.

Live application remains `85e1a5e` (fresh operator API/read-only verification).
Both health endpoints returned 200; only the approved report is visible and its
original transcript hash matches. Render reports December 9 expiry; backup
retention and real provider balance remain operator-owned. Direct production SQL
head verification was unavailable; readiness implies the prior exact `0004` head.
No live provider call, recording, production mutation, deployment or submission.

Offline replay retains 12/15 complete cases, 6/6 safe blocks and 3/3 correction
recovery. Genuine WER/CER and independent held-out evaluation remain unavailable.
Exact old deployed API source at local schema `0005` fails startup/readiness;
compatible rollback image, exact candidate CI/container, approved backup and
production release remain blocked. No 95/100 outcome is claimed.

The following November 14 and earlier records preserve their original scope.

# Current local improvement candidate — 2026-11-14

The Downloads improvement specification is implemented locally on
`feature/95-improvements`, based on `0fca9716e3589eb9cac70f12e2468aacf7cadb5a`.
Read [the improvement log](../tasks/improvements.md) and
[release manifest](evidence/improvement-release.json) before further work.
The unchanged baseline passed 199 tests in a detached local worktree; the
candidate passed 293 tests against isolated `fieldsaarthi_test`, with no live
speech calls. New browser artifacts are synthetic fixtures, separate from older
hosted/genuine evidence. No code was pushed, deployed or merged into main.

Implemented: tracked-source ZIP guard, active reviewer/deadline documentation,
typed SQL role-scoped queue summary across all pages, judge example shortcut,
explicit review/language guidance, standalone offline WER/CER scorer, cached
parser replay, durable speech-operation ledger and synchronized login limiter.
`rules-v4` is retained: cached replay still yields 12/15 complete cases and six
safe blocks, without regressions. Independent held-out results and genuine
WER/CER remain unavailable because verified human reference transcripts are
missing. Do not call this a verified 95/100 result.

Local schema head is `0005`; the deployed schema/revision were not directly
verified through operator credentials. Public health/ready returned 200 after
initial cold-start timeouts; neither endpoint reports a SHA/schema head.
Public baseline GitHub CI for `0fca971` passed. Candidate CI remains pending.
The previous image cannot start or pass readiness on `0005`; production rollout
is held pending a verified staged compatibility image, approved private backup
and exact candidate CI. Never downgrade a live database to make an old app boot.
Provider operation counts survive restarts locally; they are not credit balances.
Login counts remain process-local and deployment remains one worker/replica.

Participant credentials, report visibility, original audio/transcripts and
historical release tags/evidence are preserved. No new recordings, paid
provider calls, production writes, account rotations or public submissions.
Backup/expiry and current balance remain operator-owned. The December 9 expiry
below is historical; recheck through the operator before any release.

## Historical November 10 operational completion

Latest operational completion: the identified engineering gaps are closed for the agreed temporary-demo scope. Actual hosted rollback/restore preserves all existing reports; console credit observation and tested STT/TTS pause cover credit operations; an immutable engineering tag records release signoff. See [release proof](evidence/demo-operational-release.json). Backups/DB expiry and participant/submission work belong to the user. 199 backend tests, strict backend/frontend checks and exact-application CI passed. No new recordings or paid provider requests were needed.

# FieldSaarthi AI — project context for future changes

Engineering review: 2026-11-10. Baseline main: `562d4c0`; this report ships with the correction-recovery audit. Use Git to identify the eventual merge commit. Repository: https://github.com/rdx644/FieldSarthi-AI. Hosted app: https://fieldsaarthi-ai.onrender.com; **Open judge demo** requires no password.

## Scope and measured outcome

The Downloads `FieldSaarthi_AI_Traceable_Implementation_Roadmap.md` was checked against all 24 sections, 94 numbered headings and 64 WBS tasks. Its SHA256 is `c099f20863d923e045440542de63400f729069350821b40b5448c040ed20cd97`, identical to the ignored private reference. See the [section report](evidence/end-to-end-roadmap-audit.md) and [individual heading/WBS dispositions](evidence/end-to-end-roadmap-audit.json). All IDs are accounted for; strict production/release exceptions below remain open.

The user owns individual eligibility/contributions, video, public post and official form. Do not invent contribution statements or publish/submit on their behalf. Tamil is excluded from acceptance by the user's November 10 clarification. Retained Tamil text aliases and locale selection do not establish Tamil speech quality. Actual evaluated coverage is Hindi/English/Hinglish; all 15 recordings already exist and no further recording is requested.

The original genuine Prisma v2.5 development evaluation remains **12/15 automatic complete cases**, meeting the roadmap target of at least 12/15; all six required unsafe/incomplete cases blocked correctly. Same-corpus parser refinement, English substitutions for 04/10 and absence of a held-out/WER/CER benchmark remain disclosed. NLP-04, NLP-12 and NLP-14 pass **3/3 explicit correction replays** using their cached transcripts and known ground truth in the isolated test database. This is application recovery proof, not 15/15 automatic ASR or a new human/hosted evaluation. No provider requests or hosted writes were made for that recovery check.

## Product and authority

A worker records or uploads a short report; the backend normalizes media and requests genuine Gnani STT. The app maps returned words to synthetic inventory and presents evidence and unresolved fields. The worker checks/corrects the transcript and structured details, explicitly confirms, and creates one durable work order. A supervisor assigns, reprioritizes, starts and resolves it. Optional Timbre acknowledgment runs only for an already saved order. A distinct manual-text path never claims speech-provider provenance.

Editing the corrected transcript stores a separate value; it does **not** automatically re-extract or update location, equipment, issue, urgency or description. The review UI now explains this. Those structured controls must be checked explicitly. Raw transcript/provider model/request ID and original extraction stay intact. Confirmed intakes and audit records are protected by database triggers.

PostgreSQL owns business state. Creation commits intake confirmation, work order, CREATED event and idempotency record together. Advisory/row locks and a unique intake relationship protect concurrent retries. The same key/body returns the same order; changed bodies conflict. Supervisor mutations require current role, valid transition and expected version. No browser-local state is authoritative.

## Code and change map

| Concern | Primary files | Verification |
|---|---|---|
| Browser navigation and API | `web/src/App.tsx`, `web/src/lib/api.ts`, `web/src/lib/navigation.ts` | TypeScript/Vite and browser workflow |
| Recording, upload, manual intake | `web/src/pages/Report.tsx`, `ManualReport.tsx` | Permission/lifecycle/WebM/browser and intake tests |
| Correction and confirmation | `web/src/pages/Review.tsx`, `api/app/schemas/commands.py`, `api/app/services/orders.py` | `api/tests/integration/test_asr_correction_recovery.py`, workflow/provenance tests |
| Supervisor queue/detail | `web/src/pages/Orders.tsx`, `Detail.tsx`, `api/app/routers/orders.py` | RBAC/filter/version/transition/browser tests |
| Genuine STT and TTS | `api/app/integrations/gnani.py`, `tts.py`, `api/app/routers/intakes.py` | Contract tests and existing genuine evidence |
| Safe media decoding | `api/app/services/audio.py`, `api/app/core/limits.py` | Actual decoder/media-limit tests |
| Catalog extraction | `api/app/services/extraction.py`, `api/app/seed.py` | Unicode spans, ambiguity, Hindi variants and roadmap tests |
| Models, transactions and schema | `api/app/db/models.py`, `api/app/services/orders.py`, `api/alembic/versions` | Real PostgreSQL integration/race/rollback/immutability tests |
| Security and telemetry | `api/app/core`, `api/app/routers/auth.py` | Role/ownership/CSRF/JWT/log/readiness tests |
| Public judge access | `api/app/routers/auth.py`, `api/app/routers/orders.py`, judge migration/seed | Allowlist, session revocation and judge browser tests |
| Build and deployment | `.github/workflows/ci.yml`, `Dockerfile`, `render.yaml` | Required quality gate, Docker build and runtime evidence |

React/Vite/TypeScript is served by FastAPI from one origin. SQLAlchemy/Pydantic provide typed persistence/contracts. PostgreSQL 18 schema head is migration 0004. The seven domain tables are users, locations, assets, intakes, work orders, audit events and idempotency records. Use actual model/table names when writing SQL. Runtime migrations precede serving; readiness checks exact migration head.

Graph exports are private local reference material. `graphify-out/` is ignored by Git and excluded from Docker; fresh clones do not require it. Use the tracked source, architecture/ADRs, RTM and this report for public project context. Private refreshes must use tracked-file inputs and exclude credentials, raw audio and private/untracked material. The exports were removed from the current tracked tree; older commits and branches retain their historical copies.

## Verification and evidence boundaries

This review executed 193 backend tests (44.59 seconds), Ruff lint/format, mypy over 22 application files, frontend build/lint/Prettier and the existing full browser/accessibility regression. The three private cached-transcript correction replays passed in 4.87 seconds. The browser regression uses one explicit test speech result and a real isolated test DB; it makes zero live provider calls. [Recovery evidence](evidence/asr-correction-recovery.json) describes its exact scope.

Existing genuine evidence remains separate: [15-recording evaluation](evidence/audio-evaluation.json), [ten hosted voice-to-resolved workflows](evidence/hosted/reliability.json), [Timbre WAV verification](evidence/hosted/judge-release-tts.json), [restart persistence](evidence/hosted/judge-release-restart.json), [snapshot restore](evidence/hosted/release-backup-restore.json) and [migration rehearsal](evidence/hosted/snapshot-upgrade.json). Ten hosted workflows reused one consenting clip: reliability evidence, not ten distinct accuracy samples. A fresh participant Hindi microphone report was separately verified. Do not repeat paid calls/restarts merely for reassurance.

Local checks from `api/`: `.venv/Scripts/python.exe -m pytest -q`, `-m ruff check .`, `-m ruff format --check .`, `-m mypy app`. CI uses `uv sync --locked` and corresponding `uv run` commands on Linux. Frontend from `web/`: `npm run build`, `npm run lint`, `npm run format:check`. Browser from `api/`: `.venv/Scripts/python.exe tests/browser/workflow_check.py --channel chrome` (CI uses installed Chromium). Browser and integration tests reset **only** `fieldsaarthi_test`; run them sequentially.

For optional cached recovery, set `FIELD_SAARTHI_REPLAY_RESULTS` to the ignored `private/evaluation/results` directory and run the correction test file. It reads cached transcripts only inside tests and emits sanitized results under `private/asr-recovery/`. Credentials and original recordings/results stay ignored. Local PostgreSQL must use the documented port **55432**, not its default 5432. Never print `.env`, private account files or credential helper output.

Historical availability at the earlier audit: the first free HTTP attempt timed out, then readiness returned 200 at application `6f702c2`. The subsequent [operational release drill](evidence/demo-operational-release.json) deployed `85e1a5e`, rolled back and restored it successfully; this is the current live application. No paid workflow was repeated.

## Security, privacy and operational limits

Gnani credentials remain server-side. Audio has request-size/decoded-duration/subprocess/resource limits and temporary cleanup. Argon2, signed sessions, Secure/HTTP-only/SameSite cookies in production, CSRF checks, current-role checks and per-worker ownership apply. Judge access is read-only and exposes only explicitly approved reports; this review does not change the approved WO-AFF1E3EE3BD2. React escapes transcript content. Logs record request IDs/stage timings without audio/transcript bodies. CI scans reachable history/index for known credential signatures and forbidden private/media paths. These checks are not a universal secret scanner or full penetration test.

The exact Downloads roadmap includes a production checklist requiring enabled backups. Free Render PostgreSQL has **no managed backups** and expires **2026-12-09**. Private logical dumps/restores exist but do not satisfy continuous managed backup requirements. Backups and expiry are now explicitly user-managed for this temporary demo. No paid plan or upgrade is authorized. A controlled restart and isolated snapshot restore were verified; an actual compatible app rollback and restoration are now verified, with all persisted report-detail hashes and approved judge access unchanged. Keep this distinction when assessing WBS-07.7 and production readiness.

Provider limits are per-process/in-memory and reset at restart; the service uses one worker/replica and a shared STT/TTS semaphore. The user supplied a current authenticated-console balance check, retained privately. `GNANI_REQUESTS_ENABLED=false` now pauses both STT/TTS while saved and manual workflows stay available. Ongoing balance checks remain operational; admission counters are not a monetary cap. Before horizontal scaling, add durable shared budgets/rate limits and production operations appropriate to the intended use.

The immutable candidate `v0.2.0-rc.1` remains historical. Engineering tag `demo-verified-2026-11-10` freezes verified application `85e1a5e20c1f623c0ce664493c8f002e7d5cff10`; technical demo signoff is complete. Contest/publication signoff remains user-owned. Engineering checks do not declare the contest submitted or participant/publication gates complete. Prisma v3, LLM extraction, telephony, streaming, native apps and multi-tenant expansion remain optional/excluded scope.

## Git and future work

At fetched baseline `562d4c0`, all six user-named topic branches and both additional graph-context branches were ancestors of main; no missing commits or duplicate merges were needed. Preserve historical branches and tags. New changes go through the protected PR/required quality workflow; do not weaken protection or force-push main. Record the final merge SHA/CI separately because a document cannot contain its own commit hash.

Read `AGENTS.md`, `tasks/todo.md`, `docs/rtm.md`, this report and current evidence before edits. Inspect actual source/Git state, scope changes by FR/NFR IDs, preserve original provider facts and migrations, test against the isolated DB and update the relevant evidence/ADRs. The roadmap and `docs/submission` were deliberately removed from the public tracked tree; reference them privately without restoring them. Contributions remain the user's decision.
