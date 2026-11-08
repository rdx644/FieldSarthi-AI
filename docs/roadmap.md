# FieldSaarthi AI — End-to-End Traceable Implementation Roadmap

**Project:** FieldSaarthi AI — Multilingual Voice-to-Action Intelligence for Field Operations  
**Challenge:** Gnani AI — Great Indian AI Internship Challenge 2026  
**Document version:** 1.0 | **Prepared:** 08 November 2026 (IST)  
**Submission cutoff:** **10 November 2026, 11:59 PM IST**  
**Build strategy:** Gnani-first, vertical-slice delivery, evidence-based release gates  
**Owners:** Solo developer or two-person team (maximum permitted team size: 2)

> **Read first:** This is an implementation specification and execution plan, **not a claim that an app has already been built or tested**. Items marked **[OFFICIAL]** are requirements from the linked Gnani sources. Items marked **[DESIGN]** are recommended implementation decisions. Items marked **[GATE]** must pass before claiming completion. Proposed quality targets are **not** official contest judging scores. Do not substitute simulated transcripts or stock audio for a claimed live Gnani integration.

---

## 0. Executive decision and success definition

### 0.1 Product in one sentence

**FieldSaarthi turns a worker's Hindi/English/Tamil voice report into a validated, auditable maintenance work order that a supervisor can assign and resolve, using a genuine Gnani Prisma speech-to-text request and optionally a Gnani Timbre spoken acknowledgment.**

### 0.2 The minimum qualifying working demonstration

1. A worker logs in and records a short, newly spoken fault report.
2. The frontend uploads **real microphone audio** to the application's backend.
3. The backend calls **Gnani Prisma**, receives an authentic transcript, and retains nonsecret model/request metadata.
4. The system extracts a probable location, asset, issue category and urgency cue from that **actual transcript**.
5. The worker reviews, edits and confirms; incomplete/ambiguous facts cannot silently become authoritative records.
6. The backend creates **exactly one durable work order** and returns a real ID.
7. A supervisor can assign it, advance its state and view the persisted history after a page refresh.
8. If implemented and verified, Gnani Timbre synthesizes a spoken success acknowledgment; TTS failure must not undo a saved work order.
9. The publicly posted demo shows this real flow, followed by completion of Gnani's official submission form.

**Definition of done:** the chain `fresh microphone recording → authentic Gnani response → reviewed structured data → durable database write → supervisor action → verifiable evidence` works end to end in the deployed or reproducibly runnable application. A frontend-only prototype, hard-coded transcript, fake response, or manual-only mode **does not** satisfy this definition.

### 0.3 Primary differentiator

The product closes the loop from **speech to an accountable enterprise action**. It exposes what was heard, how the report was interpreted, what a human corrected, what was finally written, and who changed its status. This is more credible than a standalone speech transcription or generic chatbot.

### 0.4 Outcome metrics (proposed engineering targets, not Gnani scoring)

| Metric ID | Target for demo build | Measurement/evidence |
|---|---|---|
| KPI-01 | 100% of claimed live voice reports invoke Gnani STT | Correlated server request metadata and recorded test evidence |
| KPI-02 | At least 12/15 scripted extraction cases have all required fields correct after rule/parser stage | Ground-truth evaluation CSV, pass/fail script |
| KPI-03 | 100% of missing/unknown asset or location cases require human correction | Negative tests |
| KPI-04 | A repeated submission with the same idempotency key creates exactly one ticket | DB assertion |
| KPI-05 | Complete successful workflow remains persisted after refresh | E2E test + screen capture |
| KPI-06 | STT/TTS failure never becomes an invented success | Fault-injection tests |
| KPI-07 | No API keys, real personal data or raw audio in public Git history | Secret and content scan |
| KPI-08 | One complete 60-second public demo published with the required hashtags | Public URL + publication check |

---

## 1. Official challenge compliance — no-invalidation controls

Verify these instructions at submission time; the programme terms and registration page remain authoritative.

| Compliance ID | Verified official requirement | Action/evidence | Failure prevention |
|---|---|---|---|
| O-01 | Enrolled student in India, age **18+** | Confirm eligibility and registration | Do not claim entry if ineligible |
| O-02 | Solo or team of **two** | One registrant; add teammate email if applicable | No unregistered third participant |
| O-03 | One submission per person/team | Maintain one final project entry | No duplicate entries |
| O-04 | Working app integrating **at least one genuine Gnani model/API** | Capture authentic STT request, model, request ID, result | Reject demo builds that fake Gnani output |
| O-05 | Explain title, problem, users, models/APIs, contributions | Prepare final project summary | Use precise implementation claims |
| O-06 | Public video showing application **working** | Post on LinkedIn, X, or both | Test visible functionality before recording |
| O-07 | Include both **#GnaniAI** and **#GreatIndianAIInternshipChallenge**; tag Gnani AI | Check post before publication | Do not rely on tag alone |
| O-08 | Nominate **one public post link per used platform** in submission | Copy canonical post URL(s) to form | Posting is not submitting |
| O-09 | Submit video, explanation, technologies and post URLs in emailed form | Capture confirmation before cutoff | Treat email submission form as authoritative |
| O-10 | Deadline **10 Nov 2026, 11:59 PM IST** | Submit early with buffer | No extension assumption |
| O-11 | No bought engagement, bots, paid promotion, swaps, plagiarism, misleading demos | Organic promotion and truthful demo | Avoid disqualification |
| O-12 | Use synthetic demo data, not real calls/phone/account/Aadhaar/PAN data | Seed fake workers, assets, locations | Avoid unnecessary privacy exposure |

**Selection model:** Verified public engagement is used for internship interview shortlisting among eligible projects; individual skills/interviews determine offers. Awards are separate. No project architecture can guarantee selection. The relevant award angles for this project are **Real Deal** (real-world usefulness), **Mixed Vibes** (only if code-mixed speech is actually demonstrated), and **Demo Day Drop** (strong 60-second video). Do not claim eligibility for an award category merely by naming it.

**Official source links:**
- Challenge and rules: https://www.gnani.ai/internship
- Registration and terms: https://www.gnani.ai/great-indian-ai-internship-registration-form
- Gnani API console: https://app.gnani.ai/voice
- Developer quick start: https://docs.gnani.ai/api/introduction/quick-start

**Important distinction:** The challenge page highlights Prisma v2.5 and Timbre v2.5. Current Gnani API docs also describe v3.0 versions. Build against **Prisma v2.5** as the proven project baseline; consider v3.0 only if your programme account authorizes it and a live acceptance test passes. Do **not** assume newer model access or claim v3.0 was used without evidence. Agent Builder is outside the challenge API platform. Evon weights require separate hosting and are **not a dependency**.

---

## 2. Product charter and operating assumptions

### 2.1 Problem statement

Field technicians in Indian facilities often communicate faults through informal calls, voice notes or word of mouth. Supervisors must manually translate unstructured speech into actionable assignments. This loses asset/location context, encourages duplicate reports and makes accountability difficult.

### 2.2 Target personas

| Persona | Main goal | App permissions |
|---|---|---|
| Worker / reporter | Report a problem quickly in a familiar language, correct the transcript, track own issues | Record, preview, confirm, create; view own tickets |
| Supervisor / dispatcher | Triage, assign and track maintenance work | View all tickets in demo organization, assign, set priority, update state |
| Admin (seed/setup only) | Manage known assets, locations and demo accounts | Seed maintenance master data; not a complex UI for MVP |
| Evaluator / interviewer | Verify real model integration, reliability and engineering decisions | Observe demo or test with a restricted demo user |

### 2.3 Realistic example

A worker says: **“Block B second floor ka water pump leak ho raha hai, urgent repair chahiye.”** The frontend displays Gnani's actual transcript. The parser proposes: `asset=Water Pump B-02`, `location=Block B / Floor 2`, `issue=LEAKAGE`, `priority_suggestion=HIGH`; the reporter confirms. A supervisor sees work order `WO-...`, assigns it and marks `IN_PROGRESS`, later `RESOLVED`.

**Safety rule:** “urgent” is a reported cue, **not** an authoritative safety diagnosis. The app may suggest priority, but the supervisor owns final triage. For possible electrical/fire/gas or immediate danger, prominently advise following the organization's emergency protocol; do not position the product as emergency response infrastructure.

### 2.4 Locked assumptions to avoid overengineering

- **One seeded demo organization** with small master inventory; no full multi-tenant SaaS, billing or onboarding.
- One short report per request; **recording target ≤25 seconds** to remain inside Gnani's **30-second REST limit**.
- Selected `hi-IN`, `en-IN`, or `ta-IN` per Prisma v2.5 request; don't claim automatic cross-language detection on v2.5.
- Audio processed in memory or temporary server disk, converted as needed, then deleted; **no long-lived raw audio storage** in MVP.
- **Hindi/Hinglish first** for polished demonstration; English and Tamil added only once each tested with authentic audio.
- Deterministic, inspectable extraction from a small approved asset/location inventory; an optional LLM is a secondary improvement, never a source of unverified facts.
- Supervisors are simulated with explicitly seeded **synthetic** identities and plausible maintenance assets.
- Backend API and PostgreSQL remain authoritative; browser state is never the system of record.

### 2.5 Explicit non-goals for the November 10 build

No WhatsApp or PSTN telephony integration; no native Android app; no unbounded audio streaming pipeline; no custom ASR training; no Kubernetes; no real industrial PLC/IoT control; no incident auto-dispatch without human confirmation; no autonomous emergency decisions; no complex RAG/agent orchestration; no production-grade enterprise SSO; no external customer data. Add these to a future roadmap, not the deadline-critical path.

---

## 3. Scope backlog with traceable priorities

**P0 = submission-critical**, **P1 = showcase differentiation**, **P2 = future extension**. Implement P0 in the listed dependency order; do not let P1 block P0.

| Epic | Work item | Priority | Requirement IDs |
|---|---|---|---|
| E1 Foundation | Repository, env, CI, database, synthetic seed | P0 | FR-01, FR-02, NFR-08 |
| E2 Identity | Seeded worker/supervisor authentication, RBAC | P0 | FR-03, NFR-04 |
| E3 Audio capture | Browser recorder, upload limits, format conversion | P0 | FR-04, FR-05 |
| E4 Gnani STT | Live backend Prisma call, transcript + metadata, error mapping | **P0, critical dependency** | FR-06–FR-09 |
| E5 Voice-to-action | Asset/location/issue extraction and evidence display | P0 | FR-10–FR-12 |
| E6 Verification | Editable transcript/fields, blocking validation | P0 | FR-13–FR-15 |
| E7 Orders | Transactional creation, idempotency, state machine, event log | P0 | FR-16–FR-19 |
| E8 Supervisor | Assignment, triage, dashboard, workflow | P0 | FR-20–FR-22 |
| E9 Gnani TTS | Spoken confirmation, optional and non-blocking | P1 | FR-23 |
| E10 Trust | Duplicate warning, provenance/audit display | P1 | FR-24–FR-25 |
| E11 Quality | E2E, negative scenarios, deployment, monitor | P0 | NFR-01–NFR-12 |
| E12 Showcase | Public demo, explanatory material, submission form | **P0** | O-04–O-10 |
| E13 Advanced | Optional Prisma v3 comparison, richer code-mix, telemetry analytics | P2 | EXP-01 |

### 3.1 Functional requirements and acceptance conditions

| ID | Requirement | Testable acceptance condition | Main owner |
|---|---|---|---|
| FR-01 | Application boots from documented commands | Fresh clone passes local smoke test | Backend |
| FR-02 | Seed known sites/locations/assets/users | At least two locations, three assets, two roles are usable | Backend |
| FR-03 | Role-restricted login/session | Worker cannot access supervisor-only actions | Full-stack |
| FR-04 | Browser records audio with permission handling | Permission denied produces guidance; permitted recording uploads | Frontend |
| FR-05 | Server validates/normalizes audio | Unsupported, empty, >30s rejected; accepted input converts to allowed format | Backend |
| FR-06 | Real Prisma request is made server-side | Test succeeds against Gnani, not mock, and model shown accurately | Backend |
| FR-07 | Transcript is displayed and saved as received | `raw_transcript` is preserved unchanged in intake record | Full-stack |
| FR-08 | Gnani evidence is correlated | `model`, `request_id`, duration/latency when provided captured | Backend |
| FR-09 | STT errors handled without false success | 401/402/403/429/5xx mapped to clear retry/support statuses | Backend |
| FR-10 | Extract asset and location from transcript | Match only seeded aliases; unsupported match remains unresolved | Backend |
| FR-11 | Extract issue and urgency suggestion | Explicit cues map to enumerated types; ambiguous text flagged | Backend |
| FR-12 | Provide explainable extraction evidence | UI shows recognized phrases and unresolved fields | Full-stack |
| FR-13 | Worker corrects suggested fields | Corrections visible and logged separately from model transcript | Frontend |
| FR-14 | Require valid location, asset and description | Invalid/unknown or cross-location asset cannot be confirmed | Backend |
| FR-15 | Human confirmation required before ticket | No `work_orders` row before explicit confirmation | Backend |
| FR-16 | Work order persists transactionally | Valid confirmed intake creates one durable order | Backend |
| FR-17 | Idempotent creation | Repeated same key/body returns same ID; conflicting body => 409 | Backend |
| FR-18 | Immutable audit events record transitions | Every creation/assignment/status change has timestamp/actor | Backend |
| FR-19 | Worker can view own tickets | Other worker's tickets inaccessible | Full-stack |
| FR-20 | Supervisor views/searches work-order queue | Queue displays correct status, priority, location, assignee | Full-stack |
| FR-21 | Supervisor can assign and reprioritize | Saved update visible after refresh | Full-stack |
| FR-22 | State transitions are constrained | Invalid transitions denied; optimistic lock blocks stale update | Backend |
| FR-23 | Timbre speaks saved-ticket acknowledgment | Real binary WAV returned; ticket stays saved on TTS failure | Full-stack |
| FR-24 | Potential duplicates flagged | Existing open same-asset report generates warning | Backend |
| FR-25 | Provenance page shows audit trail | Raw transcript, corrections, model and request ID can be inspected | Full-stack |

### 3.2 Nonfunctional requirements (engineering acceptance targets)

| ID | Requirement | Proposed test / threshold |
|---|---|---|
| NFR-01 | Reliability | 10 consecutive end-to-end happy paths in test/staging without unhandled exception (subject to upstream availability) |
| NFR-02 | Latency | Measure end-to-end STT time; display progress; don't promise fixed Gnani inference latency |
| NFR-03 | Correctness | DB constraints, idempotency, transaction atomicity verified |
| NFR-04 | Security | Server-side secret only, RBAC, safe upload parsing, input validation |
| NFR-05 | Privacy | Synthetic data; ephemeral audio; no raw transcript/PII in routine logs |
| NFR-06 | Explainability | Every created ticket linked to intake and Gnani provenance |
| NFR-07 | Accessibility | Keyboard navigation, labels, high-contrast states, visible text confirmation |
| NFR-08 | Reproducibility | README, pinned dependencies/lockfile, migrations, seed script |
| NFR-09 | Observability | Correlation ID, structured error types, stage timings and uptime endpoint |
| NFR-10 | Fault isolation | STT failure blocks claim of completed voice report; TTS failure never rolls back ticket |
| NFR-11 | Deployment | HTTPS frontend; live API; durable PostgreSQL; microphone permission works |
| NFR-12 | Maintainability | Typed backend and frontend, separated layers, lint/tests in CI |
| NFR-13 | Cost awareness | Limited recording duration, request concurrency, budget monitoring |
| NFR-14 | Honest representation | Mock fixtures in tests only; production UI distinguishes demo data and live integration |

### 3.3 Requirement-to-evidence traceability matrix (RTM)

| Requirement group | Implementation artifact | Tests | Gate evidence |
|---|---|---|---|
| FR-04–05 / NFR-05 | `web/src/features/voice/*`, `api/app/services/audio.py` | T-AUD-01…05 | Valid short recording, unsupported audio rejection |
| FR-06–09 / O-04 | `api/app/integrations/gnani.py` | T-STT-01…07, T-LIVE-01 | Real provider request ID/model in log + UI |
| FR-10–12 | `api/app/services/extraction.py` | T-NLP-01…15 | Ground-truth comparison report |
| FR-13–15 | `web/src/features/intakes/*`, `api/app/services/validation.py` | T-VAL-01…06 | Missing asset blocks confirmation |
| FR-16–19 | `api/app/services/orders.py`, migrations | T-ORD-01…08 | DB data and atomic audit events |
| FR-20–22 | `web/src/features/operations/*` | T-RBAC-01…04, T-WF-01…05 | Supervisor state transition demo |
| FR-23 | `api/app/integrations/gnani.py` TTS adapter | T-TTS-01…04 | WAV from Gnani; saved ticket survives TTS error |
| FR-24–25 | `api/app/services/duplicates.py`, audit UI | T-DUP-01…03, T-AUDIT-01…03 | Warning and provenance screen |
| NFR-01–14 | `tests/`, CI, deployment config | T-E2E, T-SEC, T-OPS | Test report, clean checks, deployment smoke |
| O-05–10 | `docs/submission/`, public social posts | T-SUB-01…07 | Video link, post URL, official confirmation |

**Traceability rule:** Every work item/PR references `FR`, `NFR` or `O` IDs; every requirement links to a test and a verifiable artifact. No “done” labels without test evidence.

---

## 4. Lightweight CMMI-inspired delivery process (not certification)

**CMMI is not required by Gnani.** Use the practical disciplines behind CMMI to organize this short build; **do not claim CMMI certification or compliance**. A heavy formal assessment would be counterproductive before the deadline.

| CMMI-inspired discipline | Lightweight artifact | Cadence / enforcement |
|---|---|---|
| Requirements Management (REQM) | Versioned requirements in this file, RTM | Each feature and PR links to an ID |
| Project Planning (PP) | Scope P0/P1/P2, timeboxes, owners, critical path | Re-plan daily at a fixed checkpoint |
| Project Monitoring & Control (PMC) | Kanban board, blockers, burn-down of P0 | Daily 15-minute review |
| Configuration Management (CM) | Git main + feature branches, tagged release, locked dependencies | Review every change; release tags |
| Process & Product Quality Assurance (PPQA) | DoD checklist, lint/test/security checks | CI on each PR |
| Verification (VER) | Unit/integration/contract tests | Before merge |
| Validation (VAL) | Genuine voice-to-ticket task tested with real user script | Before demo/publication |
| Measurement & Analysis (MA) | STT success rate, latency, extraction accuracy, failure counts | Review after each E2E run |
| Risk Management (RSKM) | Risk register with triggers, mitigations and owners | Review daily; blocker escalation |
| Decision Analysis (DAR), selectively | Short ADR files for architecture and model choice | Only for high-impact changes |

### 4.1 Project lifecycle / release gates

```mermaid
flowchart LR
    A[Gate G0: Requirements and access] --> B[Gate G1: Real Gnani STT spike]
    B --> C[Gate G2: Voice-to-ticket vertical slice]
    C --> D[Gate G3: Reliability and security]
    D --> E[Gate G4: Recorded public demo]
    E --> F[Gate G5: Official submission]
```

| Gate | Must be true | Required evidence | Stop/rework condition |
|---|---|---|---|
| G0 | Registered; key accessible; scope frozen; repo running | Registration/access confirmation, baseline commit | No API key or unapproved scope |
| G1 | Genuine Prisma call succeeds from backend | Real request ID, returned model, transcript | Provider unavailable/unauthorized; **do not fake** |
| G2 | Confirmed voice report becomes durable work order | DB row and audit event; visible dashboard | Any broken core path |
| G3 | Negative cases, auth, retries, E2E tests pass | Reports and CI run | Critical/High severity open defects |
| G4 | Public demo accurately shows functionality | 60s recording, public post URL | Misleading demonstration/secret exposure |
| G5 | Official form completed correctly and on time | Submission confirmation / saved proof | Missing nomination URL or form completion |

### 4.2 Development standards and branch policy

- Branch naming: `feat/FR-06-gnani-stt`, `fix/FR-17-idempotency`, `test/NFR-04-upload-security`.
- Commit format: `feat(FR-06): add genuine Prisma STT adapter`.
- PR checklist: requirement ID → implementation → tests → evidence → security/privacy impact → rollback note.
- Never merge failing CI or broken P0 functionality into `main`.
- Save release evidence under `docs/evidence/`, **excluding credentials and raw user audio**.
- Tag verified build `v1.0.0-submission` and record commit SHA in submission notes.
- If using AI coding agents/Codex: agent-created code still requires human review, real tests, and production/release-gate approval.

### 4.3 Definition of Ready (DoR) / Done (DoD)

**DoR:** requirement ID, actor, inputs/outputs, acceptance test, affected components, dependencies, known risks.  
**DoD:** code merged, type/lint pass, relevant unit/contract tests pass, negative path tested, provenance and auth validated, README updated if interface changed, evidence captured, no secret leak.

---

## 5. Architecture and authoritative data flow

### 5.1 Architecture diagram

```mermaid
flowchart TB
  Worker[Worker browser - microphone] -->|HTTPS auth + audio| API[FastAPI Backend]
  Supervisor[Supervisor browser - queue] -->|HTTPS auth + actions| API
  API --> Audio[Audio validation and conversion]
  Audio --> GnaniSTT[Gnani Prisma STT API]
  GnaniSTT -->|transcript + request_id + model| Intake[Report intake + extraction]
  Intake --> Catalog[Seeded location and asset catalog]
  Catalog --> Validate[Server-side schema + human confirmation]
  Validate --> Orders[Transactional Work Order Service]
  Orders --> DB[(PostgreSQL)]
  Orders --> Event[Immutable audit events]
  Event --> DB
  Orders -->|if enabled, after commit| TTS[Gnani Timbre TTS API]
  TTS -->|audio/wav, non-critical| Worker
  API --> Logs[Redacted structured logs / timings]
```

### 5.2 Trust boundaries and system ownership

- **Untrusted:** browser inputs, audio uploads, recognized transcript, extracted fields, user-provided idempotency headers.
- **Trusted after authentication and validation:** role claims verified server-side, known asset/location IDs, transition rules, DB write constraints.
- **Third party:** Gnani APIs; never expose `X-API-Key-ID` to browser or public logs; handle transient failures and quotas.
- **Authoritative facts:** backend and DB, not LLM output or frontend-generated JSON.
- **Provenance invariant:** `raw_transcript` is never rewritten when the worker corrects text; keep `edited_transcript` or correction event separately.
- **No hidden substitution:** if a manual text-entry fallback exists, label it `MANUAL`, not `GNANI_STT`; exclude it from claimed live Gnani demonstrations.

### 5.3 Sequence of a valid report

```mermaid
sequenceDiagram
    actor W as Worker
    participant UI as React UI
    participant API as FastAPI
    participant G as Gnani Prisma
    participant DB as PostgreSQL
    actor S as Supervisor
    participant T as Gnani Timbre
    W->>UI: Record and submit audio
    UI->>API: POST /v1/intakes/transcribe (audio + language)
    API->>API: Validate, convert, duration check
    API->>G: POST /stt/v3 with API key
    G-->>API: transcript, model, request_id
    API->>DB: Save intake + provider metadata
    API-->>UI: Intake + transcript + proposed fields
    W->>UI: Review/correct and confirm
    UI->>API: POST /v1/work-orders with intake + idempotency key
    API->>DB: Validate + transactionally create order and audit event
    DB-->>API: Committed order ID
    API-->>UI: 201 Created / existing ID on replay
    opt Optional separate action
       UI->>API: GET/POST acknowledgment audio
       API->>T: TTS request
       T-->>API: WAV bytes
       API-->>UI: Audio playback
    end
    S->>UI: Assign/update work order
    UI->>API: PATCH /v1/work-orders/:id/status
    API->>DB: Check role, transition, version + audit transaction
    API-->>UI: New state and version
```

### 5.4 State machines

**Intake:** `RECORDING → UPLOADING → TRANSCRIBING → READY_FOR_REVIEW → CONFIRMED` or `FAILED / DISCARDED`. A failed transcription cannot become a confirmed Gnani intake.  
**Work order:** `OPEN → ASSIGNED → IN_PROGRESS → RESOLVED`; `OPEN/ASSIGNED/IN_PROGRESS → CANCELLED` when justified by supervisor; optional `RESOLVED → REOPENED → ASSIGNED` (only if implemented and tested; otherwise remove). All transitions are validated on the server and logged. No direct `OPEN → RESOLVED` shortcut in the default policy.

### 5.5 Architecture Decision Records (ADRs)

| ADR | Decision | Why | Reconsider when |
|---|---|---|---|
| ADR-001 | React + Vite + TypeScript frontend | Fast responsive build; simple UI separation | Existing approved app foundation is better |
| ADR-002 | FastAPI + Pydantic backend | Typed contracts and quick Python integration | Team has already validated a stronger backend |
| ADR-003 | PostgreSQL, migrations, transaction boundaries | Durable relational state and strong constraints | Prototype only, but cannot sacrifice persistence |
| ADR-004 | REST STT for ≤30s clips | Easiest reliable vertical slice | Core system complete; streaming actually required |
| ADR-005 | Prisma v2.5 baseline + model metadata | Matches challenge's highlighted model and documented default | v3.0 access and regression tests both pass |
| ADR-006 | Rule/alias parser + human verification | Testable, explainable, prevents hallucinated asset IDs | Larger real catalog, sufficient evaluation data |
| ADR-007 | TTS independent of ticket transaction | Avoid provider failure breaking saved business outcome | Always optional, even if operationally promoted |
| ADR-008 | Synthetic demo data only | Minimizes privacy/security risks | Approved data processing regime exists |

---

## 6. Technology baseline and repository layout

### 6.1 Pinned build choices

| Concern | Recommended choice |
|---|---|
| Web | React, Vite, TypeScript, Tailwind CSS, React Router, React Query or equivalent |
| API | Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2, Alembic, HTTPX |
| Storage | PostgreSQL (managed instance for deployed build) |
| Audio | Browser `MediaRecorder`; server `ffprobe` + `ffmpeg` where necessary |
| STT | Gnani Prisma v2.5 via REST `POST /stt/v3` |
| TTS | Optional Gnani Timbre v2.5 via REST inference endpoint |
| Tests | Pytest, pytest-asyncio, HTTPX test client, Playwright, Vitest |
| QA/CI | GitHub Actions lint/typecheck/unit/contract/E2E, optional dependency scan |
| Hosting | HTTPS static frontend host + Python API service + durable managed PostgreSQL |
| Monitoring | JSON logs, correlation IDs, API health/readiness and basic timing gauges |

**Dependency discipline:** pin lockfiles; choose compatible releases already available in the environment; don't blindly upgrade dependencies on deadline day.

### 6.2 Proposed monorepo tree

```text
fieldsaarthi-ai/
├── README.md
├── LICENSE                          # choose a license only if intended
├── .gitignore
├── .env.example                     # no secrets
├── docker-compose.yml               # local db + API optional
├── .github/
│   └── workflows/ci.yml
├── docs/
│   ├── architecture.md
│   ├── requirements.md                # or reference this roadmap
│   ├── rtm.md
│   ├── adrs/ADR-001.md ...
│   ├── risks.md
│   ├── tests/evaluation.csv
│   ├── evidence/                     # redacted screenshots, output summaries
│   └── submission/
│       ├── project-summary.md
│       ├── demo-script.md
│       └── final-checklist.md
├── api/
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── alembic/versions/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/config.py
│   │   ├── core/security.py
│   │   ├── db/session.py
│   │   ├── db/models.py
│   │   ├── schemas/auth.py
│   │   ├── schemas/intakes.py
│   │   ├── schemas/orders.py
│   │   ├── routers/auth.py
│   │   ├── routers/intakes.py
│   │   ├── routers/orders.py
│   │   ├── routers/assets.py
│   │   ├── integrations/gnani.py
│   │   ├── services/audio.py
│   │   ├── services/extraction.py
│   │   ├── services/validation.py
│   │   ├── services/orders.py
│   │   ├── services/duplicates.py
│   │   ├── services/acknowledgment.py
│   │   └── observability/logging.py
│   ├── scripts/seed_demo.py
│   └── tests/
│       ├── unit/
│       ├── integration/
│       ├── contract/
│       └── live/                      # explicit opt-in live Gnani tests
└── web/
    ├── package.json
    ├── package-lock.json
    ├── index.html
    ├── src/
    │   ├── app/router.tsx
    │   ├── lib/api.ts
    │   ├── lib/auth.ts
    │   ├── components/
    │   ├── features/voice/
    │   ├── features/intakes/
    │   ├── features/orders/
    │   ├── features/operations/
    │   ├── pages/LoginPage.tsx
    │   ├── pages/ReportPage.tsx
    │   ├── pages/MyTicketsPage.tsx
    │   ├── pages/SupervisorPage.tsx
    │   └── pages/TicketDetailPage.tsx
    └── tests/
```

### 6.3 Configuration contract (`.env.example`)

```dotenv
APP_ENV=development
APP_NAME=FieldSaarthi AI
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/fieldsaarthi
JWT_SECRET=REPLACE_WITH_RANDOM_SECRET
JWT_ACCESS_TTL_MINUTES=30
CORS_ORIGINS=http://localhost:5173
GNANI_API_KEY_ID=REPLACE_IN_PRIVATE_ENV_ONLY
GNANI_STT_MODEL=prisma-v2.5
GNANI_STT_URL=https://api.vachana.ai/stt/v3
GNANI_TTS_ENABLED=false
GNANI_TTS_MODEL=timbre-v2.5
GNANI_TTS_URL=https://api.vachana.ai/api/v1/tts/inference
AUDIO_MAX_DURATION_SECONDS=30
AUDIO_RECORDING_SOFT_LIMIT_SECONDS=25
AUDIO_MAX_UPLOAD_BYTES=10485760
LOG_LEVEL=INFO
```

**Do not commit a real `.env`.** The `GNANI_API_KEY_ID` naming refers to the documented request header; treat it as a secret credential. The 10 MiB upload limit is a **local protective choice**, not a documented provider limit; reject or resize while respecting the 30-second provider maximum. Configure production domains and provider keys in the host's secret manager. Never interpolate secrets into a client-side `VITE_*` variable.

---

## 7. Database design, invariants, migrations and synthetic seed

### 7.1 Entity relationships

```mermaid
erDiagram
  USERS ||--o{ REPORT_INTAKES : creates
  LOCATIONS ||--o{ ASSETS : contains
  REPORT_INTAKES ||--o| WORK_ORDERS : confirms_to
  ASSETS ||--o{ WORK_ORDERS : relates_to
  USERS ||--o{ WORK_ORDERS : reports
  USERS ||--o{ WORK_ORDERS : assigned_to
  WORK_ORDERS ||--o{ AUDIT_EVENTS : has
  USERS ||--o{ AUDIT_EVENTS : acts
  USERS ||--o{ IDEMPOTENCY_KEYS : owns
```

### 7.2 Minimal relational schema (adapt in Alembic)

This is a **reference schema**, not a substitute for versioned migrations. Implement appropriate indexes, foreign keys and checks in actual migrations.

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  display_name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('WORKER','SUPERVISOR')),
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE locations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  aliases JSONB NOT NULL DEFAULT '[]'::jsonb,
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE assets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  location_id UUID NOT NULL REFERENCES locations(id),
  asset_code TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  aliases JSONB NOT NULL DEFAULT '[]'::jsonb,
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE report_intakes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  reporter_id UUID NOT NULL REFERENCES users(id),
  status TEXT NOT NULL CHECK (status IN
    ('TRANSCRIBING','READY_FOR_REVIEW','CONFIRMED','FAILED','DISCARDED')),
  language_code TEXT NOT NULL,
  provider TEXT NOT NULL DEFAULT 'GNANI',
  provider_model TEXT,
  provider_request_id TEXT,
  raw_transcript TEXT,
  edited_transcript TEXT,
  extraction JSONB NOT NULL DEFAULT '{}'::jsonb,
  audio_duration_seconds NUMERIC(6,2),
  stt_latency_ms INTEGER,
  error_code TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ix_intake_reporter_time ON report_intakes(reporter_id, created_at DESC);
CREATE INDEX ix_intake_provider_request ON report_intakes(provider_request_id);

CREATE TABLE work_orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  public_code TEXT NOT NULL UNIQUE,
  intake_id UUID NOT NULL UNIQUE REFERENCES report_intakes(id),
  reporter_id UUID NOT NULL REFERENCES users(id),
  location_id UUID NOT NULL REFERENCES locations(id),
  asset_id UUID NOT NULL REFERENCES assets(id),
  issue_category TEXT NOT NULL CHECK (issue_category IN
    ('LEAKAGE','ELECTRICAL','MECHANICAL','CLEANING','OTHER')),
  description TEXT NOT NULL CHECK (length(trim(description)) > 0),
  priority TEXT NOT NULL DEFAULT 'NORMAL' CHECK (priority IN ('LOW','NORMAL','HIGH')),
  priority_suggestion TEXT,
  status TEXT NOT NULL DEFAULT 'OPEN' CHECK (status IN
    ('OPEN','ASSIGNED','IN_PROGRESS','RESOLVED','CANCELLED')),
  assignee_id UUID REFERENCES users(id),
  version INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  resolved_at TIMESTAMPTZ
);
CREATE INDEX ix_orders_queue ON work_orders(status, priority, created_at DESC);
CREATE INDEX ix_orders_asset_status ON work_orders(asset_id, status);

CREATE TABLE audit_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  work_order_id UUID NOT NULL REFERENCES work_orders(id),
  actor_id UUID NOT NULL REFERENCES users(id),
  action TEXT NOT NULL,
  from_state TEXT,
  to_state TEXT,
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  occurred_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ix_audit_order_time ON audit_events(work_order_id, occurred_at ASC);

CREATE TABLE idempotency_keys (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  actor_id UUID NOT NULL REFERENCES users(id),
  route TEXT NOT NULL,
  idem_key TEXT NOT NULL,
  request_hash TEXT NOT NULL,
  result_work_order_id UUID REFERENCES work_orders(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(actor_id, route, idem_key)
);
```

### 7.3 Data invariants and transaction boundaries

1. `work_orders.intake_id` is unique; one intake cannot create two orders.
2. Worker may confirm **only their own** intake, after successful authentic transcription; supervisor cannot silently rewrite original transcript.
3. `asset.location_id` **must match** submitted `location_id` (validate in service transaction; optional DB trigger if desired).
4. Order creation and its `CREATED` audit event commit **atomically**.
5. Assignment/status changes and corresponding audit event commit **atomically**.
6. All edits use verified identity from token/session, never a client-provided actor ID.
7. Apply `SELECT FOR UPDATE` or optimistic concurrency on `version` for state changes.
8. Generate `public_code` server-side and ensure uniqueness (UUID-derived or sequence); do not use `MAX(code)+1` without locking.
9. Persist raw Gnani transcript as immutable intake metadata, store edits separately; show both only to authorized viewers.
10. A successful provider response with `transcript=""` remains **no speech detected** and cannot create a voice-derived work order.
11. Do not store long-lived audio blobs unless explicitly required and consent/security controls are added.
12. `RESOLVED` requires a real assignee and permissible prior state per transition policy.

### 7.4 Example seed inventory (synthetic only)

| Location code | Location display | Asset code | Asset name | Alias examples |
|---|---|---|---|---|
| BLK-B-F2 | Block B / Floor 2 | PUMP-B02 | Water Pump B-02 | pump, water pump, पानी पंप, मोटर, water motor, நீர் பம்ப் |
| BLK-A-GF | Block A / Ground Floor | AC-A01 | Air Conditioner A-01 | AC, एसी, air conditioner, ஏசி |
| WH-C | Warehouse C | FAN-C03 | Exhaust Fan C-03 | exhaust, fan, पंखा, விசிறி |
| WH-C | Warehouse C | LIGHT-C04 | Bay Light C-04 | light, bulb, लाइट, விளக்கு |

**Critical extraction nuance:** Generic word `pump` does not uniquely establish `PUMP-B02` if another pump exists; pair location + asset alias, and ask the user if multiple matches remain. Asset identifiers and location names must never be invented by an LLM.

**Roles:** seed one `WORKER` and one `SUPERVISOR` identity with randomly generated passwords provisioned privately. Do not publish hard-coded production credentials. If a public demo account is provided, sandbox it to synthetic records, rate-limit it, rotate after the contest, and communicate its limited capabilities.

### 7.5 Migration/rollback procedure

1. Create Alembic initial migration from reviewed models; run against fresh local PostgreSQL.
2. Seed in an idempotent script (`upsert` by stable asset/location codes).
3. Confirm FK/unique/check constraints by deliberate negative inserts.
4. Test backup/restore or create database snapshot before the demo.
5. Later migrations must be additive where possible; never destroy demo data during release.
6. Rollback app version when needed; DB rollback only after verifying compatibility and restoring snapshot if appropriate.

---

## 8. API design — internal application contracts

**All endpoints below are OUR proposed backend API design, not Gnani endpoints.** Prefix `/api/v1`. Authentication: HTTP-only secure cookie with CSRF protection **or** short-lived bearer token; pick one consistent approach. For a fast MVP, short-lived JWT bearer auth with access token kept in memory (not localStorage), HTTPS and no anonymous writes is acceptable. Set CORS to exact frontend origin(s). API error envelope: `{ "error": { "code": "...", "message": "...", "request_id": "..." } }`. Responses never echo provider credentials.

| Endpoint | Role | Purpose / main payload | Success |
|---|---|---|---|
| `POST /auth/login` | Anyone with seeded credentials | email, password | 200 user + access token/session |
| `GET /me` | Authenticated | Current identity/role | 200 |
| `GET /locations` | Worker/Supervisor | Active known locations | 200 |
| `GET /assets?location_id=...` | Worker/Supervisor | Assets in a location | 200 |
| `POST /intakes/transcribe` | Worker | Multipart `audio_file`, `language_code` | 201 intake + authentic transcript + candidates |
| `GET /intakes/{id}` | Owner/Supervisor | Intake transcript, editable candidates, provider provenance | 200 |
| `PATCH /intakes/{id}` | Owner, before confirm | corrected transcript + selected fields | 200 updated review |
| `POST /work-orders` | Worker | `intake_id`, location_id, asset_id, issue_category, description, suggested priority, `Idempotency-Key` | 201 order; 200 same order on replay |
| `GET /work-orders` | Worker/Supervisor | Filter status, location, assignee, paging | 200 appropriate authorized list |
| `GET /work-orders/{id}` | Owner/Supervisor | Order + audit + provenance | 200 |
| `PATCH /work-orders/{id}/assignment` | Supervisor | `assignee_id`, `expected_version` | 200 updated order |
| `PATCH /work-orders/{id}/priority` | Supervisor | `priority`, `expected_version` | 200 updated order |
| `PATCH /work-orders/{id}/status` | Supervisor | `status`, `expected_version`, `resolution_note` when resolving | 200 updated order |
| `GET /work-orders/{id}/duplicates` | Worker owner/Supervisor | Active same-asset candidate list | 200 candidates/warning |
| `POST /work-orders/{id}/acknowledgment-audio` | Owner/Supervisor | language choice; no raw arbitrary text | 200 audio/wav, or typed failure |
| `GET /health/live` | Host | Process healthy | 200 |
| `GET /health/ready` | Host | DB reachable, not a provider cost-incurring call | 200 or 503 |

**Avoid accidental route ambiguity:** register static `POST /work-orders` and typed ID detail routes normally; define `work-orders/{id}/...` clearly in API router.

### 8.1 Example successful transcription response (our schema)

```json
{
  "intake_id": "9fa045f4-c751-44cd-b9e0-ac70f1dcba11",
  "status": "READY_FOR_REVIEW",
  "input_language_code": "hi-IN",
  "raw_transcript": "ब्लॉक बी सेकंड फ्लोर का वाटर पंप लीक हो रहा है",
  "provider": {
    "name": "Gnani AI",
    "model": "prisma-v2.5",
    "request_id": "<real-request-id-from-provider>"
  },
  "suggested_fields": {
    "location_id": "<seeded-location-uuid>",
    "asset_id": "<seeded-asset-uuid>",
    "issue_category": "LEAKAGE",
    "priority_suggestion": "HIGH"
  },
  "field_evidence": {
    "location": ["ब्लॉक बी", "सेकंड फ्लोर"],
    "asset": ["वाटर पंप"],
    "issue": ["लीक"]
  },
  "needs_review": true,
  "unresolved_fields": []
}
```

`<...>` placeholders above are **illustrative**, not provider responses. A successful actual demo must show real values returned to the backend from Gnani and must label any redactions as redactions.

### 8.2 Example work-order creation request

```http
POST /api/v1/work-orders
Authorization: Bearer <USER_ACCESS_TOKEN>
Idempotency-Key: 0d6a6201-d6c1-464c-9fb2-43ea8105c4b7
Content-Type: application/json

{
  "intake_id": "9fa045f4-c751-44cd-b9e0-ac70f1dcba11",
  "location_id": "<existing-location-uuid>",
  "asset_id": "<existing-asset-uuid>",
  "issue_category": "LEAKAGE",
  "description": "Water pump leaking on second floor",
  "priority_suggestion": "HIGH"
}
```

**Behavior:** Replaying the same key and canonical body for the same actor/route returns the same work order. Reusing the key with a different body returns `409 IDEMPOTENCY_CONFLICT`. Two different keys for one `intake_id` are still prevented by the DB unique constraint; translate that integrity error to the existing ticket, never a duplicate.

### 8.3 Suggested standardized application errors

| Our error code | HTTP | UI treatment |
|---|---:|---|
| `INVALID_AUDIO` | 400 | Explain allowed formats/size and retry |
| `AUDIO_TOO_LONG` | 413 or 422 | Limit recording and rerecord |
| `GNANI_AUTH_FAILURE` | 502 | Private configuration issue; inform operator |
| `GNANI_QUOTA_EXHAUSTED` | 503 | Explicitly unavailable; do not synthesize transcript |
| `GNANI_RATE_LIMITED` | 503 | Retry after backoff, queue or ask user to retry |
| `GNANI_TRANSCRIPTION_FAILED` | 502 | Keep draft; retry actual provider call |
| `NO_SPEECH_DETECTED` | 422 | Rerecord; no work order created |
| `UNKNOWN_ASSET` / `UNKNOWN_LOCATION` | 422 | Show dropdown correction required |
| `ASSET_LOCATION_MISMATCH` | 422 | Reconcile asset and location |
| `FORBIDDEN` | 403 | Access denied |
| `INVALID_TRANSITION` | 409 | Refresh current order state |
| `VERSION_CONFLICT` | 409 | Refresh and reapply edit |
| `IDEMPOTENCY_CONFLICT` | 409 | New idempotency key for truly new action |
| `TTS_UNAVAILABLE` | 503 | Continue in text; saved order remains intact |

---

## 9. Gnani integration specification — the central technical proof

### 9.1 Account and authorization spike (FIRST task)

1. Verify programme registration and access email.
2. Open `https://app.gnani.ai/voice`, create a scoped credential with appropriate STT access and optionally TTS.
3. Store key in local secret environment / host secret manager; never in frontend or recording.
4. Record a real ≤25s test clip in Hindi; use safe synthetic content.
5. Execute the provider API request directly using cURL/Postman or a short Python spike.
6. Check HTTP status, `success`, nonempty `transcript`, actual `model` and `request_id`.
7. Add one live integration test that calls this provider **only with an explicit opt-in environment flag**, not on every CI run.
8. Record redacted evidence: timestamp, chosen language, returned model/request ID, no key or real personally identifying speech.
9. If credentials/scope/credits fail, resolve them through the official console/support. Do not construct an alternative fake provider adapter and present it as live.

### 9.2 Exact Prisma v2.5 REST contract (official)

- Endpoint: `POST https://api.vachana.ai/stt/v3`
- Header: `X-API-Key-ID: <SECRET>`; optional `X-API-Request-ID: <our-correlation-id>`.
- Body: `multipart/form-data` with required `audio_file` and `language_code` (`hi-IN`, `en-IN`, or `ta-IN` after verifying each supported language in docs).
- `model`: omit for documented **Prisma v2.5 default** or set `model=prisma-v2.5` explicitly, after validating with your key.
- Supported formats: WAV, MP3, OGG, FLAC, AAC, M4A. REST input maximum **30 seconds**. Supported sample-rate range in the quick start: **8 kHz to 44.1 kHz**.
- Typical response keys: `success`, `request_id`, `transcript`, `model` and sometimes timing/`output.literal`; optional fields must be parsed defensively.
- **Empty transcription** can still return `success: true`; application must treat `transcript.trim()==""` as not usable.
- Prisma v2.5 uses **one** selected language code per request. **Do not** send `indic-auto`, `codemix`, or multiple languages with v2.5.
- `bias_list` and `bias_score` are optional v2.5 word-boosting features; defer until baseline performance is measured.

```bash
# Provider smoke test — first use a consented, synthetic-content WAV clip.
# Use environment variables rather than committing a real key.
curl --fail-with-body --request POST \
  'https://api.vachana.ai/stt/v3' \
  --header "X-API-Key-ID: ${GNANI_API_KEY_ID}" \
  --form 'audio_file=@sample_hi.wav' \
  --form 'language_code=hi-IN' \
  --form 'model=prisma-v2.5'
```

**Important HTTP rule:** Let the HTTP client set the `multipart/form-data` boundary. Do not manually hardcode a plain `Content-Type: multipart/form-data` header if your client is building the multipart body automatically.

**Provider docs:** https://docs.gnani.ai/api/STT/speech-to-text

### 9.3 Optional Prisma v3.0 experiment — only after P0 passes

Current docs describe `model=prisma-v3.0`, language hints such as `indic-auto` or up to four comma-separated languages, and `format=codemix`. This could improve mixed-language demonstrations, **but is a separately tested enhancement**. Introduce an explicit config feature flag, compare against v2.5 on identical consented clips, record model IDs accurately, and keep a verified v2.5 fallback. Do not mix v3-only parameters into the v2.5 contract. Verify eligibility/credits for this version in your account; the programme listing highlights v2.5.

**Decision gate EXP-01:** Use v3.0 only if (a) live call works, (b) correct fields improve on your fixture set, (c) no blocking regression, and (d) submission description identifies actual models used.

### 9.4 Browser audio — subtle but critical implementation issue

**Many browsers produce `audio/webm`/Opus via `MediaRecorder`, whereas Gnani REST documents WAV/MP3/OGG/FLAC/AAC/M4A, not WebM.** An unmodified `audio/webm` upload can fail.

Implement **all** of the following:

1. Detect supported `MediaRecorder.isTypeSupported` MIME types, store blob metadata; never assume the recorded file is WAV because its filename ends `.wav`.
2. Send original browser recording to **our FastAPI server** only.
3. Validate maximum request size at gateway and app, inspect actual media with `ffprobe` and enforce `duration <= 30.0s` (UI recording soft cap 25s).
4. Normalize untrusted browser recordings using `ffmpeg` into **16 kHz mono PCM WAV** (chosen implementation format). The official quick start supports input sample rates up to 44.1 kHz, so 16 kHz is inside range.
5. Use `subprocess.run([...], shell=False, timeout=...)`, fixed executable path, random temporary file names, strict resource quotas and cleanup in `finally`. Reject corrupt/empty/oversize files; do not trust client MIME/extensions.
6. Confirm resulting audio has the expected channel/sample rate and nonzero duration before provider upload.
7. Avoid saving raw audio permanently; delete temp files in success/failure; don't place audio in logs.
8. Provide manual **text entry for accessibility/support** only with clear `MANUAL_TEXT` provenance; **never** count manual text as live Gnani STT proof.

### 9.5 Provider adapter implementation plan

Define a `GnaniSpeechClient` interface with `transcribe(audio_bytes, language, correlation_id)` and `synthesize(text, language, voice, correlation_id)` methods. Production adapter calls Gnani; test adapter returns explicit fixtures only in test environment. Disable fixture adapter in deployment configurations.

For STT:

1. Build multipart request to official URL; set `X-API-Key-ID` server-side.
2. Use `httpx.AsyncClient` with explicit connection/read timeouts and response-size control. Initial overall timeout may be **60 seconds** (engineering starting point, not provider SLA).
3. Apply one local concurrency semaphore per process; `429` may indicate very low provider concurrency. Avoid uncontrolled parallel demo requests.
4. Retry **transient** connection/429/502/503/504 failures at most 1–2 times with capped jittered exponential backoff; do **not** retry 400, 401, 402, 403, validation errors automatically.
5. Treat provider HTTP status as authoritative; provider JSON error shapes differ (including 422 and 504); parse defensively.
6. Verify `success is True` and nonempty transcript before marking `READY_FOR_REVIEW`.
7. Store exact returned model/request ID, chosen language, correlation ID, measured elapsed time; redact transcript in general-purpose request logs.
8. Expose a typed app error message (not the raw secret-bearing provider response) on failure.
9. No downstream automatic order creation — require explicit user confirmation.

**Failure-mode test:** Shut off the provider adapter or use a known invalid test key in isolated test config. UI must show a real error and **not** a prepared ticket or fake transcript.

### 9.6 Exact Timbre v2.5 contract (P1)

- Endpoint: `POST https://api.vachana.ai/api/v1/tts/inference`.
- Header: `X-API-Key-ID` and `Content-Type: application/json`.
- Example payload: `model=timbre-v2.5`, `text`, `voice=Nalini`, `language=hi-IN`, `speed=1.0`, `audio_config={sample_rate:48000,num_channels:1,sample_width:2,encoding:linear_pcm,container:wav}`.
- A successful response is **binary audio** (commonly `audio/wav`), **not JSON**. Do not call `response.json()` on success.
- Suggested catalog: Hindi `Nalini`/`hi-IN`, Hinglish `Poorvi`/`hi-en`, Tamil `Asmita`/`ta-IN`, English `Kaveri`/`en-IN`; ensure chosen voice matches model/version.
- Construct acknowledgment text from the **committed** work-order result, not untrusted raw transcript: “Your report has been registered. Ticket number [spoken-safe identifier].” Prefer simple identifiers that sound natural; avoid voice-reading UUID strings.
- Generate after ticket commit (separate request); return WAV with correct MIME, caching only where appropriate; if TTS fails, return text acknowledgment with an explicit audio-unavailable state.

```bash
curl --fail-with-body --request POST \
  'https://api.vachana.ai/api/v1/tts/inference' \
  --header "X-API-Key-ID: ${GNANI_API_KEY_ID}" \
  --header 'Content-Type: application/json' \
  --data '{
    "text": "आपकी शिकायत दर्ज हो गई है।",
    "model": "timbre-v2.5",
    "voice": "Nalini",
    "language": "hi-IN",
    "speed": 1.0,
    "audio_config": {
      "sample_rate": 48000,
      "num_channels": 1,
      "sample_width": 2,
      "encoding": "linear_pcm",
      "container": "wav"
    }
  }' --output acknowledgment.wav
```

**Provider docs:** https://docs.gnani.ai/api/TTS/tts-inference  
**Voice catalog:** https://docs.gnani.ai/api/TTS/available-voices

### 9.7 Provider error taxonomy and safe behavior

| Gnani HTTP/provider condition | Application action |
|---|---|
| 400 invalid language, audio decode, unsupported file, >30 seconds | Show exact user-correctable category; do not retry identical bad request |
| 401 invalid/missing API key | Operator configuration incident; no fabricated fallback |
| 402 insufficient credits | Halt further provider calls, report credit issue |
| 403 scope denied | Fix key scope/access; no auto fallback |
| 422 missing form field | Developer bug; add contract regression test |
| 429 rate/concurrency limited | Queue/serialize briefly, cap backoff, advise retry |
| 500/502/503 provider issue | Bounded retry; then clear unavailable state |
| 504 upstream timeout | Bounded retry and show uncertainty; avoid duplicate business write |
| 200 + empty transcript | “No intelligible speech detected”; require re-record |
| 200 + `truncated: true` when available | Show warning; re-record shorter before confirmation |
| Provider API response lacks optional metadata | Keep functioning but only display verified fields; never invent request ID |
| TTS returns non-audio/error | Text success remains; no attempt to undo committed order |

**Cost rule:** 5,000 programme credits are allocated as described by Gnani, but the price per request is not specified in this plan. Use the Gnani console's **actual usage/remaining balance**, not fabricated arithmetic, to budget tests; cap test volume and disable accidental retry storms.

---

## 10. Multilingual extraction, validation and decision logic

### 10.1 Why the extraction layer is not “magical AI”

Gnani Prisma converts speech **to text**. It does not, by itself, promise reliable extraction of an asset UUID, machine type, safety classification or work-order transaction. Those are **our application responsibilities**. Keep the capability boundaries visible in architecture and demo. Optional Evon/other language reasoning is **not required** for a genuine Gnani-based workflow because STT is essential to the spoken intake.

### 10.2 Extraction pipeline

1. Take real `raw_transcript` as an immutable input.
2. Normalize Unicode and whitespace; use casefold, punctuation normalization, and optional transliteration only for search, while preserving original text.
3. Map location aliases to a seeded known-location catalog (`Block B`, `ब्लॉक बी`, `பிளாக் பி` etc.).
4. Map equipment aliases to seeded assets **within resolved location**.
5. Match issue cues by language-aware phrase dictionaries: `leak`, `leaking`, `लीक`, `रिसाव`, `கசிவு` → `LEAKAGE`; add guarded cues for electrical, mechanical, cleaning.
6. Match urgency cues separately (`urgent`, `तुरंत`, `जल्दी`, `அவசரம்`) → `HIGH` **suggestion only**; neutral default can be `NORMAL` after human review.
7. Resolve collisions: zero matches → missing; multiple plausible matches → ambiguous; mismatched location/assets → invalid.
8. Produce `suggested_fields` + **exact matched evidence spans** + `unresolved_fields` + parser version.
9. Present editable values; user explicitly confirms their selected asset/location/issue.
10. Server validates final selections against DB and persists only on confirmation.

### 10.3 Example extraction object (our schema)

```json
{
  "parser_version": "rules-v1",
  "location": {
    "id": "<known-location-id>",
    "evidence": ["Block B", "second floor"],
    "status": "SUGGESTED"
  },
  "asset": {
    "id": "<known-asset-id>",
    "evidence": ["water pump"],
    "status": "SUGGESTED"
  },
  "issue_category": {
    "value": "LEAKAGE",
    "evidence": ["leak"],
    "status": "SUGGESTED"
  },
  "priority_suggestion": {
    "value": "HIGH",
    "reason": "Reporter said urgent",
    "authoritative": false
  },
  "unresolved_fields": [],
  "requires_confirmation": true
}
```

Do not report an arbitrary “97% AI confidence” without a calibrated, evaluated confidence model. Prefer transparent statuses `EXACT_MATCH`, `AMBIGUOUS`, `MISSING`, `USER_CORRECTED` and direct evidence spans.

### 10.4 Ambiguity and safety rules

| Situation | Correct handling |
|---|---|
| “Pump broken” with no location | Ask location via dropdown; do not infer from worker identity |
| “Block B, second floor” but multiple pumps | Display candidate list; require user choice |
| “Block A pump” with selected `PUMP-B02` | Reject asset/location mismatch |
| “Fan issue” with no issue type | Show `OTHER` and require explicit explanation or selection |
| “Urgent” in transcript | Suggest HIGH; supervisor may change |
| “Sparks, smoke” | Show emergency-protocol warning, require urgent human intervention; **no automated safety dispatch** |
| No intelligible speech | Retry real recording; no order creation from fictional text |
| Worker edits transcript heavily | Preserve raw provider text; audit corrected text and final structured fields |
| Similar active report exists | Warn and link existing order; do not silently merge/drop new report |

### 10.5 Optional LLM-based structured extraction (only after deterministic path works)

If a separately available LLM is used: constrain output with a JSON schema (`location_code`, `asset_code`, `issue_category`, `description`, `urgency_cue`), run strict Pydantic validation, verify catalog membership, cite exact source spans when available, and require user confirmation. The LLM is a **parser enhancement**, not evidence that Gnani has performed reasoning unless an actual Gnani reasoning model was separately integrated. Track model/provider accurately in docs. Do not make a hosted Evon dependency or costly LLM orchestration a blocker.

---

## 11. UI/UX implementation specification

### 11.1 Pages and components

| Screen | Must display | Important states |
|---|---|---|
| Login | Synthetic worker/supervisor identity | Invalid password, loading, session expiration |
| Worker report | Language selector, audio record/stop, duration, transcript | Idle, permission denied, recording, uploading, transcribing, failed |
| Review/confirm | Original transcript, editable corrected transcript, resolved location, asset, issue, priority suggestion | Fields missing, ambiguous, duplicate warning, confirm disabled |
| Ticket success | Real ticket code, status and link, optional play acknowledgment | Saved, TTS generating, audio unavailable |
| My tickets | Worker-owned tickets, created time and status | Loading, empty, error |
| Supervisor console | Queue, summary counts, location/status filters, assignment, priority, transitions | Empty list, stale version, success, error |
| Ticket detail/provenance | Status timeline, assignee, reporter, transcript, correction log, model/request ID | Permissions, loading, audited events |

### 11.2 Required controls and accessibility

- Large microphone button with visible **start/stop** state, elapsed seconds and immediate stop at 25-second soft cap.
- Visible language selection; explain that Prisma v2.5 is sent **one chosen language code**; code-mixed reports may need corrections.
- Text transcript always visible even when audio acknowledgment exists.
- Confirmation never triggered merely by finishing transcription; separate explicit “Confirm and create work order” button.
- Fields with unresolved values are highlighted and selectable from **known catalog records**.
- Busy indicators for upload, STT and TTS; disable duplicate submission while pending, but rely on backend idempotency too.
- Accessible form labels, keyboard focus, ARIA status updates where appropriate and responsive mobile layout.
- Worker ticket success should display authoritative status and creation time only **after server persistence**.
- Supervisor must see who reported, source of data, what was edited, and next permitted action.

### 11.3 Component contracts

- `VoiceRecorder`: emits `Blob`, `mimeType`, `durationSeconds` or typed capture error; never makes direct Gnani call.
- `LanguagePicker`: emits a verified locale string; default selected from explicit user choice, not speculative automatic detection.
- `TranscriptReview`: receives `raw_transcript` as read-only and `edited_transcript` as editable; emits corrected fields.
- `AssetSelector`: options filtered by location, never free-form arbitrary ID.
- `WorkOrderCard`: uses backend values, never frontend-generated success metadata.
- `StatusTimeline`: renders server audit events sorted by occurrence, not simulated progress.
- `GnaniEvidencePanel`: displays actual `provider_model`/`request_id` when available; never keys or authentication headers.

### 11.4 Visual direction

Create a professional industrial-operations UI: clean light surfaces, readable text, restrained accent color, clear severity labels, compact queue cards and prominent voice input. Avoid animations that obscure state, fake “AI confidence” meters, nonworking charts and dashboard counts not backed by database queries. A polished vertical slice is preferred over decorative breadth.

---

## 12. Reliability, security, privacy and production controls

### 12.1 Threat model and mitigations

| Threat / failure | Mitigation | Verification |
|---|---|---|
| Exposed Gnani key | Backend only, secret manager, redaction, git secret scan | Search built JS, repo and logs |
| Forged worker/supervisor request | Server JWT verification, password hash, per-route role checks | RBAC negative tests |
| IDOR: worker reads another worker's ticket | Apply row-level ownership filter on every GET/write path | Two-worker permission test |
| Upload bombing / malicious media | Size + duration + MIME sniff + ffprobe/ffmpeg timeout/limits | Oversize/corrupt upload tests |
| Cross-origin abuse | Explicit CORS, HTTPS, secure auth strategy | Origin testing |
| SQL injection | ORM parameter binding and schema checks | Injection payload test |
| XSS through transcript | React-safe escaping, no unsafe HTML insertion | Script-containing transcript test |
| Duplicate work orders | Idempotency + unique intake constraint | Parallel replay test |
| Wrong equipment | Catalog validation + human confirmation | Unknown/mismatch tests |
| Uncontrolled retry cost | Concurrency limiter, finite backoff, credit budget | Simulated 429 sequence |
| Sensitive audio retention | Temp deletion, no routine audio storage | Inspect local/cloud persistence |
| Misleading public demo | Authentic live provider, inspectable metadata, disclose any edits | Demo review checklist |
| Host cold start or outage | Check deployed readiness early, preserve local executable fallback for recording | Pre-demo smoke |

### 12.2 Basic SRE controls

- `GET /health/live`: app process responsive; **must not** call paid Gnani API.
- `GET /health/ready`: DB accessible and migrations applied; fail when incapable of handling work orders.
- Logs: JSON fields such as `correlation_id`, `stage`, `status_code`, `duration_ms`, `provider_model` and `provider_request_id` after sanitization; no API keys, raw audio, or full transcripts in routine logs.
- UI errors: actionable and honest; no fabricated “success” on provider failure.
- Safe retries: `STT` transcriptions can be retried with caution; business mutations require idempotency. `TTS` can be retried after commit without mutating ticket.
- Backups: snapshot or database export before final recording; verify recovery for seed data.
- Dependency isolation: TTS failure must be limited to acknowledgment output.
- Incident runbook: identify stage → capture correlation ID → inspect sanitized logs → determine upstream/local issue → fix/redeploy → rerun smoke tests.

### 12.3 Privacy and ethics

Use only fake location codes, fake IDs and consented audio spoken by the team. Do not upload recordings from real employees, customers or third parties without an appropriate legal basis and permission. Don't publicly show account details, keys or full personal voice records. Prefer an ephemeral audio lifecycle and a clear disclosure that reports are sent to Gnani for speech recognition. The challenge page explicitly advises synthetic data. Document actual retention practices, not aspirational ones.

---

## 13. End-to-end implementation work breakdown (WBS)

Each phase has a **trace ID**, concrete tasks, outputs, dependencies and acceptance test. The sequence is strict: **do the real Gnani spike before polishing the dashboard.**

### Phase 0 — Challenge readiness and source lock [WBS-00]

**Dependencies:** none. **Owner:** lead. **Timebox:** start immediately.

- [ ] **WBS-00.1** Read programme rules/terms; verify registration, eligibility, team count, final form delivery.
- [ ] **WBS-00.2** Verify Gnani account, credits, key scope; save credentials privately.
- [ ] **WBS-00.3** Snapshot the official docs/URLs used for endpoint decisions; record last checked date.
- [ ] **WBS-00.4** Freeze P0 backlog, project title, roles, language baseline and demonstration scenario.
- [ ] **WBS-00.5** Create GitHub repo, protected main workflow, issue tracker, RTM and risk register.

**Output:** baseline plan, repo, access proof.  
**Gate G0:** enrolment/access verified; API testing may proceed.  
**Do not proceed by assuming keys work; prove it next.**

### Phase 1 — Prove real Gnani STT integration [WBS-01] **CRITICAL PATH**

- [ ] **WBS-01.1** Record short Hindi synthetic audio; verify actual format/duration locally.
- [ ] **WBS-01.2** Run documented cURL call to `POST /stt/v3` with `X-API-Key-ID`.
- [ ] **WBS-01.3** Confirm nonempty transcript, actual `request_id`, actual model, HTTP status.
- [ ] **WBS-01.4** Build `GnaniSpeechClient` HTTPX adapter with typed success/error parsing.
- [ ] **WBS-01.5** Write contract tests for success, no-speech, 400, 401, 402, 403, 429, 500 and timeout.
- [ ] **WBS-01.6** Save redacted live integration evidence (`docs/evidence/gnani-stt-live.md`).

**Output:** callable provider adapter and one verified live test.  
**Gate G1:** genuine Gnani transcription works with **the exact deployed account/key**.  
**If blocked:** concentrate on provider access support and other independent tasks (repo, DB, UI skeleton), but **never claim a finished valid Gnani build** until this gate passes.

### Phase 2 — Foundation, identity, inventory and schema [WBS-02]

- [ ] **WBS-02.1** Bootstrap React/Vite/TypeScript and FastAPI app with strict formatting.
- [ ] **WBS-02.2** Configure PostgreSQL, SQLAlchemy, Alembic initial migration.
- [ ] **WBS-02.3** Implement `users`, `locations`, `assets`, `report_intakes`, `work_orders`, `audit_events`, `idempotency_keys`.
- [ ] **WBS-02.4** Seed synthetic workers, supervisor, locations, equipment and aliases.
- [ ] **WBS-02.5** Implement seeded authentication with salted password hashing (Argon2/bcrypt) and verified role checks.
- [ ] **WBS-02.6** Implement `/health/live`, `/health/ready`, CORS, errors and structured request IDs.
- [ ] **WBS-02.7** Add migration and access-control tests.

**Output:** runnable app + durable DB + testable users + inventory.  
**Gate:** separate worker/supervisor sessions, valid DB relations, and no role escalation.

### Phase 3 — Voice recording, preprocessing, STT intake [WBS-03]

- [ ] **WBS-03.1** Implement microphone permission handling and recorder state machine.
- [ ] **WBS-03.2** Set 25-second soft stop, metadata preview, cancel/rerecord.
- [ ] **WBS-03.3** Create multipart upload to our `/intakes/transcribe`; never invoke Gnani from React.
- [ ] **WBS-03.4** Validate size, media type, duration; convert WebM/Opus → WAV using protected ffmpeg invocation.
- [ ] **WBS-03.5** Call verified `GnaniSpeechClient` with selected `language_code`; preserve response metadata.
- [ ] **WBS-03.6** Save real intake row with `READY_FOR_REVIEW` only after genuine nonempty STT result.
- [ ] **WBS-03.7** Delete temporary audio files and handle errors, retry state, empty transcript.
- [ ] **WBS-03.8** Add audio validation, provider adapter and live smoke tests.

**Output:** browser-recorded voice becomes authentic, persisted Gnani transcript.  
**Gate:** a completely new spoken sentence reaches transcript screen; inspect genuine request ID.

### Phase 4 — Structured extraction and verified ticket creation [WBS-04]

- [ ] **WBS-04.1** Implement Unicode-safe alias normalization and deterministic parser.
- [ ] **WBS-04.2** Resolve location and asset candidates against DB; enforce asset-location relationship.
- [ ] **WBS-04.3** Extract issue category and nonauthoritative urgency suggestion with evidence.
- [ ] **WBS-04.4** Implement `Review & Confirm` page showing raw transcript and editable corrections separately.
- [ ] **WBS-04.5** Validate required fields on server; reject ambiguities and missing records.
- [ ] **WBS-04.6** Generate per-submission idempotency key; implement DB uniqueness/transaction logic.
- [ ] **WBS-04.7** Commit confirmed intake → order → `CREATED` audit event in one transaction.
- [ ] **WBS-04.8** Show only server-returned real ticket code; verify after page refresh.
- [ ] **WBS-04.9** Create 15-case extraction fixtures and negative validation tests.

**Output:** verified voice-to-ticket vertical slice.  
**Gate G2:** valid voice report creates exactly one order; incomplete report creates none; refresh retains record.

### Phase 5 — Supervisor workflow and operational accountability [WBS-05]

- [ ] **WBS-05.1** Implement authorized `/work-orders` listing with server paging/filters.
- [ ] **WBS-05.2** Implement supervisor queue: status, priority, location, assignee, created time.
- [ ] **WBS-05.3** Implement authorized assignment and controlled priority adjustment.
- [ ] **WBS-05.4** Enforce state machine and expected `version` on every workflow mutation.
- [ ] **WBS-05.5** Transactionally write event history for each action.
- [ ] **WBS-05.6** Implement ticket details, provenance panel and chronological timeline.
- [ ] **WBS-05.7** Unit/integration/E2E tests for authorization, transitions and concurrency.

**Output:** functioning supervisor operational loop.  
**Gate:** supervisor assigns and resolves a persisted worker-submitted ticket; worker sees real updated state.

### Phase 6 — TTS, duplicate warnings and finish quality [WBS-06] **P1 IF TIME**

- [ ] **WBS-06.1** Verify live Timbre v2.5 key scope using safe short text.
- [ ] **WBS-06.2** Add server-side TTS adapter; return binary WAV with correct MIME.
- [ ] **WBS-06.3** Add `Play acknowledgment` only after saved ticket success; nonblocking error state.
- [ ] **WBS-06.4** Flag potential duplicates for the same asset in `OPEN/ASSIGNED/IN_PROGRESS` states; show warning, don't silently merge.
- [ ] **WBS-06.5** Polish mobile, accessibility, empty/error states; remove decorative unimplemented elements.
- [ ] **WBS-06.6** Document actual model usage and limitations.

**Output:** differentiated speech-in/speech-out experience and trust cues.  
**Gate:** independently demonstrate a verified WAV and a saved-ticket fallback on TTS outage.

### Phase 7 — Verification, staging and production release [WBS-07]

- [ ] **WBS-07.1** Lint, typecheck, backend unit and API contract tests green.
- [ ] **WBS-07.2** Verify two-role RBAC, IDOR and direct HTTP requests, not only frontend route blocking.
- [ ] **WBS-07.3** Evaluate 15 real or consented short audio scripts, review ground truth and export results.
- [ ] **WBS-07.4** Execute negative scenarios: empty, unsupported, oversized, corrupt, rate limited, provider down, wrong asset, duplicate, status conflict.
- [ ] **WBS-07.5** Deploy HTTPS frontend and backend, production secret config and PostgreSQL; check DB migration.
- [ ] **WBS-07.6** Run production smoke with **real Gnani** from mobile/desktop browser using newly recorded clip.
- [ ] **WBS-07.7** Run backup/rollback drill, secret scan, public repository inspection.
- [ ] **WBS-07.8** Freeze release tag and save evidence.

**Output:** tested build and reproducible deployment.  
**Gate G3:** zero known critical/high defects, genuine provider integration verified, app stable enough to record.

### Phase 8 — Demo, engagement integrity and final submission [WBS-08]

- [ ] **WBS-08.1** Record full technical run and a sharp 60-second showcase with actual app behavior.
- [ ] **WBS-08.2** Verify audio/video clarity, accuracy of model names, no credentials/personal data shown.
- [ ] **WBS-08.3** Draft project summary and each member's personally verifiable contributions.
- [ ] **WBS-08.4** Post public demo on LinkedIn and/or X; tag Gnani AI; both exact hashtags.
- [ ] **WBS-08.5** Verify post is public and directly opens for someone not signed into your account (where platform permits).
- [ ] **WBS-08.6** Find official submission form from registration email, fill all requested fields and **nominate post URL(s)**.
- [ ] **WBS-08.7** Submit before November 10, 11:59 PM IST; retain visible/email confirmation.
- [ ] **WBS-08.8** Share organically only. No bought promotion, exchange groups, bots or misleading teaser.

**Output:** full contest entry, not merely public content.  
**Gate G4/G5:** demonstrable video + public post(s) + completed official form + confirmation.

---

## 14. Test strategy, fixtures and objective validation

### 14.1 Test pyramid and boundaries

| Layer | Test type | Mocks allowed? | Must demonstrate |
|---|---|---|---|
| Unit | parser, validator, state machine, audio metadata guard | Yes, deterministic fixtures | Correct logic |
| API/DB integration | migration, constraints, ownership, transactions, idempotency | Mock Gnani only, not DB | Correct persistent business outcome |
| Provider contract | Gnani adapter parsing success/error envelopes | Yes, explicit recorded/sanitized provider-shaped fixtures | Client contract robustness |
| Live provider | Authenticated STT/TTS invocation with consented synthetic audio | **No** | Genuine Gnani integration evidence |
| Browser E2E | Record → transcribe → review → create → assign → resolve | No for final release smoke; can mock in CI for fast regressions | Real user workflow |
| Deployment smoke | Deployed HTTPS frontend → live backend → Gnani → DB | **No** | Demo-ready behavior |

For deterministic CI, an explicitly named mock adapter may be used. For the official **public demo and live acceptance gate, it must be disabled**. CI green is not evidence that provider integration is live; both categories of tests are needed.

### 14.2 Test ID catalog

| Test IDs | Scope | Expected result |
|---|---|---|
| T-AUD-01 | Valid short WAV | Accepted, correct duration |
| T-AUD-02 | Browser WebM converted | Converted playable WAV sent to Gnani |
| T-AUD-03 | >30s recording | Rejected before provider call |
| T-AUD-04 | Corrupt/0-byte recording | Typed error, no intake success |
| T-AUD-05 | Permission denied | UI message, no fake audio |
| T-STT-01 | Valid Gnani v2.5 response | Transcript/model/request ID mapped |
| T-STT-02 | 200 with empty transcript | `NO_SPEECH_DETECTED`, no created ticket |
| T-STT-03 | 401/403 key/scope error | Operator-readable error, no mock fallback |
| T-STT-04 | 402 credits exhausted | User told service unavailable |
| T-STT-05 | 429 concurrency limit | Finite retry/backoff; no retry storm |
| T-STT-06 | 400/422 malformed audio/body | No retry without input change |
| T-STT-07 | 5xx / network timeout | Recoverable error state, no invented transcript |
| T-LIVE-01 | Real newly recorded STT | Actual Gnani `request_id`/`model` observable |
| T-NLP-01…15 | Ground-truth extraction corpus | Actual field-level comparison produced |
| T-VAL-01 | Missing location | Confirm blocked |
| T-VAL-02 | Missing asset | Confirm blocked |
| T-VAL-03 | Unknown catalog ID | Confirm blocked |
| T-VAL-04 | Asset belongs to different location | Confirm blocked |
| T-VAL-05 | Empty description | Confirm blocked |
| T-VAL-06 | Ambiguous matching asset | User selection required |
| T-ORD-01 | Valid confirmed intake | One work order, audit event |
| T-ORD-02 | Identical idempotent retry | Same work-order ID, one DB row |
| T-ORD-03 | Same key different request body | HTTP 409, no mutation |
| T-ORD-04 | Two keys same intake | DB uniqueness still prevents duplicate |
| T-ORD-05 | Simulated DB error | No success, no orphan audit event |
| T-ORD-06 | Refresh after save | Ticket remains present |
| T-ORD-07 | Parallel request race | One order, no data corruption |
| T-ORD-08 | Failed STT intake confirmation attempt | Rejected |
| T-RBAC-01 | Worker invokes supervisor assignment | 403 |
| T-RBAC-02 | Worker accesses other worker's ticket | 403/404 without data leakage |
| T-RBAC-03 | Expired/invalid token | 401 |
| T-RBAC-04 | Supervisor access to queue | Correct filtered data |
| T-WF-01 | OPEN → ASSIGNED | Allowed, assignee saved |
| T-WF-02 | ASSIGNED → IN_PROGRESS | Allowed, audit appended |
| T-WF-03 | IN_PROGRESS → RESOLVED | Allowed with resolution note |
| T-WF-04 | Invalid transition | 409, no state mutation |
| T-WF-05 | Stale expected version | 409, refresh needed |
| T-TTS-01 | Real Timbre v2.5 request | Valid binary WAV/`audio/wav` |
| T-TTS-02 | Provider returns JSON error | Not interpreted as audio |
| T-TTS-03 | TTS down after saved ticket | Ticket persists, text acknowledgment works |
| T-TTS-04 | Voice/model mismatch | Clear failure, no fake audio |
| T-DUP-01 | Same asset has active order | Duplicate warning shown |
| T-DUP-02 | Same asset has resolved order only | No active duplicate warning |
| T-DUP-03 | Two distinct assets | No false duplicate match |
| T-AUDIT-01 | Create/assign/resolve | All history events present |
| T-AUDIT-02 | Transcript edited | Raw and corrected versions both available |
| T-AUDIT-03 | Unauthorized viewer | No provider/intake details disclosed |
| T-OPS-01 | Health readiness without DB | 503 |
| T-SEC-01 | Built frontend searched for Gnani key | Secret absent |
| T-SEC-02 | XSS string in transcript | Rendered as harmless text |
| T-SEC-03 | Malicious media and oversize | Rejected without process crash |
| T-E2E-01 | Full worker/supervisor flow | End-to-end passes with persistence |
| T-SUB-01…07 | Registration, genuine demo, post, tags, model details, form, confirmation | All required official submission checks done |

### 14.3 Synthetic 15-case multilingual evaluation suite

Record each with consented audio; keep a separate expected-field CSV. The following text is **script material**, **not** a substitute for recording and sending real speech through Gnani.

| Case | Language / script | Utterance / scenario | Expected treatment |
|---|---|---|---|
| NLP-01 | Hinglish | “Block B second floor ka water pump leak ho raha hai, urgent hai.” | `BLK-B-F2`, `PUMP-B02`, leakage, HIGH suggestion |
| NLP-02 | Hindi | “ब्लॉक बी की दूसरी मंजिल पर पानी का पंप लीक कर रहा है।” | Known pump and location, leakage |
| NLP-03 | English | “The air conditioner on Block A ground floor is not cooling.” | `AC-A01`, mechanical/OTHER as explicitly defined |
| NLP-04 | Tamil | “பிளாக் பி இரண்டாவது மாடியில் தண்ணீர் பம்ப் கசிகிறது.” | Block B pump/leak if aliases verified |
| NLP-05 | Hinglish | “Warehouse C mein exhaust fan band ho gaya.” | Warehouse C fan, mechanical |
| NLP-06 | Hindi | “गोदाम सी में लाइट खराब है।” | Warehouse C light, electrical/OTHER as dictionary defines |
| NLP-07 | English | “The pump has a problem.” | **Missing location**, block confirmation |
| NLP-08 | Hindi | “तुरंत ठीक करो!” | **Missing location and asset**, block |
| NLP-09 | English | “Block A water pump leaks.” | Reject unknown/mismatched asset if no Block A pump seeded |
| NLP-10 | Tamil | “இங்கே விளக்கு வேலை செய்யவில்லை.” | Location unresolved, request clarification |
| NLP-11 | Hinglish | “Block B mein pump or fan dono issue hain.” | Multiple issue/asset ambiguity, request one issue at a time |
| NLP-12 | English | “Air conditioner at Block A ground floor is broken and urgent.” | Known AC, HIGH suggestion, confirm issue type |
| NLP-13 | Hindi | “ब्लॉक बी दूसरी मंजिल, पंप में रिसाव।” | Known pump, leakage |
| NLP-14 | Hinglish | “Warehouse C ki bay light flicker kar rahi hai.” | Known light, electrical category |
| NLP-15 | English | Silence/background hiss/no intelligible speech | No ticket; rerecord |

**Evaluation protocol:**

1. Save consented voice recordings, not third-party phone calls. Capture language, accent/code-mix and noise condition as nonidentifying metadata.
2. For every recording, label expected `location_code`, `asset_code`, `issue_category`, `priority_cue` and whether `needs_review` must be true.
3. Run all clips through the **actual Gnani STT model chosen for the release**, not a fixed transcript fixture.
4. Compute transcript word/character error rates **only** where an appropriate reference and tokenization method are defined; be clear about code-mixed and script effects.
5. For extraction, calculate per-field exact-match accuracy and complete-case correctness; include a confusion table for missing/ambiguous fields.
6. Make the acceptance threshold a **target** (for example 12/15 complete cases, with all unsafe ambiguity cases blocked), not an invented observed result.
7. Publish a concise validation summary: sample count, actual pass counts, model name, limitations and failure examples.

---

## 15. Short-horizon schedule: November 8–10, 2026 (IST)

**Date context:** This plan was prepared November 8, 2026, so the contest is time constrained. These are **recommended timeboxes**, not promises of completion or background processing. Reorder based on available time and work already done.

| Local window | Work package | Must exit with | If behind schedule |
|---|---|---|---|
| **Nov 8, first work block** | WBS-00/01: registration, API access, real STT spike | **G1 verified**, actual Gnani request ID | Stop adding features; resolve provider access |
| **Nov 8, next block** | WBS-02: repo, DB, auth, seed, basic pages | App + schema + two roles | Drop advanced auth UI design; keep secure role verification |
| **Nov 8–9** | WBS-03: recorder, safe conversion, Gnani-backed transcription | Voice→transcript from browser | Skip live streaming and extra languages |
| **Nov 9, primary block** | WBS-04: parser, confirmation, idempotent ticket save | **G2 vertical slice** | Manual user correction of parsed fields is acceptable; Gnani voice cannot be mocked |
| **Nov 9, later block** | WBS-05: supervisor view, assignment, status history | End-to-end operations | Use simple functional table rather than complex analytics |
| **Nov 10, early** | WBS-07: negative tests, deployment, secret scan | G3 release candidate | Drop P1 TTS/duplicates if P0 not robust |
| **Nov 10, before deadline** | WBS-08: record truthful public demo, post, nominate link, submit | **G4 + G5 completion** | Prioritize official submission over cosmetic enhancements |

### 15.1 Milestone order / critical path

`Account access → genuine Prisma call → backend upload/conversion → persisted intake → extraction/review → work-order transaction → supervisor workflow → deployment test → public demo → official form`.

**Parallelizable items for a two-person team:**
- Contributor A: Prisma adapter, audio handling, DB/work-order integrity, integration tests.
- Contributor B: React recorder/review/queue UI, UX states, demo preparation, E2E.
- Integrate contracts early; both contributors verify the entire flow and prepare to explain their own changes. Do not misrepresent contributions.

### 15.2 Strict cut lines

- If G1 is not passed: no claim of a genuine Gnani application; prioritize fixing access.
- If G2 is incomplete by Nov 9: **drop TTS, duplicate scoring, charts, language expansions**; ship the core.
- If end-to-end is unstable Nov 10: stop adding capabilities; run fault tests and repair.
- If deployment is unreliable: record the genuine reproducible local build with visible model evidence, as permitted by the challenge's working demo requirement; do not claim a live deployed URL exists. Still prepare the public video and official submission, ensuring actual Gnani calls work.
- Regardless of feature count: final public post and official form must be completed **before the cutoff**.

---

## 16. CI/CD, production readiness and release gate

### 16.1 Local developer commands (template — adjust to actual dependencies)

```bash
# API setup (example, after Python dependency versions are locked)
cd api
python -m venv .venv
source .venv/bin/activate             # Windows: .venv\Scripts\activate
pip install -e '.[dev]'
alembic upgrade head
python -m app.scripts.seed_demo       # or: python scripts/seed_demo.py
uvicorn app.main:app --reload

# Web setup (separate terminal)
cd web
npm ci
npm run dev

# Validation (adjust package scripts to actual implementation)
cd api
pytest -q
ruff check .
# mypy app OR pyright, if configured

cd ../web
npm run lint
npm run typecheck
npm run test
npm run build
npx playwright test
```

**Note:** The example `app.scripts.seed_demo` import path works only if the final repository places the script as a package module. Use the actual path implemented; do not leave dead commands in the README.

### 16.2 CI pipeline (suggested sequence)

1. Install pinned Python and Node versions; restore controlled cache.
2. Static format/lint, TypeScript check, Python lint/typecheck.
3. Unit tests: parser, validation, workflow, provider contract via explicit fixtures.
4. Start PostgreSQL service; apply Alembic migrations; run DB/API integration tests.
5. Web build + browser E2E with test backend/fixture provider (clearly isolated).
6. Secret scan, dependency scan and check for committed raw media.
7. Publish build artifact or deploy on `main` only after all checks pass.
8. Run **separate, manual, credit-consuming live Gnani smoke** with approved key and safe audio (not on every push).
9. Gate production release against actual live test results and the P0 checklist; tag version.

### 16.3 Deployment and smoke procedure

- [ ] Managed PostgreSQL created; backups enabled; DB connection securely configured.
- [ ] Python service installed with `ffmpeg/ffprobe`; persistent volume not required for ephemeral audio.
- [ ] Host memory/CPU/time limits can process one short recording without worker termination.
- [ ] Secrets attached to backend host only; no `.env` in public static frontend build.
- [ ] `CORS_ORIGINS` matches exact HTTPS frontend origin; authentication flow works over HTTPS.
- [ ] Database migration applied; seed performed once without duplicate users/assets.
- [ ] Backend `/health/ready` succeeds; UI works on desktop and mobile.
- [ ] Browser grants microphone on secure origin (`https://` or permitted `localhost` development).
- [ ] Upload captured audio; provider model/request ID and transcript verified live.
- [ ] Confirm ticket, assign, resolve, refresh; DB states remain correct.
- [ ] TTS audio playback verifies content type if feature enabled.
- [ ] Cloud logs do not disclose token, audio, full transcripts or passwords.
- [ ] Deployment rollback/restart has been tried; DB data survives.

### 16.4 Formal release checklist (G3)

```text
Release: v1.0.0-submission
Commit SHA: __________________________
UTC/IST timestamp: ____________________
Registered account access confirmed: [ ]
Gnani production STT verified (real request ID): [ ]
Schema migration and seed: [ ]
Role-based authorization: [ ]
Audio conversion and input limits: [ ]
Extraction + review and confirmation gate: [ ]
Atomic work-order create + audit event: [ ]
Idempotency + concurrency negative tests: [ ]
Supervisor assignment/status workflow: [ ]
Complete E2E browser smoke: [ ]
Secrets/PII scan: [ ]
No known blocking bugs: [ ]
Readme / setup documented: [ ]
Decision: RELEASE / HOLD
Release approver (self/team): __________
```

**A release is not approved merely because an AI coding assistant reports success.** The above checks must be independently observed or executed.

---

## 17. Risk register and mitigation triggers

Rank risks daily. Ratings here are preliminary and can be updated based on actual test findings.

| Risk ID | Risk | Impact / likelihood | Trigger | Mitigation / contingency | Owner |
|---|---|---|---|---|---|
| R-01 | Gnani key, account scope or credits unavailable | Critical / Medium | Real spike returns 401/402/403 | Resolve official account support immediately; never fake a pass | Lead |
| R-02 | Browser WebM unsupported by STT | High / High | 400 unsupported media | Server-side ffmpeg to WAV + metadata checks | Backend |
| R-03 | Multilingual/code-mixed ASR errors | Medium / High | Wrong terminology | Test short clips; selected locale; corrections; optional model experiment | AI integration |
| R-04 | Parser maps wrong equipment | High / Medium | Ambiguous aliases | Catalog + evidence + human verification | Backend |
| R-05 | Duplicate ticket from retries | High / Medium | Repeated click/network retry | Idempotency and unique intake constraint | Backend |
| R-06 | TTS beta/unavailable | Low / Medium | TTS fails | Keep optional; text-only acknowledgment | Backend |
| R-07 | Hosting instability/cold starts | High / Medium | Demo service timeout | Early deployment and real smoke; record local genuine run if needed | DevOps |
| R-08 | Time lost on nonessential features | Critical / High | G2 behind schedule | Enforce P0 cut line; remove P1/P2 | Lead |
| R-09 | Secret/PII leaks into post or GitHub | Critical / Medium | Credential visible in screen/log | Redaction, review, rotate compromised key | All |
| R-10 | Submission post lacks tags or form nomination | Critical / Medium | Final check reveals missing post/form | O-06–O-10 checklist and explicit confirmation | Lead |
| R-11 | Misleading model claims | Critical / Medium | Demo uses fixture/other model labeled Gnani | Accurate provenance and real STT gate | All |
| R-12 | Teammate contribution unclear | Medium / Medium | Form lacks ownership clarity | PR/commit log + individual contribution paragraphs | Team |
| R-13 | Wrong database migrations erase state | High / Low | Schema drift or destructive migration | Backup and migration rehearsal | Backend |
| R-14 | Real audio or identifiable data in demo | Critical / Medium | Real customer content added | Synthetic scripts only, consent, review | All |

### 17.1 Defect severity policy

- **Critical:** false Gnani proof, exposed credentials, broken work-order creation, failure to submit, major unauthorized data access → **release blocked**.
- **High:** cross-worker data leak, duplicate work orders, invalid state updates, missing Gnani model evidence → **release blocked**.
- **Medium:** Tamil recognition poor on one test, TTS unavailable, duplicate warnings noisy → may ship only if clearly disclosed and not in claimed P0 path.
- **Low:** decorative styling, small layout polish → never prioritize over mandatory release/submission.

---

## 18. Suggested Codex / AI-agent implementation protocol

If implementing with AI coding agents, use **one verifiable vertical slice at a time**. Avoid instructing the agent to “build the whole project” without explicit proof requirements. The prompts below are implementation aids, not a substitute for testing.

### 18.1 Repository contract for coding agents (`AGENTS.md` suggested)

```markdown
# FieldSaarthi Agent Rules

1. Read the roadmap and reference requirement IDs before changing files.
2. Work one WBS item at a time; don't implement P1/P2 until P0 gates pass.
3. Preserve and test the genuine Gnani REST adapter; production output must
   never use fake/mocked transcripts or preloaded successful responses.
4. Keep GNANI_API_KEY_ID server-side; never expose it in React/console/logs.
5. Do not invent asset IDs, locations, model capabilities, scores or API fields.
6. Use Pydantic/SQLAlchemy constraints and real DB transaction boundaries.
7. For new endpoints, update schema, tests, and README/OpenAPI docs together.
8. For every change, report: requirement IDs, files, test commands/results,
   remaining issues and whether real Gnani tests were run.
9. Don't claim tests passed unless executed; don't claim deployment unless verified.
10. Never alter existing verified contracts without an explicit ADR and regression test.
```

### 18.2 Task slices and prompt starters

**Agent task A — Gnani adapter (FR-06–09)**

> Implement a typed FastAPI Gnani Prisma v2.5 REST adapter to `POST https://api.vachana.ai/stt/v3`, using backend-only `X-API-Key-ID`, multipart WAV + selected language, parsing nonempty `transcript`, real `model` and `request_id`. Create test fixtures for nonempty, empty, auth, quota, rate-limit and timeout responses. Do not simulate success in production. Return changed files, test results and live-test requirements.

**Agent task B — Audio handling (FR-04–05)**

> Implement React `MediaRecorder` upload and FastAPI audio safety validation/conversion. Browser WebM must be converted with ffmpeg to 16k mono WAV if needed; enforce 25-second UI soft cap and provider 30-second maximum; use safe subprocess, temporary cleanup, typed errors. Include corrupt/oversized/unsupported tests. Never put API keys in frontend.

**Agent task C — Orders and verification (FR-10–19)**

> Implement catalog-backed multilingual alias extraction with evidence spans, explicit review UI, required location/asset/description validation, one-to-one intake/order relationship, transactional creation and audit event, idempotency-key handling and test cases. Preserve raw Gnani text independently of user correction. Do not invent catalog values.

**Agent task D — Supervisor workflow (FR-20–22, FR-25)**

> Implement role-verified ticket queue, assignment, priority, allowed status transitions, optimistic locking and immutable audit view. Write negative RBAC, stale-version and forbidden-transition tests. UI must display server state, not local simulations.

**Agent task E — Production gate (NFR/O IDs)**

> Run exact lint, type, unit, integration and E2E checks; report commands and outputs. Review client bundle and repository for secrets, smoke deployed HTTPS capture with real Gnani integration, and generate release evidence. Clearly mark checks not run; do not mark release approved automatically.

### 18.3 Completion report required from every agent task

```text
Task / Requirement IDs:
Files changed:
Data/contract changes:
Tests executed (actual commands and results):
Live Gnani call executed? yes/no (never include key):
Evidence path / screenshot:
Security/privacy considerations:
Unresolved issues and severity:
Recommended next WBS item:
```

---

## 19. Public demonstration plan and technical proof package

### 19.1 Show exactly what is real

- Use live **new microphone recording** during capture; do not silently insert a prepared transcript.
- Show **Gnani-provided transcript** and real model/request provenance, but not key/session token.
- Show the extraction/review stage, including human confirmation.
- Show the newly created work order, real ID and persisted queue after refresh.
- Show assignment and status update from supervisor context.
- Optional: play live or explicitly generated-and-stored Gnani Timbre WAV when verified.
- Do not imply asset recognition, priority policy or ticket persistence were performed by Gnani; explain that Gnani supplies the speech model and the app supplies workflow logic.

### 19.2 60-second public demo shot list (the Demo Day Drop category is specifically 60 seconds)

| Timestamp | Screen/action | Narration focus |
|---|---|---|
| 0–06s | Worker faces a reporting issue | “Field fault reports get lost in informal speech.” |
| 06–19s | Select Hindi, speak fresh short report, submit audio | “FieldSaarthi captures a natural Indian-language report using Gnani Prisma.” |
| 19–32s | Real transcript, extracted fields, corrections if needed | “The system maps speech into known assets and requires verification.” |
| 32–43s | Confirm work order, show server ID and queue after refresh | “This becomes a durable, traceable work order.” |
| 43–53s | Supervisor assigns / advances status | “Supervisors can act on it and track responsibility.” |
| 53–60s | Optional Timbre audio, provenance and tagline | “Real speech intelligence linked to a complete operational outcome.” |

Ensure pacing reflects actual API latency. Editing a genuine recorded demonstration for length is acceptable, but never splice outputs to imply nonexistent integration or fake workflow steps. If provider latency is longer than the slot, capture a full honest run and edit transparently; no fabricated response screens.

### 19.3 Longer technical demonstration (recommended evidence, not mandatory separate official video)

1. Explain architecture (frontend → backend → Gnani STT → parser → review → DB → dashboard).
2. Show real model string and request ID in response/evidence panel.
3. Rerecord with missing asset/location and show confirmation **blocked**.
4. Show duplicate idempotency attempt (same key yields same ticket).
5. Switch supervisor role, assign, progress to resolved; show immutable event history.
6. Simulate TTS failure safely to show work order survives (if TTS built).
7. Mention limitations honestly: language selected for v2.5, short REST clips, human verification, synthetic demo inventory.

### 19.4 Submission project description template

**Title:** FieldSaarthi AI — Multilingual Voice-to-Action Intelligence for Field Operations  
**Problem:** Frontline maintenance issues reported verbally are difficult to structure, assign and audit reliably.  
**Users:** Indian facility workers, supervisors and maintenance coordinators.  
**Solution:** Workers speak short reports; Gnani Prisma transcribes; FieldSaarthi validates catalog-backed asset/location fields, requires review and creates traceable work orders; supervisors manage assignments and resolution. Optional Gnani Timbre speaks acknowledgment.  
**Gnani models/APIs actually used:** [Fill **only** verified models, e.g., `Prisma v2.5 STT` and/or `Timbre v2.5 TTS`].  
**Verified functional demo:** [Describe flows actually demonstrated and tested].  
**Individual contributions:** [Fill exact person → responsible code, tests, UX, deployment; do not use vague “built everything together” if inaccurate].  
**Limitations:** [Short REST audio, synthetic data, selected-language mode, or any feature not yet live].  
**Demo/public URL(s):** [Insert publicly accessible links].

### 19.5 Public post content checklist

- [ ] Project name and actual value proposition are understandable to nonspecialists.
- [ ] Video shows a **working**, authentic Gnani-based application.
- [ ] Model/API used is named accurately.
- [ ] Gnani AI's actual official account is tagged on the platform.
- [ ] Both exact hashtags present: `#GnaniAI` and `#GreatIndianAIInternshipChallenge`.
- [ ] Video and text avoid real private data, credential leaks and fabricated results.
- [ ] Post is public before the form is submitted.
- [ ] Canonical post URL copied and nominated in the official submission form.
- [ ] No purchased, automated or swap-based engagement.

### 19.6 Official final-form checklist

**The final form is supplied to the registered email.** Its live fields are authoritative; this is a preparation list, not an invented replica of the exact UI.

- [ ] Registration/identity/team details as requested.
- [ ] Project title and concise problem statement.
- [ ] Target users and outcome.
- [ ] Gnani model names and actual purpose of each integration.
- [ ] Working video/showcase attachment or video URL in whichever format the form actually requests.
- [ ] Individual contributor descriptions.
- [ ] Public LinkedIn URL if posted; public X URL if posted (one nominated post per used platform).
- [ ] Any additional form fields completed truthfully; no empty required inputs.
- [ ] Submission made by **10 Nov 2026, 11:59 PM IST** with buffer.
- [ ] Official confirmation or submission acknowledgment saved.

**Remember:** Neither an attractive README nor a public LinkedIn post alone completes the application. The official submission form must be finalized.

---

## 20. Post-submission technical interview preparation

Because Gnani interviews shortlisted contributors separately, keep a concrete explanation ready for:

1. **Why Gnani?** Demonstrate that the application relies on Prisma for Indian-language speech recognition and optionally Timbre for spoken feedback; distinguish this from ordinary transcription alternatives.
2. **What is the true model input/output contract?** Explain multipart upload, language selection, limits, `request_id`, `model`, empty transcripts and error shapes.
3. **How did you solve browser audio compatibility?** Explain WebM/Opus recording, ffprobe validation and WAV conversion, resource limits.
4. **What happens if Gnani fails?** Explain bounded retry and explicit failure, never fabricated results.
5. **How do you prevent wrong work orders?** Explain known inventory, field evidence, missing/ambiguous flags and user confirmation.
6. **How do you prevent duplicates and races?** Explain idempotency, `UNIQUE(intake_id)` and transaction locking/versioning.
7. **What is the data model?** Explain why raw transcript and edited transcript are separate, and why audit events are immutable.
8. **How did you measure accuracy?** Present real 15-utterance results and distinguish measured results from targets.
9. **What is the threat model?** Discuss server-only API keys, auth/RBAC, audio parser hardening, synthetic data and data retention.
10. **What would you scale next?** Mention real telephony/streaming after proving performance, but be clear they were out of scope for MVP.
11. **What did YOU personally implement?** Identify commits, modules, tradeoffs, tests, defects found and fixes; every teammate must answer independently.
12. **Why lightweight CMMI?** Traceable requirements, monitoring, quality gates and release evidence are useful; full certification/process overhead was neither required nor suitable for the short challenge.

---

## 21. Evidence index and final handoff package

Deliver these repository artifacts to enable a reviewer to reproduce or inspect the solution. The official challenge does **not** require every extra document here; they are a recommended professional engineering package.

| Artifact | Path | Content | Officially mandatory? |
|---|---|---|---|
| Functional working application | deployed URL or reproducible run instructions | Genuine Gnani-backed workflow | **Yes, working app** |
| Public working demo | LinkedIn/X media URL | Working video and required hashtags | **Yes** |
| Written project explanation | `docs/submission/project-summary.md` | Problem, users, model details, contributions | **Yes, in form** |
| Nominated social URL(s) | final form | Public post links | **Yes** |
| Source code | GitHub repo | Actual application implementation | Recommended |
| README | `README.md` | Setup, features, limitations, quick demo | Recommended |
| Architecture and ADRs | `docs/architecture.md`, `docs/adrs/` | Technical design and decisions | Recommended |
| RTM | `docs/rtm.md` | Requirements → tests → evidence | Recommended |
| Test evidence | `docs/evidence/` | Sanitized reports and real provider metadata | Recommended |
| Risk register | `docs/risks.md` | Severity, mitigation, owners | Recommended |
| Release proof | `docs/evidence/release-gate.md` | CI, smoke, tag, approvals | Recommended |
| Technical demo notes | `docs/submission/demo-script.md` | Showcase and interview walkthrough | Recommended |
| Operational runbook | `docs/operations.md` | Start/stop, error response, rollback | Recommended |

### 21.1 Suggested README outline

1. Project overview and actual user problem.
2. Gnani models used, why and **where in the code** they are invoked.
3. Architecture diagram and stack.
4. Features actually implemented (separate planned vs done).
5. Prerequisites and environment variables (**placeholders only**).
6. Database migration/seed instructions.
7. Local run instructions and deployment link, if verified.
8. Test commands, measured results and known limitations.
9. Responsible-use/privacy note and synthetic demo data disclosure.
10. Screenshots, public video, attribution and contributors.

---

## 22. Master execution checklist (release and contest completion)

### Access and compliance
- [ ] O-01 / O-02 / O-03 eligibility, registration and team verified.
- [ ] Gnani console, key scope and available credits confirmed.
- [ ] Official deadline and form access confirmed.

### Build / functional core
- [ ] FR-06 real Prisma call; model/request ID captured.
- [ ] FR-04 / FR-05 real browser recording, conversion and short-audio limit.
- [ ] FR-10–FR-15 known catalog extraction, editable review, blocking validation.
- [ ] FR-16–FR-19 durable idempotent order and audit transaction.
- [ ] FR-20–FR-22 supervisor assignment, valid states, persistent dashboard.
- [ ] Genuine failure cases work; no fake transcript/provider success.

### Quality and release
- [ ] Unit, API/DB, UI and E2E checks executed and reported.
- [ ] Critical/high issues resolved; security and synthetic-data checks pass.
- [ ] Real deployed or reproducible live Gnani smoke verified.
- [ ] Release version/tag and sanitized proof recorded.

### Submission
- [ ] Public actual-app video created.
- [ ] Accurate model names and contributors described.
- [ ] Required two hashtags and tag included in live post.
- [ ] Official form completed with nominated URL(s).
- [ ] Form confirmation saved **before November 10, 2026 at 11:59 PM IST**.

---

## 23. Reference index and verification notes

**Official challenge sources (rechecked 08 November 2026):**
1. Gnani Internship Challenge: https://www.gnani.ai/internship
2. Gnani Internship registration and programme terms: https://www.gnani.ai/great-indian-ai-internship-registration-form
3. Gnani challenge blog: https://www.gnani.ai/resources/blogs/great-indian-ai-internship-challenge-2026

**Official engineering sources:**
4. API quick start (Prisma default/version and TTS examples): https://docs.gnani.ai/api/introduction/quick-start
5. STT REST — provider params, limits, responses, error types: https://docs.gnani.ai/api/STT/speech-to-text
6. TTS REST — inference payload and binary response: https://docs.gnani.ai/api/TTS/tts-inference
7. Timbre voices/model version catalog: https://docs.gnani.ai/api/TTS/available-voices
8. Error handling / authentication/rate limits: https://docs.gnani.ai/api/introduction/errors
9. Gnani API platform: https://app.gnani.ai/voice

**What must still be empirically verified by the developer:**
- Actual account eligibility, API key activation, permissions, credits, any model/version entitlement.
- Actual live transcript quality on your particular voice clips/languages.
- TTS behavior under your key, chosen voice and exact provider version.
- Your selected cloud platform's runtime, ffmpeg support, cold starts and microphone behavior.
- Whether the registration email's final form requests any extra fields or media format; follow that actual form rather than inventing inputs.
- Actual test pass rates, measurements and uptime after building and deploying.

**Final decision:** Prioritize the verified Gnani STT → human-reviewed structured work order → real persisted supervisor workflow. An optional spoken acknowledgment and duplicate warning make the product richer, but never at the cost of a complete truthful, stable submission. **Evidence before claims; official form before deadline.**
