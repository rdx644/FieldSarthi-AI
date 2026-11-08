# Frozen baseline - WBS-00.4
Title: FieldSaarthi AI - Multilingual Voice-to-Action Intelligence for Field Operations.
Personas: worker/reporter, supervisor/dispatcher; seeded setup admin only.
Baseline: Hindi/Hinglish report, selected `hi-IN`, genuine Prisma v2.5 STT. English/Tamil only after authentic tests. Optional Timbre and v3 experiments remain deferred.
Scenario: Block B / second floor / water pump leaking, urgent repair cue. Synthetic inventory; actual recording from consenting speaker. Urgency is a suggestion requiring supervisor triage.

P0 backlog frozen in dependency order: foundation and synthetic inventory (FR-01..02), auth/RBAC (FR-03), capture/validation (FR-04..05), genuine Prisma/provenance/errors (FR-06..09), catalog extraction (FR-10..12), correction/confirmation (FR-13..15), durable transactional/idempotent orders/audit (FR-16..19), supervisor workflow (FR-20..22), reliability/security/reproducibility (NFR-01..14), truthful demo and final form (O-04..10).
P1: Timbre (FR-23), duplicate warnings/provenance UI (FR-24..25), after P0. Preserve core audit/provenance in P0 backend.
P2: Prisma v3 comparison, richer analytics. No telephony, native app, Kubernetes or autonomous emergency actions.

This execution stops at WBS-01. WBS-02 onward waits for genuine G1. Changes to this scope require a recorded reason and updated tests/traceability.
