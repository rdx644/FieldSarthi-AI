# Actual Render deployment evidence - 2026-11-09

Application: https://fieldsaarthi-ai.onrender.com

Deployed application commit: `09cb09faf75817f73e2f0cfc71397db266b2346c`. Render deployment `dep-dborm5ec6qcc738i127g` is **live**. Blueprint **GNANI** (`exs-dborlpu417fc7396uk2g`) is **in_sync**, linked to `FieldSarthi-AI/main` and `render.yaml`; its two resources are the intended free Singapore Docker service and PostgreSQL 18 database. Account authorization used the official CLI; the user completed the required Dashboard Blueprint step. Existing unrelated resources were not modified.

## Executed hosted checks

- Root, liveness and database readiness return HTTP 200 over HTTPS. Real startup migrated PostgreSQL and seeded synthetic identities/catalog.
- Existing consenting Hindi recording -> actual Prisma v2.5 -> explicit browser review/confirmation -> persisted work order `WO-59BF37DC1536` -> refresh -> supervisor assignment, in-progress and resolution -> refresh and mobile queue. See runtime-verification.json for actual provider/model/request ID. The recorder was separately exercised with file-fed audio. **This is not freshly spoken human microphone input.**
- Secure/HTTP-only/SameSite=strict cookies; cross-origin cookie mutation 403; other worker order/intake access 404; worker supervisor mutation 403.
- One actual hosted Timbre request returned HTTP 200 audio/wav, 5.76seconds mono 48 kHz PCM, hash recorded. Requested timbre-v2.5; response model echo is absent, not invented. No human listening claim.
- Served main JavaScript and the latest 100 log entries contained no known private values; exact synthetic transcript absent from checked logs. This bounded check is not a full-history/PII/pentest guarantee.
- Controlled app restart observed a newly started process and idempotent seed. Readiness200, one final active instance, exact unchanged order/provenance/audit, three locations/four assets. No extra provider call for restart. This does not claim rollback/managed backup verification.

Public files contain sanitized metadata and synthetic-data screenshots. Keys, JWTs, passwords, database connection strings, raw responses/logs and WAV stay in ignored private storage. The acceptance run submitted one STT request and one TTS request through the app; internal provider retries were not independently counted. No extra paid calls were made to poll readiness.

## Remaining gates

Fresh human microphone/new-sentence validation, 15 distinct authentic audio cases with ground truth, ten consecutive complete workflows, listed implementation/dedicated-test gaps, final review/tag and participant video/post/contributions/form remain open. See ../roadmap-audit.md. The user alone submits the final form.

Free Render PostgreSQL has no managed backups and expires at `2026-12-09T12:16:30.004422Z`; app files are ephemeral and web service may cold-start. No paid upgrade, external DB access or production SLA is claimed. Private demo logins remain in private/demo-accounts.json.
