# Graph Report - .  (2026-11-10)

## Corpus Check
- 192 files · ~143,064 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 616 nodes · 848 edges · 95 communities detected
- Extraction: 62% EXTRACTED · 38% INFERRED · 0% AMBIGUOUS · INFERRED: 324 edges (avg confidence: 0.79)
- Token cost: unavailable (semantic extraction agents did not return token telemetry)

## Community Hubs (Navigation)
- [Backend Workflow Regression Tests](#backend-workflow-regression-tests)
- [Authentication And Intake Routes](#authentication-and-intake-routes)
- [Architecture Decision Records](#architecture-decision-records)
- [Gnani STT And Timbre Adapters](#gnani-stt-and-timbre-adapters)
- [Recording And Browser Evaluation](#recording-and-browser-evaluation)
- [Release And Hosted Evidence](#release-and-hosted-evidence)
- [Transactional Orders And Audit Models](#transactional-orders-and-audit-models)
- [Audio Contracts And Backup Drill](#audio-contracts-and-backup-drill)
- [Catalog Extraction And Provenance](#catalog-extraction-and-provenance)
- [Deployment Configuration And CI](#deployment-configuration-and-ci)
- [Database Workflow Integration Tests](#database-workflow-integration-tests)
- [Typed API Response Schemas](#typed-api-response-schemas)
- [Frontend API And Navigation](#frontend-api-and-navigation)
- [Backend Domain Architecture](#backend-domain-architecture)
- [Typed Commands And Sample Recorder](#typed-commands-and-sample-recorder)
- [Repository Privacy Guard](#repository-privacy-guard)
- [Worker And Supervisor UI](#worker-and-supervisor-ui)
- [Operations And Evaluation Scripts](#operations-and-evaluation-scripts)
- [Judge Access Migration And Fixtures](#judge-access-migration-and-fixtures)
- [Application Entrypoints And Vite](#application-entrypoints-and-vite)
- [Alembic Schema Migrations](#alembic-schema-migrations)
- [Unit Regression Tests](#unit-regression-tests)
- [Gnani And Audio Contract Tests](#gnani-and-audio-contract-tests)
- [Immutable Database Boundaries](#immutable-database-boundaries)
- [Manual Intake Provenance Migration](#manual-intake-provenance-migration)
- [Health And Catalog Access Tests](#health-and-catalog-access-tests)
- [Typed API Command And Response Models](#typed-api-command-and-response-models)
- [SQLAlchemy Session Dependency](#sqlalchemy-session-dependency)
- [Migration-First Server Startup](#migration-first-server-startup)
- [Request ID Logging Tests](#request-id-logging-tests)
- [Accessible Manual Report Page](#accessible-manual-report-page)
- [Work Order Queue Filters](#work-order-queue-filters)
- [Authentication And Authorization Core](#authentication-and-authorization-core)
- [Request Stage Telemetry](#request-stage-telemetry)
- [Live Gnani Smoke Workflow](#live-gnani-smoke-workflow)
- [Timbre Text To Speech](#timbre-text-to-speech)
- [Browser End To End Workflow](#browser-end-to-end-workflow)
- [Shared Pytest Fixtures](#shared-pytest-fixtures)
- [Hash Route Navigation](#hash-route-navigation)
- [Runtime Settings](#runtime-settings)
- [Typed Application Errors](#typed-application-errors)
- [Audio And Request Limits](#audio-and-request-limits)
- [Provider Integration Package](#provider-integration-package)
- [Demo And Judge Authentication](#demo-and-judge-authentication)
- [Backend Application Package](#backend-application-package)
- [Environment Configuration](#environment-configuration)
- [Gnani Integration Package](#gnani-integration-package)
- [Pytest Configuration](#pytest-configuration)
- [Vite Development Configuration](#vite-development-configuration)
- [Git Text And Binary Rules](#git-text-and-binary-rules)
- [Project Change Log](#project-change-log)
- [Alembic Configuration](#alembic-configuration)
- [Python Dependencies And Tooling](#python-dependencies-and-tooling)
- [FFmpeg Type Stub](#ffmpeg-type-stub)
- [Locked Python Dependencies](#locked-python-dependencies)
- [Participant Microphone Evidence](#participant-microphone-evidence)
- [Hosted Runtime Evidence](#hosted-runtime-evidence)
- [Gnani Documentation Source Index](#gnani-documentation-source-index)
- [Frontend Lint Rules](#frontend-lint-rules)
- [Frontend HTML Entrypoint](#frontend-html-entrypoint)
- [Web Package Metadata](#web-package-metadata)
- [Web Dependency Lockfile](#web-dependency-lockfile)
- [Base Interface Styles](#base-interface-styles)
- [Application Theme Styles](#application-theme-styles)
- [Frontend App TypeScript Settings](#frontend-app-typescript-settings)
- [Frontend TypeScript Settings](#frontend-typescript-settings)
- [Vite TypeScript Settings](#vite-typescript-settings)
- [User-Owned Submission Gate](#user-owned-submission-gate)
- [Judge Queue Regression Screenshot](#judge-queue-regression-screenshot)
- [Resolved Workflow Browser Screenshot](#resolved-workflow-browser-screenshot)
- [Human Transcript Review Screenshot](#human-transcript-review-screenshot)
- [Worker And Supervisor Login Screenshot](#worker-and-supervisor-login-screenshot)
- [Voice Report Capture Screenshot](#voice-report-capture-screenshot)
- [Transcript Correction Screenshot](#transcript-correction-screenshot)
- [Persisted Work Order Screenshot](#persisted-work-order-screenshot)
- [Resolved Audit Timeline Screenshot](#resolved-audit-timeline-screenshot)
- [Supervisor Queue Screenshot](#supervisor-queue-screenshot)
- [Mobile Supervisor Queue Screenshot](#mobile-supervisor-queue-screenshot)
- [Saved Ticket TTS Control Screenshot](#saved-ticket-tts-control-screenshot)
- [Accessible Work Order Detail Screenshot](#accessible-work-order-detail-screenshot)
- [Accessible Sign-In Screenshot](#accessible-sign-in-screenshot)
- [Accessible Desktop Queue Screenshot](#accessible-desktop-queue-screenshot)
- [Accessible Mobile Queue Screenshot](#accessible-mobile-queue-screenshot)
- [Accessible Desktop Report Screenshot](#accessible-desktop-report-screenshot)
- [Accessible Mobile Report Screenshot](#accessible-mobile-report-screenshot)
- [Public Judge Dashboard Screenshot](#public-judge-dashboard-screenshot)
- [Approved Report Provenance Screenshot](#approved-report-provenance-screenshot)
- [Mobile Judge Detail Screenshot](#mobile-judge-detail-screenshot)
- [Judge Demo Login Screenshot](#judge-demo-login-screenshot)
- [Solution Pitch Preview](#solution-pitch-preview)
- [Waveform Favicon](#waveform-favicon)
- [Shared SVG Icon Symbols](#shared-svg-icon-symbols)
- [Layered Hero Illustration](#layered-hero-illustration)
- [Vite Logo Asset](#vite-logo-asset)
- [Graph Export Artifacts](#graph-export-artifacts)

## God Nodes (most connected - your core abstractions)
1. `login()` - 32 edges
2. `AppError` - 24 edges
3. `fixture_intake()` - 24 edges
4. `payload()` - 22 edges
5. `stable()` - 21 edges
6. `GnaniError` - 18 edges
7. `extract()` - 18 edges
8. `FieldSaarthi system architecture` - 17 edges
9. `Database-backed workflow and security coverage` - 16 edges
10. `Gnani speech processing` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Bounded decoding of untrusted media; original bytes never persist after conversi` --uses--> `AppError`  [INFERRED]
  api\app\services\audio.py → api\app\core\errors.py
- `main()` --calls--> `now()`  [INFERRED]
  api\scripts\backup_drill.py → api\app\db\models.py
- `test_paid_response_survives_parser_failure_without_repeating_call()` --calls--> `evaluate()`  [INFERRED]
  api\tests\unit\test_audio_evaluation.py → api\scripts\evaluate_audio.py
- `WBS-02 initial schema and database-enforced provenance/audit protection.` --uses--> `Base`  [INFERRED]
  api\alembic\versions\0001_foundation.py → api\app\db\models.py
- `main()` --calls--> `upgrade()`  [INFERRED]
  api\tests\browser\workflow_check.py → api\alembic\versions\0004_judge_demo.py

## Communities

### Backend Workflow Regression Tests
Cohesion: 0.09
Nodes (42): stable(), test_database_rejects_invalid_rows_directly(), test_search_injection_is_literal_and_preserves_ownership_and_tables(), test_manual_input_rejects_blank_oversized_or_forged_provenance(), test_manual_route_is_reporter_only(), test_manual_text_is_explicit_and_has_no_provider_provenance(), test_cookie_refresh_and_csrf_guard(), test_corrupt_and_long_audio_never_calls_provider() (+34 more)

### Authentication And Intake Routes
Cohesion: 0.07
Nodes (32): demo_capability(), judge_demo(), judge_demo_enabled(), login(), me(), session_status(), user_json(), users() (+24 more)

### Architecture Decision Records
Cohesion: 0.05
Nodes (42): ADR-001: React, Vite and TypeScript, ADR-002: Typed FastAPI REST backend, ADR-003: PostgreSQL and transactional work orders, ADR-004: Short REST audio with bounded decoding, ADR-005: Verified Prisma v2.5 baseline, ADR-006: Deterministic catalog suggestions and human review, ADR-007: Timbre after work-order commit, ADR-008: Synthetic data and temporary audio (+34 more)

### Gnani STT And Timbre Adapters
Cohesion: 0.08
Nodes (25): GnaniError, GnaniSpeechClient, ProviderResult, FR-06..09: real Prisma v2.5 REST adapter. No production fixture path. Contract:, Only safe application codes leave the integration boundary., Use one shared instance per process; its semaphore serializes provider calls., Transcription, acknowledgment() (+17 more)

### Recording And Browser Evaluation
Cohesion: 0.09
Nodes (31): main(), Non-billable browser, responsive layout and axe accessibility verification., update(), compare(), evaluate(), evaluate_cases(), main(), preflight() (+23 more)

### Release And Hosted Evidence
Cohesion: 0.06
Nodes (34): Catalog extraction and human confirmation, 15-recording result: 12 of 15 complete cases, Audio and workflow evaluation, genuine_gnani_distinct_human_recordings, genuine_gnani_distinct_human_recordings, Backend Dependency Audit, Accessibility, Live Browser Smoke (+26 more)

### Transactional Orders And Audit Models
Cohesion: 0.13
Nodes (22): WBS-02 initial schema and database-enforced provenance/audit protection., DeclarativeBase, Audit, Base, Idempotency, Intake, Order, User (+14 more)

### Audio Contracts And Backup Drill
Cohesion: 0.07
Nodes (18): normalize_audio(), Bounded decoding of untrusted media; original bytes never persist after conversi, main(), Create a private pg_dump and restore to a new isolated scratch database.  Never, test_paid_response_survives_parser_failure_without_repeating_call(), T-AUD-02: exercise actual FFmpeg WebM/Opus decoding, with test-only audio., test_actual_webm_opus_converts_to_provider_pcm_wav(), call() (+10 more)

### Catalog Extraction And Provenance
Cohesion: 0.11
Nodes (24): extract(), matches(), normalize(), normalized_source(), Catalog-backed, Unicode-aware suggestions. Unknown facts stay unresolved., Search normalization with offsets into the untouched Unicode source., source_spans(), Asset (+16 more)

### Deployment Configuration And CI
Cohesion: 0.1
Nodes (13): Deployment and continuous integration, FieldSaarthi agent rules, Challenge compliance - WBS-00.1 / O-01..12, Deployment package - Render submission demo, Github Publication, Deployment, Render Schema Validation, GitHub configuration - WBS-00.5 (+5 more)

### Database Workflow Integration Tests
Cohesion: 0.12
Nodes (17): Database-backed workflow and security coverage, api/tests/integration/conftest.py, api/tests/integration/test_extraction_provenance.py, api/tests/integration/test_final_roadmap_guards.py, api/tests/integration/test_foundation.py, api/tests/integration/test_hindi_catalog_variants.py, api/tests/integration/test_intake_sources.py, api/tests/integration/test_intakes.py (+9 more)

### Typed API Response Schemas
Cohesion: 0.23
Nodes (15): BaseModel, AssetCandidate, AssetResponse, AuditResponse, EvidenceSpan, IntakeResponse, LocationResponse, LoginResponse (+7 more)

### Frontend API And Navigation
Cohesion: 0.13
Nodes (5): api(), ApiError, async(), navigate(), async()

### Backend Domain Architecture
Cohesion: 0.13
Nodes (15): Bounded audio normalization, Evidence-backed transcript extraction, Gnani Prisma STT integration, Persistence and domain model, Transactional work-order service, Voice and manual intake endpoints, Work-order endpoints, api/app/db/models.py (+7 more)

### Typed Commands And Sample Recorder
Cohesion: 0.24
Nodes (10): Assignment, Command, Confirm, Login, ManualIntake, PriorityChange, Review, StatusChange (+2 more)

### Repository Privacy Guard
Cohesion: 0.3
Nodes (10): forbidden_path(), git(), historical_paths(), inspect_content(), main(), NFR-04/05: scan all reachable Git history for private paths, raw media and key s, test_deleted_forbidden_path_with_identical_safe_blob_is_still_found(), test_key_signatures_and_nonplaceholder_assignments_are_blocked() (+2 more)

### Worker And Supervisor UI
Cohesion: 0.17
Nodes (12): Accessible manual-text reporting UI, Intake review and confirmation UI, Same-origin typed API client, Work-order details and audit UI, Work-order queue UI, Worker voice reporting UI, web/src/lib/api.ts, web/src/pages/Detail.tsx (+4 more)

### Operations And Evaluation Scripts
Cohesion: 0.22
Nodes (9): Operations and evaluation tooling, api/scripts/backup_drill.py, api/scripts/browser_quality.py, api/scripts/browser_smoke.py, api/scripts/evaluate_audio.py, api/scripts/hosted_reliability.py, api/scripts/record_sample.py, api/scripts/repository_guard.py (+1 more)

### Judge Access Migration And Fixtures
Cohesion: 0.33
Nodes (4): User-approved public read-only judge role and explicit report allowlist., upgrade(), accounts(), migrated_database()

### Application Entrypoints And Vite
Cohesion: 0.29
Nodes (7): Application entry and build configuration, api/app/__init__.py, api/app/main.py, api/app/seed.py, web/src/App.tsx, web/src/main.tsx, web/vite.config.ts

### Alembic Schema Migrations
Cohesion: 0.33
Nodes (6): Versioned PostgreSQL schema, api/alembic/env.py, api/alembic/versions/0001_foundation.py, api/alembic/versions/0002_immutable_boundaries.py, api/alembic/versions/0003_intake_sources.py, api/alembic/versions/0004_judge_demo.py

### Unit Regression Tests
Cohesion: 0.33
Nodes (6): Unit regression coverage, api/tests/unit/test_audio_evaluation.py, api/tests/unit/test_evaluation_failure_acknowledgement.py, api/tests/unit/test_extraction.py, api/tests/unit/test_repository_guard.py, api/tests/unit/test_seed_export.py

### Gnani And Audio Contract Tests
Cohesion: 0.4
Nodes (5): Provider and media contracts, api/tests/contract/test_audio_formats.py, api/tests/contract/test_gnani.py, api/tests/contract/test_smoke.py, api/tests/contract/test_tts.py

### Immutable Database Boundaries
Cohesion: 0.5
Nodes (1): Protect maintenance operations as well as row updates.

### Manual Intake Provenance Migration
Cohesion: 0.5
Nodes (1): Add explicit manual accessibility provenance without relabeling voice reports.

### Health And Catalog Access Tests
Cohesion: 0.67
Nodes (inventory): test_foundation.py, test_anonymous_catalog_is_denied(), test_live_and_ready()

### Typed API Command And Response Models
Cohesion: 0.67
Nodes (3): Typed API contracts, api/app/schemas/commands.py, api/app/schemas/responses.py

### SQLAlchemy Session Dependency
Cohesion: 1.0
Nodes (inventory): session.py, get_db()

### Migration-First Server Startup
Cohesion: 1.0
Nodes (1): One-worker deployment entry point. Run migrations before accepting traffic.

### Request ID Logging Tests
Cohesion: 1.0
Nodes (inventory): test_observability.py, test_http_event_is_emitted_with_request_id_and_without_query_secrets()

### Accessible Manual Report Page
Cohesion: 1.0
Nodes (inventory): onReady(), ManualReport.tsx

### Work Order Queue Filters
Cohesion: 1.0
Nodes (inventory): filter(), Orders.tsx

### Authentication And Authorization Core
Cohesion: 1.0
Nodes (2): Authentication and authorization, api/app/core/security.py

### Request Stage Telemetry
Cohesion: 1.0
Nodes (2): Request observability, api/app/core/telemetry.py

### Live Gnani Smoke Workflow
Cohesion: 1.0
Nodes (2): Provider smoke workflow, api/app/integrations/smoke.py

### Timbre Text To Speech
Cohesion: 1.0
Nodes (2): Gnani Timbre TTS integration, api/app/integrations/tts.py

### Browser End To End Workflow
Cohesion: 1.0
Nodes (2): Browser workflow coverage, api/tests/browser/workflow_check.py

### Shared Pytest Fixtures
Cohesion: 1.0
Nodes (2): Automated verification, api/tests/conftest.py

### Hash Route Navigation
Cohesion: 1.0
Nodes (2): Client-side route navigation, web/src/lib/navigation.ts

### Runtime Settings
Cohesion: 1.0
Nodes (2): Runtime configuration, api/app/core/config.py

### Typed Application Errors
Cohesion: 1.0
Nodes (2): Safe application errors, api/app/core/errors.py

### Audio And Request Limits
Cohesion: 1.0
Nodes (2): Resource bounds, api/app/core/limits.py

### Provider Integration Package
Cohesion: 1.0
Nodes (2): Provider integration, api/app/integrations/__init__.py

### Demo And Judge Authentication
Cohesion: 1.0
Nodes (2): Authentication and demo access, api/app/routers/auth.py

### Backend Application Package
Cohesion: 1.0
Nodes (inventory): __init__.py

### Environment Configuration
Cohesion: 1.0
Nodes (inventory): config.py

### Gnani Integration Package
Cohesion: 1.0
Nodes (inventory): __init__.py

### Pytest Configuration
Cohesion: 1.0
Nodes (inventory): conftest.py

### Vite Development Configuration
Cohesion: 1.0
Nodes (inventory): vite.config.ts

### Git Text And Binary Rules
Cohesion: 1.0
Nodes (inventory): .gitattributes

### Project Change Log
Cohesion: 1.0
Nodes (1): Changelog

### Alembic Configuration
Cohesion: 1.0
Nodes (inventory): alembic.ini

### Python Dependencies And Tooling
Cohesion: 1.0
Nodes (inventory): pyproject.toml

### FFmpeg Type Stub
Cohesion: 1.0
Nodes (inventory): imageio_ffmpeg.pyi

### Locked Python Dependencies
Cohesion: 1.0
Nodes (inventory): uv.lock

### Participant Microphone Evidence
Cohesion: 1.0
Nodes (1): Human Microphone Verification

### Hosted Runtime Evidence
Cohesion: 1.0
Nodes (1): Runtime Verification

### Gnani Documentation Source Index
Cohesion: 1.0
Nodes (1): Index

### Frontend Lint Rules
Cohesion: 1.0
Nodes (1): .Oxlintrc

### Frontend HTML Entrypoint
Cohesion: 1.0
Nodes (1): FieldSaarthi AI | Voice to action

### Web Package Metadata
Cohesion: 1.0
Nodes (1): fieldsaarthi-web

### Web Dependency Lockfile
Cohesion: 1.0
Nodes (1): fieldsaarthi-web

### Base Interface Styles
Cohesion: 1.0
Nodes (inventory): index.css

### Application Theme Styles
Cohesion: 1.0
Nodes (inventory): styles.css

### Frontend App TypeScript Settings
Cohesion: 1.0
Nodes (1): Tsconfig.App

### Frontend TypeScript Settings
Cohesion: 1.0
Nodes (1): Tsconfig

### Vite TypeScript Settings
Cohesion: 1.0
Nodes (1): Tsconfig.Node

### User-Owned Submission Gate
Cohesion: 1.0
Nodes (1): Official form remains user-reserved

### Judge Queue Regression Screenshot
Cohesion: 1.0
Nodes (1): Automated judge queue regression screenshot at 1440 pixels

### Resolved Workflow Browser Screenshot
Cohesion: 1.0
Nodes (1): Fixture-based end-to-end test showing resolved work order

### Human Transcript Review Screenshot
Cohesion: 1.0
Nodes (1): Fixture-based end-to-end test showing human transcript review

### Worker And Supervisor Login Screenshot
Cohesion: 1.0
Nodes (1): Worker and supervisor sign-in interface

### Voice Report Capture Screenshot
Cohesion: 1.0
Nodes (1): Worker voice report capture landing page

### Transcript Correction Screenshot
Cohesion: 1.0
Nodes (1): Worker transcript review and field correction form

### Persisted Work Order Screenshot
Cohesion: 1.0
Nodes (1): Persisted work order detail after report confirmation

### Resolved Audit Timeline Screenshot
Cohesion: 1.0
Nodes (1): Supervisor work order timeline at resolved state

### Supervisor Queue Screenshot
Cohesion: 1.0
Nodes (1): Supervisor operations dashboard and work order queue

### Mobile Supervisor Queue Screenshot
Cohesion: 1.0
Nodes (1): Responsive supervisor queue on a narrow mobile screen

### Saved Ticket TTS Control Screenshot
Cohesion: 1.0
Nodes (1): Saved work order with Timbre acknowledgment playback control

### Accessible Work Order Detail Screenshot
Cohesion: 1.0
Nodes (1): Accessible work order detail desktop view

### Accessible Sign-In Screenshot
Cohesion: 1.0
Nodes (1): Accessible sign-in desktop view

### Accessible Desktop Queue Screenshot
Cohesion: 1.0
Nodes (1): Accessible supervisor queue desktop view

### Accessible Mobile Queue Screenshot
Cohesion: 1.0
Nodes (1): Accessible supervisor queue mobile view

### Accessible Desktop Report Screenshot
Cohesion: 1.0
Nodes (1): Accessible worker report capture desktop view

### Accessible Mobile Report Screenshot
Cohesion: 1.0
Nodes (1): Accessible worker report capture mobile view

### Public Judge Dashboard Screenshot
Cohesion: 1.0
Nodes (1): Password-free read-only judge work order dashboard

### Approved Report Provenance Screenshot
Cohesion: 1.0
Nodes (1): Read-only judge detail with approved report transcript provenance and audit

### Mobile Judge Detail Screenshot
Cohesion: 1.0
Nodes (1): Read-only approved report detail on mobile screen

### Judge Demo Login Screenshot
Cohesion: 1.0
Nodes (1): Password-free Open judge demo sign-in option

### Solution Pitch Preview
Cohesion: 1.0
Nodes (1): FieldSaarthi project pitch preview with product summary

### Waveform Favicon
Cohesion: 1.0
Nodes (1): FieldSaarthi green square waveform favicon

### Shared SVG Icon Symbols
Cohesion: 1.0
Nodes (1): Reusable social, documentation and repository SVG icon symbols

### Layered Hero Illustration
Cohesion: 1.0
Nodes (1): Abstract layered violet hero illustration asset

### Vite Logo Asset
Cohesion: 1.0
Nodes (1): Vite development tool logo asset

### Graph Export Artifacts
Cohesion: 0.0
Nodes (inventory): GRAPH_REPORT.md, coverage.json, graph.html, graph.json

## Knowledge Gaps
- **200 isolated node(s):** `Protect maintenance operations as well as row updates.`, `Add explicit manual accessibility provenance without relabeling voice reports.`, `User-approved public read-only judge role and explicit report allowlist.`, `Allowlisted stage events: no bodies, transcripts, credentials or exception text.`, `FR-06..09: real Prisma v2.5 REST adapter. No production fixture path. Contract:` (+195 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `SQLAlchemy Session Dependency`** (2 nodes): `session.py`, `get_db()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Migration-First Server Startup`** (2 nodes): `start.py`, `One-worker deployment entry point. Run migrations before accepting traffic.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Request ID Logging Tests`** (2 nodes): `test_observability.py`, `test_http_event_is_emitted_with_request_id_and_without_query_secrets()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Accessible Manual Report Page`** (2 nodes): `onReady()`, `ManualReport.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Work Order Queue Filters`** (2 nodes): `filter()`, `Orders.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Authentication And Authorization Core`** (2 nodes): `Authentication and authorization`, `api/app/core/security.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Request Stage Telemetry`** (2 nodes): `Request observability`, `api/app/core/telemetry.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Live Gnani Smoke Workflow`** (2 nodes): `Provider smoke workflow`, `api/app/integrations/smoke.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Timbre Text To Speech`** (2 nodes): `Gnani Timbre TTS integration`, `api/app/integrations/tts.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Browser End To End Workflow`** (2 nodes): `Browser workflow coverage`, `api/tests/browser/workflow_check.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Shared Pytest Fixtures`** (2 nodes): `Automated verification`, `api/tests/conftest.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Hash Route Navigation`** (2 nodes): `Client-side route navigation`, `web/src/lib/navigation.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Runtime Settings`** (2 nodes): `Runtime configuration`, `api/app/core/config.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Typed Application Errors`** (2 nodes): `Safe application errors`, `api/app/core/errors.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Audio And Request Limits`** (2 nodes): `Resource bounds`, `api/app/core/limits.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Provider Integration Package`** (2 nodes): `Provider integration`, `api/app/integrations/__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Demo And Judge Authentication`** (2 nodes): `Authentication and demo access`, `api/app/routers/auth.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Application Package`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Environment Configuration`** (1 nodes): `config.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Gnani Integration Package`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Pytest Configuration`** (1 nodes): `conftest.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vite Development Configuration`** (1 nodes): `vite.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Git Text And Binary Rules`** (1 nodes): `.gitattributes`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Project Change Log`** (1 nodes): `Changelog`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Alembic Configuration`** (1 nodes): `alembic.ini`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Python Dependencies And Tooling`** (1 nodes): `pyproject.toml`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `FFmpeg Type Stub`** (1 nodes): `imageio_ffmpeg.pyi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Locked Python Dependencies`** (1 nodes): `uv.lock`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Participant Microphone Evidence`** (1 nodes): `Human Microphone Verification`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Hosted Runtime Evidence`** (1 nodes): `Runtime Verification`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Gnani Documentation Source Index`** (1 nodes): `Index`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Frontend Lint Rules`** (1 nodes): `.Oxlintrc`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Frontend HTML Entrypoint`** (1 nodes): `FieldSaarthi AI | Voice to action`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Web Package Metadata`** (1 nodes): `fieldsaarthi-web`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Web Dependency Lockfile`** (1 nodes): `fieldsaarthi-web`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Base Interface Styles`** (1 nodes): `index.css`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Application Theme Styles`** (1 nodes): `styles.css`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Frontend App TypeScript Settings`** (1 nodes): `Tsconfig.App`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Frontend TypeScript Settings`** (1 nodes): `Tsconfig`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vite TypeScript Settings`** (1 nodes): `Tsconfig.Node`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `User-Owned Submission Gate`** (1 nodes): `Official form remains user-reserved`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Judge Queue Regression Screenshot`** (1 nodes): `Automated judge queue regression screenshot at 1440 pixels`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Resolved Workflow Browser Screenshot`** (1 nodes): `Fixture-based end-to-end test showing resolved work order`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Human Transcript Review Screenshot`** (1 nodes): `Fixture-based end-to-end test showing human transcript review`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Worker And Supervisor Login Screenshot`** (1 nodes): `Worker and supervisor sign-in interface`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Voice Report Capture Screenshot`** (1 nodes): `Worker voice report capture landing page`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Transcript Correction Screenshot`** (1 nodes): `Worker transcript review and field correction form`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Persisted Work Order Screenshot`** (1 nodes): `Persisted work order detail after report confirmation`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Resolved Audit Timeline Screenshot`** (1 nodes): `Supervisor work order timeline at resolved state`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Supervisor Queue Screenshot`** (1 nodes): `Supervisor operations dashboard and work order queue`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Supervisor Queue Screenshot`** (1 nodes): `Responsive supervisor queue on a narrow mobile screen`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Saved Ticket TTS Control Screenshot`** (1 nodes): `Saved work order with Timbre acknowledgment playback control`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Accessible Work Order Detail Screenshot`** (1 nodes): `Accessible work order detail desktop view`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Accessible Sign-In Screenshot`** (1 nodes): `Accessible sign-in desktop view`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Accessible Desktop Queue Screenshot`** (1 nodes): `Accessible supervisor queue desktop view`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Accessible Mobile Queue Screenshot`** (1 nodes): `Accessible supervisor queue mobile view`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Accessible Desktop Report Screenshot`** (1 nodes): `Accessible worker report capture desktop view`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Accessible Mobile Report Screenshot`** (1 nodes): `Accessible worker report capture mobile view`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Public Judge Dashboard Screenshot`** (1 nodes): `Password-free read-only judge work order dashboard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Approved Report Provenance Screenshot`** (1 nodes): `Read-only judge detail with approved report transcript provenance and audit`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Mobile Judge Detail Screenshot`** (1 nodes): `Read-only approved report detail on mobile screen`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Judge Demo Login Screenshot`** (1 nodes): `Password-free Open judge demo sign-in option`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Solution Pitch Preview`** (1 nodes): `FieldSaarthi project pitch preview with product summary`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Waveform Favicon`** (1 nodes): `FieldSaarthi green square waveform favicon`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Shared SVG Icon Symbols`** (1 nodes): `Reusable social, documentation and repository SVG icon symbols`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Layered Hero Illustration`** (1 nodes): `Abstract layered violet hero illustration asset`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Vite Logo Asset`** (1 nodes): `Vite development tool logo asset`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AppError` connect `Authentication And Intake Routes` to `Gnani STT And Timbre Adapters`, `Transactional Orders And Audit Models`, `Audio Contracts And Backup Drill`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `ProviderResult` connect `Gnani STT And Timbre Adapters` to `Typed API Response Schemas`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `stable()` connect `Backend Workflow Regression Tests` to `Catalog Extraction And Provenance`, `Authentication And Intake Routes`, `Recording And Browser Evaluation`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `login()` (e.g. with `test_search_injection_is_literal_and_preserves_ownership_and_tables()` and `test_manual_text_is_explicit_and_has_no_provider_provenance()`) actually correct?**
  _`login()` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `AppError` (e.g. with `BodyLimit` and `ProviderBudget`) actually correct?**
  _`AppError` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `fixture_intake()` (e.g. with `test_database_rejects_invalid_rows_directly()` and `test_search_injection_is_literal_and_preserves_ownership_and_tables()`) actually correct?**
  _`fixture_intake()` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `payload()` (e.g. with `test_search_injection_is_literal_and_preserves_ownership_and_tables()` and `test_manual_text_is_explicit_and_has_no_provider_provenance()`) actually correct?**
  _`payload()` has 16 INFERRED edges - model-reasoned connections that need verification._
