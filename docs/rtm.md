Latest ownership update: production backup is handled by the participant and
completion is not yet confirmed. The agent completes automatic source publication,
protected merge, CI and local/main synchronization. Engineering and image rollback
are verified; live migration waits for backup confirmation. See
[current status](release-finalisation.md). Earlier checkpoint statements below retain their scope.

# Latest release finalisation traceability

The [current audit](evidence/improvement-finalisation-audit.json) supersedes the
previous checkpoint: 32 local passes, one explicit participant deferral and one
pending release gate. All 39 specification headings and 34 exact section-12 test
IDs are accounted for. 307 backend tests and the actual two-image rollback pass.
Both source CI runs pass; private backup and production approval remain pending; see
[release finalisation](release-finalisation.md). Historical evidence below is retained.

# Requirements traceability
All requirements retained; no fixture success counts as live evidence.

## November 15 local improvement traceability

Status: local candidate only; historical deployed results below remain historical.
The [release manifest](evidence/improvement-release.json) records executed gates.
All 34 planned test IDs are individually mapped in the
[completion audit](evidence/improvement-completion-audit.json): 30 local passes,
one deferred held-out evaluation and three blocked migration/release gates.

| Change | Requirement references | Actual tests / evidence |
|---|---|---|
| IMP-00 / T-IMP-001..002 | FR-03/06..09; NFR-04/05/08/12/14 | `unit/test_repository_guard.py`: 43 checks; [archive evidence](evidence/improvement-archive-check.json) |
| IMP-01 / T-IMP-010..012 | FR-06/08/19/20/25; NFR-06/07/08/14; O-04/05/10 | `integration/test_judge_access.py`, browser keyboard/empty/error/mobile checks; [judge evidence](evidence/improvement-judge.json) |
| IMP-02 / T-IMP-020..025 | FR-19/20/21/25; NFR-03/04/05/07/09 | `integration/test_queue_analytics.py` (>20, paging/filter/ACL/source/status/priority/null-duration), `test_queue_controls.py`, browser stable counts/refresh; [dashboard evidence](evidence/improvement-dashboard.json) |
| IMP-03 / T-IMP-030..036 | FR-07/10..15/18/25; NFR-03/06/07/14 | `unit/test_extraction_safety_assessment.py`, existing provenance/correction/roadmap tests, browser location/confirmation reset; [cached replay](evidence/improvement-extraction.json) |
| IMP-04A / T-IMP-040..042/044 | FR-06..12/14/15; NFR-01/02/03/06/09/13/14 | `unit/test_transcript_scoring.py`: 30 synthetic metric/manifest/privacy tests; [methodology](tests/offline-asr-methodology.md), [reference blocker](evidence/improvement-asr-development.json) |
| IMP-04B / T-IMP-043 | Same as IMP-04A | Deferred: no approved independent corpus/credit budget; no new recordings or genuine measurements |
| IMP-05 / T-IMP-050..056 | FR-03/06/09/23; NFR-01/04/05/09/10/13 | `integration/test_provider_admission.py`, `test_provider_pause.py`; unit budget/admission/login tests; [quota evidence](evidence/improvement-provider-budget.json). Production startup/readiness compatibility remains blocked |
| IMP-06 / T-IMP-060..063 | FR-01/03/06/09/15..25; NFR-01..14 | 295 backend tests; strict static/frontend gates, audits and Chrome fixture checks. Exact candidate CI, production migration/deploy/rollback and private backup remain unexecuted |

## Original requirement baseline and history

| ID | Requirement | Implementation/test/evidence status |
|---|---|---|
| O-01 | Enrolled student in India, age **18+** | docs/compliance.md; account/submission evidence pending |
| O-02 | Solo or team of **two** | docs/compliance.md; account/submission evidence pending |
| O-03 | One submission per person/team | docs/compliance.md; account/submission evidence pending |
| O-04 | Working app integrating **at least one genuine Gnani model/API** | Real local STT/TTS and durable browser workflow: docs/evidence/gnani-stt-live.md and browser/live-browser-smoke.json; hosted prerecorded STT/TTS/workflow verified in docs/evidence/hosted/; fresh human report verified; final public video pending |
| O-05 | Explain title, problem, users, models/APIs, contributions | docs/compliance.md; account/submission evidence pending |
| O-06 | Public video showing application **working** | docs/compliance.md; account/submission evidence pending |
| O-07 | Include both **#GnaniAI** and **#GreatIndianAIInternshipChallenge**; tag Gnani AI | docs/compliance.md; account/submission evidence pending |
| O-08 | Nominate **one public post link per used platform** in submission | docs/compliance.md; account/submission evidence pending |
| O-09 | Submit video, explanation, technologies and post URLs in emailed form | docs/compliance.md; account/submission evidence pending |
| O-10 | Deadline **15 Nov 2026, 18:00 IST** | [Official challenge](https://www.gnani.ai/internship), verified 14 Nov 2026; participant submission remains pending |
| O-11 | No bought engagement, bots, paid promotion, swaps, plagiarism, misleading demos | docs/compliance.md; account/submission evidence pending |
| O-12 | Use synthetic demo data, not real calls/phone/account/Aadhaar/PAN data | docs/compliance.md; account/submission evidence pending |
| FR-01 | Application boots from documented commands | api/app/db/models.py; app/seed.py; Alembic; integration/test_foundation.py; real PostgreSQL seed/health verified |
| FR-02 | Seed known sites/locations/assets/users | api/app/db/models.py; app/seed.py; Alembic; integration/test_foundation.py; real PostgreSQL seed/health verified |
| FR-03 | Role-restricted login/session | app/core/security.py; routers/auth.py; integration/test_workflow.py and test_intakes.py; role/IDOR/cookie/CSRF checks |
| FR-04 | Browser records audio with permission handling | web/src/pages/Report.tsx; app/services/audio.py; core/limits.py; test_intakes.py; file-fed MediaRecorder + real decoder verified, participant-attested fresh HTTPS Hindi microphone report and durable order verified in hosted/human-microphone-verification.json |
| FR-05 | Server validates/normalizes audio | web/src/pages/Report.tsx; app/services/audio.py; core/limits.py; test_intakes.py; file-fed MediaRecorder + real decoder verified, participant-attested fresh HTTPS Hindi microphone report and durable order verified in hosted/human-microphone-verification.json |
| FR-06 | Real Prisma request is made server-side | app/integrations/gnani.py; routers/intakes.py; contract/test_gnani.py; docs/evidence/gnani-stt-live.md and browser/live-browser-smoke.json; hosted prerecorded smoke verified in docs/evidence/hosted/; fresh human Hindi report independently read back with actual Gnani provenance; 15-recording Hindi/English/Hinglish development evaluation completed; Tamil unverified |
| FR-07 | Transcript is displayed and saved as received | app/integrations/gnani.py; routers/intakes.py; contract/test_gnani.py; docs/evidence/gnani-stt-live.md and browser/live-browser-smoke.json; hosted prerecorded smoke verified in docs/evidence/hosted/; fresh human Hindi report independently read back with actual Gnani provenance; 15-recording Hindi/English/Hinglish development evaluation completed; Tamil unverified |
| FR-08 | Gnani evidence is correlated | app/integrations/gnani.py; routers/intakes.py; contract/test_gnani.py; docs/evidence/gnani-stt-live.md and browser/live-browser-smoke.json; hosted prerecorded smoke verified in docs/evidence/hosted/; fresh human Hindi report independently read back with actual Gnani provenance; 15-recording Hindi/English/Hinglish development evaluation completed; Tamil unverified |
| FR-09 | STT errors handled without false success | app/integrations/gnani.py; routers/intakes.py; contract/test_gnani.py; docs/evidence/gnani-stt-live.md and browser/live-browser-smoke.json; hosted prerecorded smoke verified in docs/evidence/hosted/; fresh human Hindi report independently read back with actual Gnani provenance; 15-recording Hindi/English/Hinglish development evaluation completed; Tamil unverified |
| FR-10 | Extract asset and location from transcript | app/services/extraction.py; web/pages/Review.tsx; unit/test_extraction.py; docs/tests/evaluation.csv: 15/15 text fixtures, not ASR evaluation |
| FR-11 | Extract issue and urgency suggestion | app/services/extraction.py; web/pages/Review.tsx; unit/test_extraction.py; docs/tests/evaluation.csv: 15/15 text fixtures, not ASR evaluation |
| FR-12 | Provide explainable extraction evidence | app/services/extraction.py; web/pages/Review.tsx; unit/test_extraction.py; docs/tests/evaluation.csv: 15/15 text fixtures, not ASR evaluation |
| FR-13 | Worker corrects suggested fields | web/src/pages/Review.tsx; app/schemas/commands.py; services/orders.py; test_release_guards.py and test_workflow.py; explicit confirmation and correction separation verified |
| FR-14 | Require valid location, asset and description | web/src/pages/Review.tsx; app/schemas/commands.py; services/orders.py; test_release_guards.py and test_workflow.py; explicit confirmation and correction separation verified |
| FR-15 | Human confirmation required before ticket | web/src/pages/Review.tsx; app/schemas/commands.py; services/orders.py; test_release_guards.py and test_workflow.py; explicit confirmation and correction separation verified |
| FR-16 | Work order persists transactionally | services/orders.py; db/models.py; migration 0002; test_workflow.py; real concurrent/replay/ownership/immutability tests and browser refresh proof |
| FR-17 | Idempotent creation | services/orders.py; db/models.py; migration 0002; test_workflow.py; real concurrent/replay/ownership/immutability tests and browser refresh proof |
| FR-18 | Immutable audit events record transitions | services/orders.py; db/models.py; migration 0002; test_workflow.py; real concurrent/replay/ownership/immutability tests and browser refresh proof |
| FR-19 | Worker can view own tickets | services/orders.py; db/models.py; migration 0002; test_workflow.py; real concurrent/replay/ownership/immutability tests and browser refresh proof |
| FR-20 | Supervisor views/searches work-order queue | routers/orders.py; pages/Orders.tsx and Detail.tsx; test_workflow.py; actual browser assignment/start/resolution verified |
| FR-21 | Supervisor can assign and reprioritize | routers/orders.py; pages/Orders.tsx and Detail.tsx; test_workflow.py; actual browser assignment/start/resolution verified |
| FR-22 | State transitions are constrained | routers/orders.py; pages/Orders.tsx and Detail.tsx; test_workflow.py; actual browser assignment/start/resolution verified |
| FR-23 | Timbre speaks saved-ticket acknowledgment | integrations/tts.py; routers/orders.py; pages/Detail.tsx; contract/test_tts.py; test_release_guards.py; actual Timbre WAV plus outage isolation |
| FR-24 | Potential duplicates flagged | routers/intakes.py and orders.py; Review/Detail duplicate warnings; limited to reports user is authorized to see |
| FR-25 | Provenance page shows audit trail | services/orders.py detail serializer; Detail.tsx; immutable DB audit/provenance; browser details/timeline evidence |
| NFR-01 | Reliability | 190 backend tests and ten consecutive complete test-only-provider API workflows; genuine 15-recording development evaluation scored 12/15 with all safety cases blocked; ten consecutive genuine hosted workflows passed in evidence/hosted/reliability.json |
| NFR-02 | Latency | Actual timing in live evidence; progress state; no fixed provider latency promise |
| NFR-03 | Correctness | PostgreSQL race/idempotency/version/atomicity tests; database constraints and triggers |
| NFR-04 | Security | Role/ownership/CSRF/cookie/upload/secret controls; dependency audits; no full pentest claim |
| NFR-05 | Privacy | Private keys/test audio; temporary decode cleanup; synthetic data; body-free logs |
| NFR-06 | Explainability | Original/corrected transcript, actual STT provenance and immutable event timeline |
| NFR-07 | Accessibility | Six retained plus ten fixture-workflow axe/layout checks and deployed judge desktop/mobile checks; no reported violations in checked views |
| NFR-08 | Reproducibility | Frozen uv/npm locks, README, migrations/seed, Docker/Render/CI artifacts |
| NFR-09 | Observability | Generated request IDs, body-free structured timings/errors and live/ready endpoints |
| NFR-10 | Fault isolation | STT failure cannot create order; TTS outage keeps saved order, verified |
| NFR-11 | Deployment | Actual Render HTTPS app/DB, Blueprint GNANI, real prerecorded provider/browser workflow and restart verified; fresh human Hindi report verified; free-backup limitation remains |
| NFR-12 | Maintainability | Strict mypy/Ruff, TypeScript build and frontend lint/format; required GitHub quality gate |
| NFR-13 | Cost awareness | 25s UI/30s decode cap; local IMP-05 durable admission ledger; prior deployed RAM limits retained until staged rollout; actual balance remains operator-owned |
| NFR-14 | Honest representation | Test fixtures confined to tests; real local/hosted provider evidence plus one participant-attested fresh Hindi report with server provenance; 15-case development results disclosed with same-corpus limitations; no held-out benchmark, final-video or submitted-form claim |

## Current completion mapping

The [judge readiness record](evidence/judge-readiness.md) supersedes historical gap
notes in this matrix. FR-04..12 now include MANUAL_TEXT provenance, exact spans,
versioned extraction and actionable errors; FR-20..25 include all queue controls,
audited cancellation and restricted judge access. NFR-01/03/04/09 are additionally
covered by test_reliability.py, test_roadmap_regressions.py, test_judge_access.py,
test_stage_telemetry.py, tests/browser/workflow_check.py and repository_guard.py.
WBS-07.3 now has all 15 authentic participant clips evaluated with genuine Prisma;
12/15 complete cases and all six safety blocks are recorded in evidence/audio-evaluation.json.
English equivalents were approved for 04/10; Tamil remains unverified.

## Temporary demo operational closure ? 2026-11-10

NFR-11/WBS-07.7: actual compatible hosted app rollback and restoration passed, preserving all 12 report-detail hashes and approved judge access. NFR-13: user supplied actual-console balance observation; tested operator pause prevents new STT/TTS calls while saved/manual work remains available. WBS-07.8: immutable technical tag `demo-verified-2026-11-10` and scoped engineering signoff complete. [Evidence](evidence/demo-operational-release.json). Backups/DB expiry are explicitly user-managed; participant/publication/form tasks and Tamil remain outside this engineering scope.
