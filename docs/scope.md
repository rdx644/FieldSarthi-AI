# Frozen baseline - WBS-00.4
Title: FieldSaarthi AI - Multilingual Voice-to-Action Intelligence for Field Operations.
Personas: worker/reporter, supervisor/dispatcher; seeded setup admin only.
Baseline: Hindi/Hinglish report, selected `hi-IN`, genuine Prisma v2.5 STT. English/Tamil speech quality remains unverified. Optional Timbre v2.5 acknowledgment and duplicate warnings are implemented and locally verified; Prisma v3 experiments remain deferred.
Scenario: Block B / second floor / water pump leaking, urgent repair cue. Synthetic inventory; actual recording from consenting speaker. Urgency is a suggestion requiring supervisor triage.

P0 backlog frozen in dependency order: foundation and synthetic inventory (FR-01..02), auth/RBAC (FR-03), capture/validation (FR-04..05), genuine Prisma/provenance/errors (FR-06..09), catalog extraction (FR-10..12), correction/confirmation (FR-13..15), durable transactional/idempotent orders/audit (FR-16..19), supervisor workflow (FR-20..22), reliability/security/reproducibility (NFR-01..14), truthful demo and final form (O-04..10).
P1: Timbre (FR-23), duplicate warnings/provenance UI (FR-24..25), after P0. Preserve core audit/provenance in P0 backend.
P2: Prisma v3 comparison, richer analytics. No telephony, native app, Kubernetes or autonomous emergency actions.

The earlier WBS-01 stop was superseded by the user's authorization for WBS-02 through WBS-08 on 2026-11-09. Development is merged at `8146882` and tagged `v0.2.0-rc.1`. The user now authorizes a full roadmap audit and free Render deployment. The explicit instruction not to submit the final form remains in force; contribution statements and social publication remain participant-owned.

The release candidate does not close every roadmap gate. See [the complete audit](evidence/roadmap-audit.md) for every section, WBS item, test gap and implementation variation. Optional P2 items remain optional; human/audio/hosting evidence needs actual execution.
