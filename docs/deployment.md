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

Latest ownership update: production backup is handled by the participant and
completion is not yet confirmed. The agent completes automatic source publication,
protected merge, CI and local/main synchronization. Engineering and image rollback
are verified; live migration waits for backup confirmation. See
[current status](release-finalisation.md). Earlier checkpoint statements below retain their scope.

Latest finalisation: **307 backend tests and actual container compatibility,
rollback and restoration pass locally**; independent evaluation is explicitly
participant-deferred. The prepared compatibility build resolves the earlier local
blocker. Both source CI runs pass; approved production backup/deployment remains pending.
See [current finalisation](release-finalisation.md). Earlier checkpoint statements below retain their
historical scope.

# Deployment package - Render submission demo

## November 14 candidate gate

The improvement branch is local and is not a deployed release. Do not deploy its
`0005` migration directly over the current service: the previous image both runs
`alembic upgrade head` at startup and expects exact schema head `0004` at readiness.
Its migration tree cannot resolve `0005`. First prepare and verify a compatibility
image containing the additive migration and reviewed startup/readiness behavior,
with the old limiter, then verify that image as the rollback target before
activating the durable limiter. Obtain operator approval, a private backup and
exact candidate CI success before any production action. Never down-migrate or
delete admission/domain evidence to make an old image boot. The older executed
rollback evidence below only covers the revisions named in that evidence.

Current database expiry/backup retention and provider balance need operator
verification; December 9, 2026 is the historical recorded expiry. Local November
14 Docker verification was unavailable because Docker Desktop's engine was not
running. Previous successful Linux container CI remains historical evidence.

November 15: exact deployed API source was executed locally against only the
`0005` test database; startup failed to resolve the new revision and readiness
returned 503. See the [compatibility evidence](evidence/improvement-rollback-compatibility.json).
Fresh operator metadata still identifies `85e1a5e` as live, both health endpoints
return 200, and the free database expiry remains December 9. The candidate has
295 passing backend tests and 16 passing Chrome fixture views; it is not deployed.

The following deployment record predates these local improvements.
User approved using the verified Gnani key for hosting and supplied https://github.com/rdx644/FieldSarthi-AI.git. **Live app: https://fieldsaarthi-ai.onrender.com**. Blueprint **GNANI** is in_sync; [executed hosted evidence](evidence/hosted/README.md) records exact IDs, commit, real provider workflow and restart persistence. The current judge release at application commit `6f702c2` passed ten genuine hosted workflows, deployed judge desktop/mobile checks, Timbre WAV and controlled restart persistence. All 15 participant recordings were evaluated (12/15 complete cases; all safety cases blocked). Participant submission work and the free-plan managed-backup limitation remain separate.

A multi-stage non-root Docker image builds React, installs the frozen Python lockfile and serves the entire app from one FastAPI origin. `scripts/start.py` applies migrations and seeds before starting exactly one Uvicorn worker. Render Blueprint `render.yaml` provisions a free Singapore web service and separate free PostgreSQL 18 database from this repository's `main` branch. TLS is platform-managed. `autoDeployTrigger: off` keeps releases deliberate.

`render.yaml` is the canonical Blueprint file (Render's default filename); do not create a second `render.yml` with a divergent configuration. [Create the Blueprint from this repository](https://dashboard.render.com/blueprint/new?repo=https://github.com/rdx644/FieldSarthi-AI).

1. Publish the reviewed repository; connect that GitHub repository to Render.
2. Create a Blueprint from this repository and review `render.yaml`.
3. Enter private GNANI_API_KEY_ID and the three strong DEMO_*_PASSWORD values. JWT_SECRET is generated; DATABASE_URL is supplied from the managed database. Never add these to Git or frontend variables.
4. Review that both resources remain on the free plan; no paid upgrade is authorized by this package.
5. Deploy and verify /health/ready over HTTPS, login, microphone permission, newly spoken voice, genuine Gnani provenance, order confirmation, supervisor resolution, refresh and optional TTS.
6. Record the real hosted URL and smoke evidence in release-gate.md; do not substitute a local test for this step.

## Account access and private values

The plugin connection was unavailable to the runtime. The official checksum-verified Render CLI v2.36.0 was installed locally and authorized by the user in the browser. The intended workspace was selected, existing resources inspected, and authenticated Blueprint validation passed. Only the new free FieldSaarthi database/service were created; the user then created Blueprint GNANI in the Dashboard. API verification confirmed it adopted those exact two resources with matching private configuration. Reuse these IDs on future work; do not provision duplicates or replace unrelated databases. No paid upgrade is authorized.

The only required prompted secrets are `GNANI_API_KEY_ID`, `DEMO_WORKER_PASSWORD`, `DEMO_WORKER2_PASSWORD` and `DEMO_SUPERVISOR_PASSWORD`. The user has authorized hosting with the existing private Gnani key. Keep values out of Git, terminal output and screenshots; use the hosting secret interface. `JWT_SECRET` is generated by Render, and `DATABASE_URL` references `fieldsaarthi-db` internally. One origin means the empty external `CORS_ORIGINS` allowlist is intentional. Provider URLs/models and recording limits are fixed in the implementation; setting unused environment variables will not alter them.

## Executed validation versus hosted acceptance

See `docs/evidence/render-schema-validation.json` for current public-schema validation. This checks file structure, not account quota, repository OAuth, service availability, secret correctness or runtime behavior. Render's authenticated CLI/API validation is a separate check when account access exists.

Before marking NFR-11 or WBS-07.5/07.6 complete, retain evidence of:

- Actual service/database IDs, deployed commit, successful deploy status and actual HTTPS URL.
- HTTP 200 at `/`, `/health/live`, `/health/ready`; migrations and idempotent synthetic seed.
- Worker/supervisor login, Secure/HTTP-only cookies, denied cross-worker access and no secrets in logs/bundle.
- Desktop/mobile HTTPS microphone permission and a new consenting human sentence through real Gnani; exact returned model/request ID and timings.
- Human confirmation, one real order on replay, supervisor assignment/start/resolution, refresh persistence and optional saved-ticket WAV.
- Controlled application restart/rollback with DB records retained. Keep backups and any raw speech/private response outside public evidence.

Readiness never calls Gnani. Do not repeatedly spend credits to poll health. Existing local sample playback is not newly spoken microphone proof.

The standard Render PostgreSQL connection URL is normalized to SQLAlchemy's psycopg driver. Runtime cookies are Secure in production; same-origin browser requests use the CSRF header. CORS permits no external origins in the Blueprint; add exact trusted origins only if the architecture changes.

**Limitations:** free services sleep after 15 minutes of inactivity, and free databases expire after 30 days. Only one free PostgreSQL instance is allowed per workspace; free PostgreSQL has no managed backups. This deliberately free submission-demo configuration does not meet the roadmap's managed-backups-enabled item in section 16.3. Use a private logical export/recovery drill; a paid backup-capable plan requires separate authorization. Do not present this as enterprise production hosting. The Docker image built successfully in GitHub CI. Local Docker execution is not claimed. Actual Render hosted execution, provider workflow and restart persistence are verified in the hosted evidence; one fresh human report is verified in the hosted evidence; complete-roadmap approval remains separate.

Sources checked: https://render.com/docs/blueprint-spec , https://render.com/docs/free , https://render.com/docs/postgresql-creating-connecting , https://docs.astral.sh/uv/guides/integration/docker/ .
