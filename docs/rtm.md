# Requirements traceability
All requirements retained; no fixture success counts as live evidence.

| ID | Requirement | Implementation/test/evidence status |
|---|---|---|
| O-01 | Enrolled student in India, age **18+** | docs/compliance.md; account/submission evidence pending |
| O-02 | Solo or team of **two** | docs/compliance.md; account/submission evidence pending |
| O-03 | One submission per person/team | docs/compliance.md; account/submission evidence pending |
| O-04 | Working app integrating **at least one genuine Gnani model/API** | Real local STT/TTS and durable browser workflow: docs/evidence/gnani-stt-live.md and browser/live-browser-smoke.json; hosted proof pending |
| O-05 | Explain title, problem, users, models/APIs, contributions | docs/compliance.md; account/submission evidence pending |
| O-06 | Public video showing application **working** | docs/compliance.md; account/submission evidence pending |
| O-07 | Include both **#GnaniAI** and **#GreatIndianAIInternshipChallenge**; tag Gnani AI | docs/compliance.md; account/submission evidence pending |
| O-08 | Nominate **one public post link per used platform** in submission | docs/compliance.md; account/submission evidence pending |
| O-09 | Submit video, explanation, technologies and post URLs in emailed form | docs/compliance.md; account/submission evidence pending |
| O-10 | Deadline **10 Nov 2026, 11:59 PM IST** | docs/compliance.md; account/submission evidence pending |
| O-11 | No bought engagement, bots, paid promotion, swaps, plagiarism, misleading demos | docs/compliance.md; account/submission evidence pending |
| O-12 | Use synthetic demo data, not real calls/phone/account/Aadhaar/PAN data | docs/compliance.md; account/submission evidence pending |
| FR-01 | Application boots from documented commands | api/app/db/models.py; app/seed.py; Alembic; integration/test_foundation.py; real PostgreSQL seed/health verified |
| FR-02 | Seed known sites/locations/assets/users | api/app/db/models.py; app/seed.py; Alembic; integration/test_foundation.py; real PostgreSQL seed/health verified |
| FR-03 | Role-restricted login/session | app/core/security.py; routers/auth.py; integration/test_workflow.py and test_intakes.py; role/IDOR/cookie/CSRF checks |
| FR-04 | Browser records audio with permission handling | web/src/pages/Report.tsx; app/services/audio.py; core/limits.py; test_intakes.py; file-fed MediaRecorder + real decoder verified, final human microphone capture pending |
| FR-05 | Server validates/normalizes audio | web/src/pages/Report.tsx; app/services/audio.py; core/limits.py; test_intakes.py; file-fed MediaRecorder + real decoder verified, final human microphone capture pending |
| FR-06 | Real Prisma request is made server-side | app/integrations/gnani.py; routers/intakes.py; contract/test_gnani.py; docs/evidence/gnani-stt-live.md and browser/live-browser-smoke.json; deployed smoke pending |
| FR-07 | Transcript is displayed and saved as received | app/integrations/gnani.py; routers/intakes.py; contract/test_gnani.py; docs/evidence/gnani-stt-live.md and browser/live-browser-smoke.json; deployed smoke pending |
| FR-08 | Gnani evidence is correlated | app/integrations/gnani.py; routers/intakes.py; contract/test_gnani.py; docs/evidence/gnani-stt-live.md and browser/live-browser-smoke.json; deployed smoke pending |
| FR-09 | STT errors handled without false success | app/integrations/gnani.py; routers/intakes.py; contract/test_gnani.py; docs/evidence/gnani-stt-live.md and browser/live-browser-smoke.json; deployed smoke pending |
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
| NFR-01 | Reliability | 87 local regression tests plus one genuine complete browser workflow; ten consecutive full voice runs not claimed |
| NFR-02 | Latency | Actual timing in live evidence; progress state; no fixed provider latency promise |
| NFR-03 | Correctness | PostgreSQL race/idempotency/version/atomicity tests; database constraints and triggers |
| NFR-04 | Security | Role/ownership/CSRF/cookie/upload/secret controls; dependency audits; no full pentest claim |
| NFR-05 | Privacy | Private keys/test audio; temporary decode cleanup; synthetic data; body-free logs |
| NFR-06 | Explainability | Original/corrected transcript, actual STT provenance and immutable event timeline |
| NFR-07 | Accessibility | Six axe WCAG desktop/mobile views with zero reported violations; browser/accessibility.json |
| NFR-08 | Reproducibility | Frozen uv/npm locks, README, migrations/seed, Docker/Render/CI artifacts |
| NFR-09 | Observability | Generated request IDs, body-free structured timings/errors and live/ready endpoints |
| NFR-10 | Fault isolation | STT failure cannot create order; TTS outage keeps saved order, verified |
| NFR-11 | Deployment | Docker/Render Blueprint schema verified; actual public HTTPS deployment and smoke pending |
| NFR-12 | Maintainability | Strict mypy/Ruff, TypeScript build and frontend lint/format; required GitHub quality gate |
| NFR-13 | Cost awareness | 25s UI/30s decode cap; per-user/global single-process limits; actual console balance remains operator-owned |
| NFR-14 | Honest representation | Test fixtures confined to tests; real local provider evidence; no deployed/form completion claim |
