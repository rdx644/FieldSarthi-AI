# Judge readiness completion plan

User authorization: finish the remaining implementation-plan gaps and update protected main,
including work from docs/human-microphone-proof, docs/render-hosted-proof,
chore/roadmap-audit-render and feature/complete-fieldsaarthi (2026-11-09).
Fetched baseline e8d6f97 contains all four branch tips; preserve their history.

Acceptance slices:

1. FR-10..12 / NFR-06: versioned extraction with exact original-text spans and
   negative/multilingual/ambiguous scenarios. No arbitrary confidence scores.
2. FR-04..09 / NFR-05,09,14: explicit manual text accessibility intake, immutable
   source type, no invented provider provenance, privacy disclosure, actionable
   provider errors and bounded stage telemetry. Add typed response contracts.
3. FR-20..22: priority/location/assignee queue controls and audited cancellation
   justification, preserving roles, ownership, paging and optimistic locking.
4. NFR-01,03,04,08,10: missing atomicity, race, validation, duplicate, token,
   readiness, media and TTS regression cases; ten consecutive test workflows;
   browser permission/XSS/full workflow checks; CI history/secret/media scan.
5. WBS-07.3 / O-04..10: private authentic-recording evaluation runner with
   distinctness and ground-truth checks, honest public results, judge walkthrough
   and submission handoff. Do not manufacture recordings, contributions or posts.
6. Review all changes; run project checks; merge via protected PR only after CI;
   synchronize local main, deploy existing Render service and verify runtime.

External completion gates: 15 authentic distinct recordings, participant
eligibility/contributions, final video/public post, participant release approval,
and user-reserved final form. No paid hosting upgrade or social publication.
Free database lifecycle/managed-backup limitation must remain explicit.

Verification and exact results will be recorded in docs/evidence/judge-readiness.md.
