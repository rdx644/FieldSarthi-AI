# Full roadmap conformance audit - 2026-11-09

Latest implementation completion: [judge readiness evidence](judge-readiness.md)
supersedes the historical implementation/test-gap assessments below. Exact spans,
manual provenance, queue/cancellation controls, typed responses, disclosure,
telemetry, missing regression scenarios, automated reliability and CI history/full
browser gates are now implemented and locally verified. Authentic recordings,
participant submission and free-plan managed-backup limits remain distinct open gates.


Verdict: **PARTIALLY FOLLOWED; complete roadmap/release sign-off is HOLD.** The working development candidate is merged, but development completion is not end-to-end roadmap completion. No unexecuted human speech, hosted run, public post, contribution statement or form submission is claimed. This verdict does not revoke the user's authorization to provision the free Render demo and gather hosted evidence.

Baseline inspected: merged main `8146882af557d46491888a644081d53c485ada13`, tag `v0.2.0-rc.1`. `git fetch origin --prune --tags` and remote main lookup showed `0` ahead / `0` behind. Main's [exact CI run](https://github.com/rdx644/FieldSarthi-AI/actions/runs/42527535002) succeeded, including Linux/browser/audit/Docker. Protection requires quality/PR/conversation resolution and forbids force pushes/deletion.

The original working tree was not clean: `.env.example` contained a safe `YOUR API KEY` placeholder edit, and the root roadmap was untracked. Both are intentionally preserved in this audit branch for publication. The root roadmap is byte-identical to `docs/roadmap.md`; the plan is not rewritten to erase gaps. Ignored private credentials/audio/database files remain local and are not sync targets.

## Later deployment addendum

The baseline audit below is preserved as a point-in-time assessment. Subsequent authorized work deployed https://fieldsaarthi-ai.onrender.com and registered actual Blueprint GNANI. Authenticated validation, genuine hosted prerecorded STT/TTS/browser workflow, production cookies/authorization/secret checks and controlled restart persistence are now verified; see [the actual hosted evidence](hosted/README.md). These results supersede the baseline's missing-account/hosting/prerecorded-smoke/restart observations. They do **not** close fresh human speech,15 distinct authentic recordings, ten consecutive full workflows, managed backups/rollback, the listed code/test gaps or user-owned submission. Full roadmap sign-off remains HOLD.

## Later fresh human microphone addendum

After hosted deployment, the participant supplied WO-AFF1E3EE3BD2 from a newly spoken Hindi microphone recording. Confirmed intake, actual distinct Gnani model/request metadata, 5.16-second duration, durable order and creation audit were independently read back; [evidence](hosted/human-microphone-verification.json). The report remains OPEN. This supersedes the earlier missing-new-Hindi-sentence observation for that one sample. It does not close the 15-clip evaluation, ten complete workflows, broader language/device coverage, final video or other roadmap gaps. The original baseline and earlier deployment snapshot remain historical records.

## Fresh executed verification

- Isolated PostgreSQL was stopped at audit start. Restarted only `private/postgres-data` on 127.0.0.1:55432. The initial stalled test run was stopped; it is not counted as a pass.
- Fresh `api/.venv/Scripts/python.exe -m pytest -q`: **87 passed in 21.97s** against `fieldsaarthi_test`; no paid provider calls.
- Backend Ruff check/format and strict mypy pass. Frontend lint/Prettier/TypeScript/Vite build pass.
- Local app restarted; `/`, `/health/live`, `/health/ready` each HTTP 200. These checks do not close hosted readiness or speech gates.
- Current blueprint/public schema, content/secret scan and audit completeness checks are recorded separately in `roadmap-audit-checks.json`. Existing provider/browser/backup artifacts retain their original timestamps; historical evidence is not relabeled as a fresh live execution.

## Section and subsection coverage

Every numbered heading is included, through section23. IMPLEMENTED describes source/evidence within the stated limits; PARTIAL and USER items are not passed gates. OPTIONAL/DEFERRED is permitted by the original plan.

| Roadmap section (source line) | Assessment | Evidence / qualification |
|---|---|---|
| 0 Executive decision and success definition (L14) | PARTIAL | Real prerecorded Hindi/provider -> reviewed order -> supervisor flow exists in browser/live-browser-smoke.json. Fresh human speech, KPI-08/public video and ten-run reliability proof remain missing. |
| 0.1 Product in one sentence (L16) | PARTIAL | Real prerecorded Hindi/provider -> reviewed order -> supervisor flow exists in browser/live-browser-smoke.json. Fresh human speech, KPI-08/public video and ten-run reliability proof remain missing. |
| 0.2 The minimum qualifying working demonstration (L20) | PARTIAL | Real prerecorded Hindi/provider -> reviewed order -> supervisor flow exists in browser/live-browser-smoke.json. Fresh human speech, KPI-08/public video and ten-run reliability proof remain missing. |
| 0.3 Primary differentiator (L34) | PARTIAL | Real prerecorded Hindi/provider -> reviewed order -> supervisor flow exists in browser/live-browser-smoke.json. Fresh human speech, KPI-08/public video and ten-run reliability proof remain missing. |
| 0.4 Outcome metrics (proposed engineering targets, not Gnani scoring) (L38) | PARTIAL | KPI-02 is 15/15 implemented text fixtures only; KPI-08 not done. Field-level ASR metrics/complete-case results on 15 recordings are absent. |
| 1 Official challenge compliance — no-invalidation controls (L53) | PARTIAL / USER | docs/compliance.md and final-checklist.md: team/form receipt confirmed; individual eligibility/registration/one-entry attestations, final contributions, post URLs and form confirmation are pending. No publishing/submission authorized here. |
| 2 Product charter and operating assumptions (L84) | IMPLEMENTED / LIMITS | Synthetic one-organization worker/supervisor use case is implemented. Hindi/Hinglish is the authentic baseline; English/Tamil speech is unverified. P2/non-goals remain excluded. |
| 2.1 Problem statement (L86) | IMPLEMENTED / LIMITS | Synthetic one-organization worker/supervisor use case is implemented. Hindi/Hinglish is the authentic baseline; English/Tamil speech is unverified. P2/non-goals remain excluded. |
| 2.2 Target personas (L90) | IMPLEMENTED / LIMITS | Synthetic one-organization worker/supervisor use case is implemented. Hindi/Hinglish is the authentic baseline; English/Tamil speech is unverified. P2/non-goals remain excluded. |
| 2.3 Realistic example (L99) | IMPLEMENTED / LIMITS | Synthetic one-organization worker/supervisor use case is implemented. Hindi/Hinglish is the authentic baseline; English/Tamil speech is unverified. P2/non-goals remain excluded. |
| 2.4 Locked assumptions to avoid overengineering (L105) | IMPLEMENTED / LIMITS | Synthetic one-organization worker/supervisor use case is implemented. Hindi/Hinglish is the authentic baseline; English/Tamil speech is unverified. P2/non-goals remain excluded. |
| 2.5 Explicit non-goals for the November 10 build (L116) | IMPLEMENTED / LIMITS | Synthetic one-organization worker/supervisor use case is implemented. Hindi/Hinglish is the authentic baseline; English/Tamil speech is unverified. P2/non-goals remain excluded. |
| 3 Scope backlog with traceable priorities (L122) | PARTIAL | FR-01..25 core implementation is present, with finer gaps below. RTM covers all 12 O, 25 FR and 14 NFR IDs. NFR-01/11, authentic multilingual evaluation and official submission remain open; EXP-01 is optional. |
| 3.1 Functional requirements and acceptance conditions (L142) | PARTIAL | FR-01..25 core implementation is present, with finer gaps below. RTM covers all 12 O, 25 FR and 14 NFR IDs. NFR-01/11, authentic multilingual evaluation and official submission remain open; EXP-01 is optional. |
| 3.2 Nonfunctional requirements (engineering acceptance targets) (L172) | PARTIAL | FR-01..25 core implementation is present, with finer gaps below. RTM covers all 12 O, 25 FR and 14 NFR IDs. NFR-01/11, authentic multilingual evaluation and official submission remain open; EXP-01 is optional. |
| 3.3 Requirement-to-evidence traceability matrix (RTM) (L191) | PARTIAL | FR-01..25 core implementation is present, with finer gaps below. RTM covers all 12 O, 25 FR and 14 NFR IDs. NFR-01/11, authentic multilingual evaluation and official submission remain open; EXP-01 is optional. |
| 4 Lightweight CMMI-inspired delivery process (not certification) (L210) | PARTIAL | Protected PR/main, locks, CI, RTM, risks, candidate tag and evidence exist. Full G0/G1/G3/G4/G5 closure, human release review, daily process/burndown and final v1.0.0-submission tag are not evidenced. |
| 4.1 Project lifecycle / release gates (L227) | PARTIAL | G1/G2 have genuine local proof. Exact deployed-key G1/new-speech G2 and full G3 are not closed; G4/G5 not done. |
| 4.2 Development standards and branch policy (L247) | PARTIAL | Protected main/current CI and v0.2.0-rc.1 exist. Historical commits do not all use the proposed requirement-ID naming convention. v1.0.0-submission must wait for actual release gates. |
| 4.3 Definition of Ready (DoR) / Done (DoD) (L257) | PARTIAL | DoD is partially fulfilled locally; participant review/deployed proof cannot be inferred from agent success. |
| 5 Architecture and authoritative data flow (L264) | IMPLEMENTED / VARIATIONS | See architecture.md, services/orders.py and migrations. Eight retrospective ADR records now describe actual choices and tradeoffs. Reopen is optional and intentionally absent; terminal resolved/cancelled states are enforced. |
| 5.1 Architecture diagram (L266) | IMPLEMENTED / VARIATIONS | See architecture.md, services/orders.py and migrations. Eight retrospective ADR records now describe actual choices and tradeoffs. Reopen is optional and intentionally absent; terminal resolved/cancelled states are enforced. |
| 5.2 Trust boundaries and system ownership (L286) | IMPLEMENTED / VARIATIONS | See architecture.md, services/orders.py and migrations. Eight retrospective ADR records now describe actual choices and tradeoffs. Reopen is optional and intentionally absent; terminal resolved/cancelled states are enforced. |
| 5.3 Sequence of a valid report (L295) | IMPLEMENTED / VARIATIONS | See architecture.md, services/orders.py and migrations. Eight retrospective ADR records now describe actual choices and tradeoffs. Reopen is optional and intentionally absent; terminal resolved/cancelled states are enforced. |
| 5.4 State machines (L330) | IMPLEMENTED / VARIATIONS | See architecture.md, services/orders.py and migrations. Eight retrospective ADR records now describe actual choices and tradeoffs. Reopen is optional and intentionally absent; terminal resolved/cancelled states are enforced. |
| 5.5 Architecture Decision Records (ADRs) (L335) | IMPLEMENTED / VARIATIONS | ADR-001..008 now present in docs/adrs with actual implementation choices and remaining limitations. |
| 6 Technology baseline and repository layout (L350) | IMPLEMENTED / VARIATIONS | uv/npm locks, typed React/FastAPI, migrations and Docker exist. Custom hash router/fetch/state replace suggested React Router/Query; browser scripts replace Vitest. Provider models/limits are fixed constants; unused example env names are not runtime settings. |
| 6.1 Pinned build choices (L352) | IMPLEMENTED / VARIATIONS | uv/npm locks, typed React/FastAPI, migrations and Docker exist. Custom hash router/fetch/state replace suggested React Router/Query; browser scripts replace Vitest. Provider models/limits are fixed constants; unused example env names are not runtime settings. |
| 6.2 Proposed monorepo tree (L369) | IMPLEMENTED / VARIATIONS | uv/npm locks, typed React/FastAPI, migrations and Docker exist. Custom hash router/fetch/state replace suggested React Router/Query; browser scripts replace Vitest. Provider models/limits are fixed constants; unused example env names are not runtime settings. |
| 6.3 Configuration contract (`.env.example`) (L444) | IMPLEMENTED / VARIATIONS | Root safe example includes required backend/seed/test values. Models/limits/TTL/logging are fixed in code; the roadmap environment contract is illustrative, not fully configurable. |
| 7 Database design, invariants, migrations and synthetic seed (L469) | IMPLEMENTED / TEST GAPS | Seven tables, seed, unique intake, locks, immutable provider/audit, original/corrected separation and real backup restore exist. DB schema is adapted (string IDs/application UUIDs/JSON). Asset-location check is in service; dedicated rollback/constraint tests are incomplete. |
| 7.1 Entity relationships (L471) | IMPLEMENTED / TEST GAPS | Seven tables, seed, unique intake, locks, immutable provider/audit, original/corrected separation and real backup restore exist. DB schema is adapted (string IDs/application UUIDs/JSON). Asset-location check is in service; dedicated rollback/constraint tests are incomplete. |
| 7.2 Minimal relational schema (adapt in Alembic) (L486) | IMPLEMENTED / TEST GAPS | Seven tables, seed, unique intake, locks, immutable provider/audit, original/corrected separation and real backup restore exist. DB schema is adapted (string IDs/application UUIDs/JSON). Asset-location check is in service; dedicated rollback/constraint tests are incomplete. |
| 7.3 Data invariants and transaction boundaries (L588) | IMPLEMENTED / TEST GAPS | Seven tables, seed, unique intake, locks, immutable provider/audit, original/corrected separation and real backup restore exist. DB schema is adapted (string IDs/application UUIDs/JSON). Asset-location check is in service; dedicated rollback/constraint tests are incomplete. |
| 7.4 Example seed inventory (synthetic only) (L603) | IMPLEMENTED / TEST GAPS | Seven tables, seed, unique intake, locks, immutable provider/audit, original/corrected separation and real backup restore exist. DB schema is adapted (string IDs/application UUIDs/JSON). Asset-location check is in service; dedicated rollback/constraint tests are incomplete. |
| 7.5 Migration/rollback procedure (L616) | IMPLEMENTED / TEST GAPS | Actual private pg_dump -> new scratch restore counts match. Hosted restart/rollback remains unexecuted. |
| 8 API design — internal application contracts (L627) | IMPLEMENTED / VARIATIONS | All proposed routes are represented in routers, including duplicate and saved-ticket audio. Review PATCH stores corrected transcript; selected fields commit atomically on confirmation. Error envelopes are safe; provider failures use generic 503 except no-speech 422. Response dict schemas are not fully typed. |
| 8.1 Example successful transcription response (our schema) (L653) | IMPLEMENTED / VARIATIONS | All proposed routes are represented in routers, including duplicate and saved-ticket audio. Review PATCH stores corrected transcript; selected fields commit atomically on confirmation. Error envelopes are safe; provider failures use generic 503 except no-speech 422. Response dict schemas are not fully typed. |
| 8.2 Example work-order creation request (L684) | IMPLEMENTED / VARIATIONS | All proposed routes are represented in routers, including duplicate and saved-ticket audio. Review PATCH stores corrected transcript; selected fields commit atomically on confirmation. Error envelopes are safe; provider failures use generic 503 except no-speech 422. Response dict schemas are not fully typed. |
| 8.3 Suggested standardized application errors (L704) | IMPLEMENTED / VARIATIONS | Safe typed codes exist, but all provider errors except no-speech are generic HTTP 503 in the intake route; operator-specific UI messages differ from proposed taxonomy. |
| 9 Gnani integration specification — the central technical proof (L725) | PARTIAL | Genuine curl/HTTPX STT, local browser flow and real Timbre proof exist. Fixed endpoints/models, selected locale, bounded retries and actual provenance are implemented. Hosted key smoke, new human capture, manual text support and broader language/audio evidence remain open. v3 remains optional. |
| 9.1 Account and authorization spike (FIRST task) (L727) | PARTIAL | Real consenting sample/curl/HTTPX evidence exists. Smoke uses explicit consent/spend flags rather than an opt-in environment flag; exact deployed-key gate remains pending. |
| 9.2 Exact Prisma v2.5 REST contract (official) (L739) | PARTIAL | Genuine curl/HTTPX STT, local browser flow and real Timbre proof exist. Fixed endpoints/models, selected locale, bounded retries and actual provenance are implemented. Hosted key smoke, new human capture, manual text support and broader language/audio evidence remain open. v3 remains optional. |
| 9.3 Optional Prisma v3.0 experiment — only after P0 passes (L766) | PARTIAL | OPTIONAL / DEFERRED: Prisma v3.0 experiment is not required for the verified v2.5 baseline. |
| 9.4 Browser audio — subtle but critical implementation issue (L772) | PARTIAL | Bounded FFmpeg sample-count inspection intentionally replaces ffprobe. No manual MANUAL_TEXT support path is implemented. New human capture remains pending. |
| 9.5 Provider adapter implementation plan (L787) | PARTIAL | Conservative adapter requires model/request ID and rejects missing proof; retries avoid ambiguous read/write timeouts to control spend. Both differ deliberately from permissive example suggestions. |
| 9.6 Exact Timbre v2.5 contract (P1) (L805) | PARTIAL | Real requested Timbre v2.5/Nalini Hindi WAV; response model is not invented. English/Tamil/code-mix voices/language choice are not implemented. |
| 9.7 Provider error taxonomy and safe behavior (L839) | PARTIAL | Provider statuses map to safe codes and no false success. Generic end-user error text does not explain each operator/configuration category. Current console balance unqueried. |
| 10 Multilingual extraction, validation and decision logic (L860) | PARTIAL | Unicode catalog extraction/human validation exist; 15 text fixtures pass. parser_version is absent, evidence contains matched catalog aliases rather than exact source spans, and the original 15-scenario multilingual/ambiguity suite differs from implemented positive fixtures. |
| 10.1 Why the extraction layer is not “magical AI” (L862) | PARTIAL | Unicode catalog extraction/human validation exist; 15 text fixtures pass. parser_version is absent, evidence contains matched catalog aliases rather than exact source spans, and the original 15-scenario multilingual/ambiguity suite differs from implemented positive fixtures. |
| 10.2 Extraction pipeline (L866) | PARTIAL | Current output lacks parser_version and exact source-span offsets; field_evidence is catalog aliases. Unknown facts still require human correction. |
| 10.3 Example extraction object (our schema) (L879) | PARTIAL | Actual suggestion object is flatter than the illustrative per-field object. No arbitrary confidence scores; provenance is real. |
| 10.4 Ambiguity and safety rules (L911) | PARTIAL | Server rejects wrong catalog relationships and empty data. Multiple assets in a location are unresolved; cross-location/multi-issue original scenarios need dedicated tests. Cancellation does not require a justification note. |
| 10.5 Optional LLM-based structured extraction (only after deterministic path works) (L925) | PARTIAL | OPTIONAL / DEFERRED: no LLM parser, hosted Evon, RAG or autonomous dispatch introduced. |
| 11 UI/UX implementation specification (L931) | PARTIAL | All primary screens, explicit confirmation, review/provenance, timeline, status search and responsive/axe checks exist. Queue location/assignee/priority filters are API-only. No manual support path; permission-denial/25-second timer/other UX branches lack dedicated browser regression evidence. |
| 11.1 Pages and components (L933) | PARTIAL | Worker/review/order/queue/detail screens exist. Location/assignee/priority filtering is available only via API, not queue controls; per-page counts are labeled accurately. |
| 11.2 Required controls and accessibility (L945) | PARTIAL | Recorded soft-stop code exists; six previous axe views are clean. Permission-denied and full 25-second auto-stop are not separately evidenced automated cases. |
| 11.3 Component contracts (L957) | PARTIAL | All primary screens, explicit confirmation, review/provenance, timeline, status search and responsive/axe checks exist. Queue location/assignee/priority filters are API-only. No manual support path; permission-denial/25-second timer/other UX branches lack dedicated browser regression evidence. |
| 11.4 Visual direction (L967) | PARTIAL | All primary screens, explicit confirmation, review/provenance, timeline, status search and responsive/axe checks exist. Queue location/assignee/priority filters are API-only. No manual support path; permission-denial/25-second timer/other UX branches lack dedicated browser regression evidence. |
| 12 Reliability, security, privacy and production controls (L973) | PARTIAL | Server secrets, auth/RBAC/ownership, cookie CSRF, CSP, bounded decode, single-worker budgets, temporary audio and body-free HTTP logging are implemented. Dedicated XSS/SQLi/readiness-down tests, provider-stage success/error telemetry and explicit Gnani/retention disclosure remain gaps. |
| 12.1 Threat model and mitigations (L975) | PARTIAL | Server secrets, auth/RBAC/ownership, cookie CSRF, CSP, bounded decode, single-worker budgets, temporary audio and body-free HTTP logging are implemented. Dedicated XSS/SQLi/readiness-down tests, provider-stage success/error telemetry and explicit Gnani/retention disclosure remain gaps. |
| 12.2 Basic SRE controls (L993) | PARTIAL | Live/ready/body-free HTTP timing and request-ID correlation implemented. Provider-stage model/request/error metrics and alerting/dashboard are not emitted as proposed. |
| 12.3 Privacy and ethics (L1004) | PARTIAL | Server secrets, auth/RBAC/ownership, cookie CSRF, CSP, bounded decode, single-worker budgets, temporary audio and body-free HTTP logging are implemented. Dedicated XSS/SQLi/readiness-down tests, provider-stage success/error telemetry and explicit Gnani/retention disclosure remain gaps. |
| 13 End-to-end implementation work breakdown (WBS) (L1010) | PARTIAL | Every WBS-00..08 task is assessed below; coding completion does not close human speech, hosted acceptance, authentic corpus or participant submission gates. |
| 14 Test strategy, fixtures and objective validation (L1138) | PARTIAL | 87 tests and prior real browser/provider evidence exist. Explicit contract fixtures are isolated to tests. The specified negative-case catalog is not fully represented; 15 text cases are not the original 15 real audio scenarios. See test mapping below. |
| 14.1 Test pyramid and boundaries (L1140) | PARTIAL | 87 tests and prior real browser/provider evidence exist. Explicit contract fixtures are isolated to tests. The specified negative-case catalog is not fully represented; 15 text cases are not the original 15 real audio scenarios. See test mapping below. |
| 14.2 Test ID catalog (L1153) | PARTIAL | See every catalog group below; do not treat 87 passes as proof of absent named negative cases. |
| 14.3 Synthetic 15-case multilingual evaluation suite (L1211) | PARTIAL | Original Hindi/English/Tamil/code-mix/unknown/ambiguous/silence 15 audio scripts have not been recorded/evaluated; implemented parser fixtures are different positive cases. |
| 15 Short-horizon schedule: November 8–10, 2026 (IST) (L1245) | ACTIVE PLAN | The date-based schedule is guidance, not evidence that timeboxes happened. Development is merged; remaining critical path is Render access -> hosted smoke/new speech -> authentic evaluation -> user video/post/form. P2 remains deferred. |
| 15.1 Milestone order / critical path (L1259) | ACTIVE PLAN | The date-based schedule is guidance, not evidence that timeboxes happened. Development is merged; remaining critical path is Render access -> hosted smoke/new speech -> authentic evaluation -> user video/post/form. P2 remains deferred. |
| 15.2 Strict cut lines (L1268) | ACTIVE PLAN | The date-based schedule is guidance, not evidence that timeboxes happened. Development is merged; remaining critical path is Render access -> hosted smoke/new speech -> authentic evaluation -> user video/post/form. P2 remains deferred. |
| 16 CI/CD, production readiness and release gate (L1278) | PARTIAL / HOLD | Exact merged-main CI passed all retained Linux/browser/audit/container gates. Blueprint is prepared; no hosted availability/restart/HTTPS microphone result yet. Free PostgreSQL lacks the specified managed backups. No final release tag or human approval is invented. |
| 16.1 Local developer commands (template — adjust to actual dependencies) (L1280) | PARTIAL / HOLD | Exact merged-main CI passed all retained Linux/browser/audit/container gates. Blueprint is prepared; no hosted availability/restart/HTTPS microphone result yet. Free PostgreSQL lacks the specified managed backups. No final release tag or human approval is invented. |
| 16.2 CI pipeline (suggested sequence) (L1313) | PARTIAL / HOLD | CI retains lint/types/tests/audits/browser/Docker. It lacks automated history/secret/raw-media scanning and full fixture-provider voice-to-resolved browser CI flow. |
| 16.3 Deployment and smoke procedure (L1325) | PARTIAL / HOLD | Pending actual HTTPS deploy, resource limits, secret/cookie/log inspection, microphone/new speech, supervisor flow and restart. Free DB has no managed backups; manual export is a documented limitation. |
| 16.4 Formal release checklist (G3) (L1341) | PARTIAL / HOLD | HOLD for complete roadmap release. Current v0.2.0-rc.1 is a candidate; no final v1.0.0-submission or independent human approval. |
| 17 Risk register and mitigation triggers (L1368) | MAINTAINED | risks.md now covers every original R-01..14 plus remote protection/free DB lifecycle. Evidence gaps are distinguished from actual defects. Severity policy remains in force. |
| 17.1 Defect severity policy (L1389) | MAINTAINED | risks.md now covers every original R-01..14 plus remote protection/free DB lifecycle. Evidence gaps are distinguished from actual defects. Severity policy remains in force. |
| 18 Suggested Codex / AI-agent implementation protocol (L1398) | FOLLOWED / LIMITS | Repository instructions and previous authorization read; changes and actual checks are recorded. No provider facts or human contributions invented. This audit does not claim an independent human release approval. |
| 18.1 Repository contract for coding agents (`AGENTS.md` suggested) (L1402) | FOLLOWED / LIMITS | Repository instructions and previous authorization read; changes and actual checks are recorded. No provider facts or human contributions invented. This audit does not claim an independent human release approval. |
| 18.2 Task slices and prompt starters (L1421) | FOLLOWED / LIMITS | Repository instructions and previous authorization read; changes and actual checks are recorded. No provider facts or human contributions invented. This audit does not claim an independent human release approval. |
| 18.3 Completion report required from every agent task (L1443) | FOLLOWED / LIMITS | Repository instructions and previous authorization read; changes and actual checks are recorded. No provider facts or human contributions invented. This audit does not claim an independent human release approval. |
| 19 Public demonstration plan and technical proof package (L1459) | PREPARED / USER | One-page pitch, project explanation, actual-form 2-3 minute script and social draft exist. Final new-speech video, optional 60-second cut, media review, public post/tag/hashtags, URLs, contributions and form confirmation remain undone. |
| 19.1 Show exactly what is real (L1461) | PREPARED / USER | One-page pitch, project explanation, actual-form 2-3 minute script and social draft exist. Final new-speech video, optional 60-second cut, media review, public post/tag/hashtags, URLs, contributions and form confirmation remain undone. |
| 19.2 60-second public demo shot list (the Demo Day Drop category is specifically 60 seconds) (L1471) | PREPARED / USER | 60-second shot list is optional social cut; actual inspected final form requires 2-3 minutes. Neither final recording is claimed complete. |
| 19.3 Longer technical demonstration (recommended evidence, not mandatory separate official video) (L1484) | PREPARED / USER | One-page pitch, project explanation, actual-form 2-3 minute script and social draft exist. Final new-speech video, optional 60-second cut, media review, public post/tag/hashtags, URLs, contributions and form confirmation remain undone. |
| 19.4 Submission project description template (L1494) | PREPARED / USER | One-page pitch, project explanation, actual-form 2-3 minute script and social draft exist. Final new-speech video, optional 60-second cut, media review, public post/tag/hashtags, URLs, contributions and form confirmation remain undone. |
| 19.5 Public post content checklist (L1506) | PREPARED / USER | One-page pitch, project explanation, actual-form 2-3 minute script and social draft exist. Final new-speech video, optional 60-second cut, media review, public post/tag/hashtags, URLs, contributions and form confirmation remain undone. |
| 19.6 Official final-form checklist (L1518) | PREPARED / USER | USER RESERVED: final form stays unsubmitted under explicit prior instruction. Do not invent confirmation or public URLs. |
| 20 Post-submission technical interview preparation (L1537) | PREPARED / USER | interview-preparation.md now covers all twelve technical prompts with source/evidence and honest accuracy limits. Personal contribution paragraphs and each member rehearsal remain participant-owned. |
| 21 Evidence index and final handoff package (L1556) | PARTIAL | README, full source, pitch, architecture/ADRs, RTM, evidence, risks, operations and scripts exist. No public hosted URL/video/post/form confirmation exists yet. Original roadmap root copy is identical to docs/roadmap.md and is preserved unchanged. |
| 21.1 Suggested README outline (L1576) | PARTIAL | README covers implemented stack/setup/evidence/limits. Public screenshots/evidence exist; hosted/public video links and finalized personal contributions remain absent. |
| 22 Master execution checklist (release and contest completion) (L1591) | PARTIAL | Core implementation/local code checks and candidate tag are evidenced. Eligibility/one-entry, new speech/15 audio cases, hosted proof, final release approval/tag and all public submission evidence remain open. |
| 23 Reference index and verification notes (L1621) | REVIEWED / LIMITS | Official source index/snapshots exist. Render blueprint/free/PostgreSQL docs were rechecked in this audit. Remaining empirical checks include current console balance, language quality, hosted resource behavior and final form/media. Historical source snapshots are not a current entitlement guarantee. |

## Every WBS task

Source is the unchanged WBS in roadmap section13. Broad implementation evidence does not imply every negative test or final gate passed.

| Task | Required work | Actual status / evidence |
|---|---|---|
| WBS-00.1 | Read programme rules/terms; verify registration, eligibility, team count, final form delivery. | PARTIAL: team/form receipt confirmed; each member eligibility/registration and one-entry attestations pending. |
| WBS-00.2 | Verify Gnani account, credits, key scope; save credentials privately. | LOCAL VERIFIED: key/scope and genuine STT/TTS; reported starting balance only; current balance not queried. |
| WBS-00.3 | Snapshot the official docs/URLs used for endpoint decisions; record last checked date. | VERIFIED: docs/sources snapshots/index, original roadmap URLs retained. |
| WBS-00.4 | Freeze P0 backlog, project title, roles, language baseline and demonstration scenario. | VERIFIED: scope.md baseline; updated to actual implemented scope and user authorization. |
| WBS-00.5 | Create GitHub repo, protected main workflow, issue tracker, RTM and risk register. | VERIFIED: GitHub remote/protected main/CI, issues #3/#4, RTM and risks; no board/burndown evidence. |
| WBS-01.1 | Record short Hindi synthetic audio; verify actual format/duration locally. | LOCAL VERIFIED: private consenting Hindi WAV; new human browser speech remains pending. |
| WBS-01.2 | Run documented cURL call to `POST /stt/v3` with `X-API-Key-ID`. | VERIFIED: gnani-curl evidence, HTTP 200. |
| WBS-01.3 | Confirm nonempty transcript, actual `request_id`, actual model, HTTP status. | VERIFIED: actual STT model/request ID/nonempty transcript. |
| WBS-01.4 | Build `GnaniSpeechClient` HTTPX adapter with typed success/error parsing. | VERIFIED: real HTTPX adapter, strict contract parser and typed safe errors. |
| WBS-01.5 | Write contract tests for success, no-speech, 400, 401, 402, 403, 429, 500 and timeout. | PARTIAL: auth/quota/rate/input/timeout contract tests; separate 500/502/504/success-false cases not all explicit. |
| WBS-01.6 | Save redacted live integration evidence (`docs/evidence/gnani-stt-live.md`). | VERIFIED: gnani-stt-live.md and sanitized metadata JSON. |
| WBS-02.1 | Bootstrap React/Vite/TypeScript and FastAPI app with strict formatting. | VERIFIED: React/Vite/TypeScript + FastAPI; fresh lint/types/build pass. |
| WBS-02.2 | Configure PostgreSQL, SQLAlchemy, Alembic initial migration. | VERIFIED: PostgreSQL 18 and Alembic0001/0002. |
| WBS-02.3 | Implement `users`, `locations`, `assets`, `report_intakes`, `work_orders`, `audit_events`, `idempotency_keys`. | VERIFIED: all seven domain tables implemented. |
| WBS-02.4 | Seed synthetic workers, supervisor, locations, equipment and aliases. | VERIFIED: two synthetic workers, supervisor, three locations/four assets. |
| WBS-02.5 | Implement seeded authentication with salted password hashing (Argon2/bcrypt) and verified role checks. | VERIFIED: Argon2, signed expiring sessions, active DB role/ownership checks. |
| WBS-02.6 | Implement `/health/live`, `/health/ready`, CORS, errors and structured request IDs. | VERIFIED: live/ready, body-free HTTP logs, request ID, CORS/errors. |
| WBS-02.7 | Add migration and access-control tests. | PARTIAL: migrations/access/immutable/race tests; not every negative insert/expiry/atomic rollback test exists. |
| WBS-03.1 | Implement microphone permission handling and recorder state machine. | PARTIAL: MediaRecorder/permission error code implemented; no fresh human/denial proof. |
| WBS-03.2 | Set 25-second soft stop, metadata preview, cancel/rerecord. | PARTIAL: soft-stop/preview/rerecord implemented; file-fed start/stop verified, 25s timer/cancel lifecycle not separately tested. |
| WBS-03.3 | Create multipart upload to our `/intakes/transcribe`; never invoke Gnani from React. | VERIFIED: browser uploads only to own backend. |
| WBS-03.4 | Validate size, media type, duration; convert WebM/Opus → WAV using protected ffmpeg invocation. | VERIFIED: body/signature/sample-count/decode deadline/temporary cleanup; real WebM release evidence, dedicated WebM regression missing. |
| WBS-03.5 | Call verified `GnaniSpeechClient` with selected `language_code`; preserve response metadata. | VERIFIED LOCAL: selected locale, genuine adapter, exact preserved metadata. |
| WBS-03.6 | Save real intake row with `READY_FOR_REVIEW` only after genuine nonempty STT result. | VERIFIED: persisted READY_FOR_REVIEW only after valid STT; no order until confirm. |
| WBS-03.7 | Delete temporary audio files and handle errors, retry state, empty transcript. | PARTIAL: cleanup/retry/error code implemented and negative tests; every cleanup/no-speech integration branch not separately covered. |
| WBS-03.8 | Add audio validation, provider adapter and live smoke tests. | PARTIAL: audio/provider/regression plus prerecorded live browser smoke; fresh-human final gate pending. |
| WBS-04.1 | Implement Unicode-safe alias normalization and deterministic parser. | VERIFIED: Unicode NFKC/casefold alias parser. |
| WBS-04.2 | Resolve location and asset candidates against DB; enforce asset-location relationship. | VERIFIED: DB-backed active catalog and asset-location validation. |
| WBS-04.3 | Extract issue category and nonauthoritative urgency suggestion with evidence. | PARTIAL: issue/urgency suggestions with matched aliases; exact source spans/parser_version absent. |
| WBS-04.4 | Implement `Review & Confirm` page showing raw transcript and editable corrections separately. | VERIFIED: Review.tsx preserves raw vs corrections. |
| WBS-04.5 | Validate required fields on server; reject ambiguities and missing records. | VERIFIED: required known catalog/description/explicit true confirmation server guards; some dedicated negative tests absent. |
| WBS-04.6 | Generate per-submission idempotency key; implement DB uniqueness/transaction logic. | VERIFIED: key/body hash, advisory/intake locks and unique constraints with concurrent tests. |
| WBS-04.7 | Commit confirmed intake → order → `CREATED` audit event in one transaction. | VERIFIED: intake/order/audit/idempotency atomic write in create_order. |
| WBS-04.8 | Show only server-returned real ticket code; verify after page refresh. | VERIFIED LOCAL: server-generated order code and actual browser refresh proof. |
| WBS-04.9 | Create 15-case extraction fixtures and negative validation tests. | PARTIAL: 15 positive text fixtures/negative checks differ from original multilingual/ambiguity scenarios; no authentic corpus. |
| WBS-05.1 | Implement authorized `/work-orders` listing with server paging/filters. | VERIFIED: authorized pagination/search and status/priority/location/assignee API filters. |
| WBS-05.2 | Implement supervisor queue: status, priority, location, assignee, created time. | VERIFIED: queue displays all required columns; location/assignee controls absent from UI. |
| WBS-05.3 | Implement authorized assignment and controlled priority adjustment. | VERIFIED: supervisor-only assignment and priority; current role checked. |
| WBS-05.4 | Enforce state machine and expected `version` on every workflow mutation. | VERIFIED: expected_version, locked changes and constrained states; cancellation justification not enforced. |
| WBS-05.5 | Transactionally write event history for each action. | VERIFIED: workflow mutation + audit event commit together; dedicated injected-DB-failure assertion absent. |
| WBS-05.6 | Implement ticket details, provenance panel and chronological timeline. | VERIFIED: details/provenance/raw-corrected timeline. |
| WBS-05.7 | Unit/integration/E2E tests for authorization, transitions and concurrency. | PARTIAL: real local browser loop and RBAC/state/race tests; all prescribed negative catalog cases not explicit. |
| WBS-06.1 | Verify live Timbre v2.5 key scope using safe short text. | VERIFIED LOCAL: actual requested Timbre v2.5 response. |
| WBS-06.2 | Add server-side TTS adapter; return binary WAV with correct MIME. | VERIFIED: bounded binary adapter + real streaming-WAV normalization. |
| WBS-06.3 | Add `Play acknowledgment` only after saved ticket success; nonblocking error state. | VERIFIED: saved-ticket control and tested outage isolation. |
| WBS-06.4 | Flag potential duplicates for the same asset in `OPEN/ASSIGNED/IN_PROGRESS` states; show warning, don't silently merge. | IMPLEMENTED: authorized active same-asset warnings/details; dedicated resolved-only/distinct-asset cases missing. |
| WBS-06.5 | Polish mobile, accessibility, empty/error states; remove decorative unimplemented elements. | PARTIAL: six automated axe/mobile views and keyboard check; permission/recording/failure UI branches incomplete. |
| WBS-06.6 | Document actual model usage and limitations. | VERIFIED: model/selected-language/fixed-clip limits documented; other language speech performance not claimed. |
| WBS-07.1 | Lint, typecheck, backend unit and API contract tests green. | VERIFIED FRESH: 87 backend tests; strict Ruff/mypy; frontend lint/format/type/build. |
| WBS-07.2 | Verify two-role RBAC, IDOR and direct HTTP requests, not only frontend route blocking. | VERIFIED: direct HTTP RBAC/IDOR/cookie/CSRF and two-worker isolation. |
| WBS-07.3 | Evaluate 15 real or consented short audio scripts, review ground truth and export results. | PENDING HUMAN: 15 distinct authentic audio scripts/ground truth/model results, not parser fixture reuse. |
| WBS-07.4 | Execute negative scenarios: empty, unsupported, oversized, corrupt, rate limited, provider down, wrong asset, duplicate, status conflict. | PARTIAL: media/provider/race/IDOR/stale/conflict tests; catalog test gaps below. |
| WBS-07.5 | Deploy HTTPS frontend and backend, production secret config and PostgreSQL; check DB migration. | PENDING ACCESS: authenticated Render creation and actual HTTPS/runtime/migration proof. |
| WBS-07.6 | Run production smoke with **real Gnani** from mobile/desktop browser using newly recorded clip. | PENDING HUMAN + HOST: new browser clip/real deployed Gnani/desktop-mobile flow. |
| WBS-07.7 | Run backup/rollback drill, secret scan, public repository inspection. | PARTIAL: real local backup/new-instance restore; exact-secret/history scan performed separately; hosted restart/rollback not executed. |
| WBS-07.8 | Freeze release tag and save evidence. | CANDIDATE ONLY: v0.2.0-rc.1 at8146882; final submission tag waits for real release gates. |
| WBS-08.1 | Record full technical run and a sharp 60-second showcase with actual app behavior. | PENDING HUMAN: full technical/new-speech demo and optional 60s cut; actual form needs2-3min. |
| WBS-08.2 | Verify audio/video clarity, accuracy of model names, no credentials/personal data shown. | PENDING HUMAN: inspect final media clarity/claims/no secrets. |
| WBS-08.3 | Draft project summary and each member's personally verifiable contributions. | PARTIAL: project explanation/one-page pitch ready; contributions deliberately undecided by user. |
| WBS-08.4 | Post public demo on LinkedIn and/or X; tag Gnani AI; both exact hashtags. | USER ACTION: no social post authorized or published. |
| WBS-08.5 | Verify post is public and directly opens for someone not signed into your account (where platform permits). | PENDING USER POST: no URL/public-access validation possible yet. |
| WBS-08.6 | Find official submission form from registration email, fill all requested fields and **nominate post URL(s)**. | USER RESERVED: actual form inspected privately; user explicitly forbids agent submission. |
| WBS-08.7 | Submit before November 10, 11:59 PM IST; retain visible/email confirmation. | USER RESERVED: no submitted form or confirmation. |
| WBS-08.8 | Share organically only. No bought promotion, exchange groups, bots or misleading teaser. | POLICY ADOPTED: organic-only plan; no bought/bot/swap activity performed. |

## Named test catalog coverage

Mappings are to inspected tests/source and previous actual evidence. Missing dedicated assertions are explicitly identified; a guard implemented in code is not itself executed negative-test proof.

| Roadmap tests | Coverage and limits |
|---|---|
| T-AUD-01 | PCM smoke metadata and real decoder checks: contract/test_smoke.py; test_intakes.py. |
| T-AUD-02 | Actual file-fed MediaRecorder/decoder browser evidence; no dedicated committed WebM->WAV regression. |
| T-AUD-03..04 | Corrupt/empty/overlong/oversize contract and intake checks; body limit before parser. |
| T-AUD-05 | Permission error handler exists; no dedicated permission-denied browser assertion/evidence. |
| T-STT-01..06 | test_gnani.py explicitly covers mapping/empty/auth/quota/429/400/422, no retries on auth, bounded retry, invalid proof/JSON/size. |
| T-STT-07 | 503/network/connect/read timeout covered; not every 500/502/504 shape/retry combination has a dedicated case. |
| T-LIVE-01 | Genuine private prerecorded sample calls exist; newly spoken browser sentence remains pending. |
| T-NLP-01..15 | 15 passing implemented positive text fixtures; original negative/Tamil/audio corpus differs and remains incomplete. |
| T-VAL-01..02 | Missing-location extraction tested; required command IDs validated. No separate missing-asset/blank-ID/required-field UI case for every branch. |
| T-VAL-03 | Known-catalog guards implemented; no dedicated unknown UUID test. |
| T-VAL-04 | Explicit mismatched asset/location regression exists. |
| T-VAL-05 | Description min-length/whitespace schema guard implemented; dedicated empty-description test absent. |
| T-VAL-06 | Candidate collision logic exists; original multiple-pump/multi-asset scenario not explicitly tested. |
| T-ORD-01..04 | Valid confirm/replay/same-key changed body/different keys same intake verified in test_workflow.py. |
| T-ORD-05 | Atomic transaction implemented; no injected DB-failure rollback/no-orphan test. |
| T-ORD-06 | Real local browser save/refresh and direct detail persistence evidenced. |
| T-ORD-07 | Concurrent different-key same-intake tested; same-key race not a separate explicit case. |
| T-ORD-08 | Service refuses failed/unready intake; no dedicated failed-intake-confirm regression. |
| T-RBAC-01..02 | Worker supervisor-action rejection and other-worker intake/order/queue isolation explicitly tested. |
| T-RBAC-03 | JWT invalid/expired guard exists; dedicated expired/invalid token assertion absent (malformed bearer/cookie fallback is tested). |
| T-RBAC-04 | Supervisor access in real workflow; not every filter/page/role combination explicitly tested. |
| T-WF-01..05 | Assignment/start/resolve/invalid transition/stale version are verified in direct API and previous real browser flow. |
| T-TTS-01 | Actual Gnani binary WAV and browser playback evidence; offline binary delivery/header repair tests exist. |
| T-TTS-02..04 | Error statuses/header handling/outage isolation tested; explicit successful HTTP200 JSON error and voice/model mismatch cases not dedicated. |
| T-DUP-01..03 | Ownership-filtered active-asset query implemented; three dedicated same-active/resolved-only/distinct-asset tests absent. |
| T-AUDIT-01 | Creation/assignment/status timeline asserted; update/delete/truncate guards exist. |
| T-AUDIT-02 | Raw/corrected storage separation implemented and browser-visible; explicit edit-then-immutable assertion is incomplete. |
| T-AUDIT-03 | Unauthorized order/intake detail returns404 in two-worker tests; provenance not serialized to unauthorized worker. |
| T-OPS-01 | Live/ready healthy test exists; DB-unavailable readiness503 case absent. |
| T-SEC-01 | Current exact-secret scan separately recorded; not a CI-enforced secret-history gate. |
| T-SEC-02 | React escapes transcript text; no dedicated malicious-transcript browser regression. |
| T-SEC-03 | Oversize/corrupt/audio-length rejection covered; not an exhaustive malicious-codec/resource attack suite. |
| T-E2E-01 | Previous actual local prerecorded Gnani->order->supervisor->refresh proof. New-human/hosted final path unverified; CI browser script covers non-billable views, not full voice workflow. |
| T-SUB-01..07 | Participant eligibility/contribution/video/post/tags/URLs/form/confirmation remain incomplete or user reserved. |

## Remaining work, in dependency order

1. Connect/verify the intended Render account/workspace and repository access; create the free Blueprint. Validate actual deployed commit/secrets/migrations/resource health. Existing `render.yaml` is the single canonical configuration; no divergent second YAML file.
2. Run actual HTTPS desktop/mobile workflow, inspect production cookies/logs/secret boundaries, restart/rollback and verify persisted DB records. The free plan has no managed backups and a 30-day DB life; explicit manual-export limitation does not pass the managed-backups requirement.
3. Participants record a new sentence through the deployed microphone and 15 distinct authentic scripts with reviewed ground truth. Export actual field accuracy/case failures and sample/model limits. Run the proposed ten consecutive complete workflows; no such reliability metric is currently claimed.
4. Close implementation gaps if strict roadmap equivalence is required: manual text accessibility path with distinct provenance; parser version/exact source spans; queue filter controls; cancellation justification; explicit Gnani/retention disclosure; provider-stage telemetry; clearer error categories; typed response contracts. None is silently counted as done.
5. Add the missing negative/atomicity/ambiguity/duplicate/readiness/XSS/permission/WebM regression cases identified above, and CI secret/media scanning/full deterministic workflow coverage. Reverify without weakening existing gates.
6. Independently review G3 and only then publish final release tag `v1.0.0-submission`. Preserve immutable candidate tag and exact evidence; do not retag an unverified build as final.
7. Participants attest eligibility/registration/one-entry, supply accurate contributions, record/review 2-3 minute final video (optional 60s cut), publish/tag/hashtag the actual demo, and nominate canonical URLs. The user alone submits the final form and retains confirmation under the standing instruction.

No social post, message to another person, final form or paid upgrade is authorized by this audit. Prisma v3/LLM/reopen/telephony/native app/streaming remain optional or excluded as originally specified.
