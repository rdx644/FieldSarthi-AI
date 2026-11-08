# Requirements traceability
All requirements retained; no fixture success counts as live evidence.

| ID | Requirement | Implementation/test/evidence status |
|---|---|---|
| O-01 | Enrolled student in India, age **18+** | docs/compliance.md; account/submission evidence pending |
| O-02 | Solo or team of **two** | docs/compliance.md; account/submission evidence pending |
| O-03 | One submission per person/team | docs/compliance.md; account/submission evidence pending |
| O-04 | Working app integrating **at least one genuine Gnani model/API** | docs/compliance.md; account/submission evidence pending |
| O-05 | Explain title, problem, users, models/APIs, contributions | docs/compliance.md; account/submission evidence pending |
| O-06 | Public video showing application **working** | docs/compliance.md; account/submission evidence pending |
| O-07 | Include both **#GnaniAI** and **#GreatIndianAIInternshipChallenge**; tag Gnani AI | docs/compliance.md; account/submission evidence pending |
| O-08 | Nominate **one public post link per used platform** in submission | docs/compliance.md; account/submission evidence pending |
| O-09 | Submit video, explanation, technologies and post URLs in emailed form | docs/compliance.md; account/submission evidence pending |
| O-10 | Deadline **10 Nov 2026, 11:59 PM IST** | docs/compliance.md; account/submission evidence pending |
| O-11 | No bought engagement, bots, paid promotion, swaps, plagiarism, misleading demos | docs/compliance.md; account/submission evidence pending |
| O-12 | Use synthetic demo data, not real calls/phone/account/Aadhaar/PAN data | docs/compliance.md; account/submission evidence pending |
| FR-01 | Application boots from documented commands | Planned; see docs/roadmap.md; not implemented/tested |
| FR-02 | Seed known sites/locations/assets/users | Planned; see docs/roadmap.md; not implemented/tested |
| FR-03 | Role-restricted login/session | Planned; see docs/roadmap.md; not implemented/tested |
| FR-04 | Browser records audio with permission handling | Planned; see docs/roadmap.md; not implemented/tested |
| FR-05 | Server validates/normalizes audio | Planned; see docs/roadmap.md; not implemented/tested |
| FR-06 | Real Prisma request is made server-side | api/app/integrations/gnani.py; tests/contract/test_gnani.py; genuine local cURL/HTTPX proof: docs/evidence/gnani-stt-live.md; deployed proof pending |
| FR-07 | Transcript is displayed and saved as received | api/app/integrations/gnani.py; tests/contract/test_gnani.py; genuine local cURL/HTTPX proof: docs/evidence/gnani-stt-live.md; deployed proof pending |
| FR-08 | Gnani evidence is correlated | api/app/integrations/gnani.py; tests/contract/test_gnani.py; genuine local cURL/HTTPX proof: docs/evidence/gnani-stt-live.md; deployed proof pending |
| FR-09 | STT errors handled without false success | api/app/integrations/gnani.py; tests/contract/test_gnani.py; genuine local cURL/HTTPX proof: docs/evidence/gnani-stt-live.md; deployed proof pending |
| FR-10 | Extract asset and location from transcript | Planned; see docs/roadmap.md; not implemented/tested |
| FR-11 | Extract issue and urgency suggestion | Planned; see docs/roadmap.md; not implemented/tested |
| FR-12 | Provide explainable extraction evidence | Planned; see docs/roadmap.md; not implemented/tested |
| FR-13 | Worker corrects suggested fields | Planned; see docs/roadmap.md; not implemented/tested |
| FR-14 | Require valid location, asset and description | Planned; see docs/roadmap.md; not implemented/tested |
| FR-15 | Human confirmation required before ticket | Planned; see docs/roadmap.md; not implemented/tested |
| FR-16 | Work order persists transactionally | Planned; see docs/roadmap.md; not implemented/tested |
| FR-17 | Idempotent creation | Planned; see docs/roadmap.md; not implemented/tested |
| FR-18 | Immutable audit events record transitions | Planned; see docs/roadmap.md; not implemented/tested |
| FR-19 | Worker can view own tickets | Planned; see docs/roadmap.md; not implemented/tested |
| FR-20 | Supervisor views/searches work-order queue | Planned; see docs/roadmap.md; not implemented/tested |
| FR-21 | Supervisor can assign and reprioritize | Planned; see docs/roadmap.md; not implemented/tested |
| FR-22 | State transitions are constrained | Planned; see docs/roadmap.md; not implemented/tested |
| FR-23 | Timbre speaks saved-ticket acknowledgment | Planned; see docs/roadmap.md; not implemented/tested |
| FR-24 | Potential duplicates flagged | Planned; see docs/roadmap.md; not implemented/tested |
| FR-25 | Provenance page shows audit trail | Planned; see docs/roadmap.md; not implemented/tested |
| NFR-01 | Reliability | Planned; see docs/roadmap.md; not implemented/tested |
| NFR-02 | Latency | Planned; see docs/roadmap.md; not implemented/tested |
| NFR-03 | Correctness | Planned; see docs/roadmap.md; not implemented/tested |
| NFR-04 | Security | Partial WBS-01 controls; docs/security.md, README; full-system verification pending |
| NFR-05 | Privacy | Partial WBS-01 controls; docs/security.md, README; full-system verification pending |
| NFR-06 | Explainability | Planned; see docs/roadmap.md; not implemented/tested |
| NFR-07 | Accessibility | Planned; see docs/roadmap.md; not implemented/tested |
| NFR-08 | Reproducibility | Partial WBS-01 controls; docs/security.md, README; full-system verification pending |
| NFR-09 | Observability | Partial WBS-01 controls; docs/security.md, README; full-system verification pending |
| NFR-10 | Fault isolation | Partial WBS-01 controls; docs/security.md, README; full-system verification pending |
| NFR-11 | Deployment | Planned; see docs/roadmap.md; not implemented/tested |
| NFR-12 | Maintainability | Planned; see docs/roadmap.md; not implemented/tested |
| NFR-13 | Cost awareness | Partial WBS-01 controls; docs/security.md, README; full-system verification pending |
| NFR-14 | Honest representation | Partial WBS-01 controls; docs/security.md, README; full-system verification pending |
