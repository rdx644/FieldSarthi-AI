# Hosted judge release — 2026-11-10 IST

Application commit **6f702c26f5d0ebca99cc71ba870bb7031fdd4dcd** is live at
https://fieldsaarthi-ai.onrender.com, deployment `dep-dbp1rkek1f9s73aqchvg`.
[Exact application-main CI passed](https://github.com/rdx644/FieldSarthi-AI/actions/runs/42682797881).
Blueprint GNANI is in_sync. Select **Open judge demo**; no password is needed.

- [Hosted authorization/health checks](judge-release-verification.json): only the
  explicitly approved WO-AFF1E3EE3BD2 is public, still OPEN/version 1 with its original
  transcript hash, actual Prisma provenance and creation audit unchanged.
- [Deployed browser checks](judge-browser-verification.json): login, dashboard,
  desktop/mobile detail and refresh passed with no reported axe violations,
  horizontal overflow or JavaScript errors. Screenshots accompany the result.
- [Ten consecutive genuine hosted workflows](reliability.json) passed: Prisma,
  explicit confirmation, idempotent replay, supervisor assignment/start/resolution,
  and persisted read-back. One consenting clip was repeated for reliability;
  this is separate from the distinct-recording evaluation.
- [One genuine saved-ticket Timbre request](judge-release-tts.json) returned valid
  6.4-second WAV and left the saved order/audit unchanged.
- [Controlled restart](judge-release-restart.json) observed a new ready instance.
  All ten workflow IDs, states, versions, provider metadata and audit counts
  matched pre-restart evidence. The approved report additionally retained its
  original transcript hash. No provider call was needed for restart verification.
- The separate [15-recording development evaluation](../audio-evaluation.json)
  scored 12/15 complete cases, with all six safety cases blocked. Hindi/English/
  Hinglish were tested; Tamil is unverified. Same-corpus refinement is disclosed.

190 backend tests and frontend/browser/audit/container checks passed. Engineering
and measured evaluation gaps listed in the historical audit are superseded by
[the current completion record](../judge-readiness.md). Individual contributions,
eligibility attestations, final video/post and the user-reserved form remain pending.
Free PostgreSQL still has no managed backups and expires on 2026-12-09; the approved
private export/isolated restore does not establish a managed backup SLA.

The following sections retain earlier point-in-time evidence and call counts.

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

## Later participant microphone verification

The participant confirmed making a new Hindi microphone recording and supplied WO-AFF1E3EE3BD2. [The separate evidence](human-microphone-verification.json) records server-read confirmed intake, actual distinct Prisma v2.5 request, 5.16-second duration, persisted Warehouse C/Exhaust Fan C-03 order and creation audit. The ticket remains OPEN and was not modified by the agent. No additional provider request was needed to verify it. Earlier runtime/deployment JSON files are point-in-time records from the prerecorded test before this participant check; their fresh-human false/pending fields are superseded by this later artifact. The source attestation is explicit; no audio-origin forensic or broader accuracy claim.

## Historical remaining gates

At this earlier checkpoint, the 15-case evaluation, ten-run reliability and implementation/test gaps were open. The hosted judge release above supersedes those observations. Participant video/post/contributions/form remain user-owned; the form is unsubmitted.

Free Render PostgreSQL has no managed backups and expires at `2026-12-09T12:16:30.004422Z`; app files are ephemeral and web service may cold-start. No paid upgrade, external DB access or production SLA is claimed. Private demo logins remain in private/demo-accounts.json.
