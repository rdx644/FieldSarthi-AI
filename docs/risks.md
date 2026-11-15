Latest finalisation: **307 backend tests and actual container compatibility,
rollback and restoration pass locally**; independent evaluation is explicitly
participant-deferred. The prepared compatibility build resolves the earlier local
blocker. Both source CI runs pass; approved production backup/deployment remains pending.
See [current finalisation](release-finalisation.md). Earlier checkpoint statements below retain their
historical scope.

# Risk register - reviewed 2026-11-09

Severity describes impact if the risk occurs, not proof that a defect exists. See [the complete audit](evidence/roadmap-audit.md) for missing requirements and tests.

| ID | Impact | Current evidence / remaining trigger | Mitigation / owner |
|---|---|---|---|
| R-01 | Critical | Local and hosted genuine STT/TTS verified; current balance unqueried | Participant monitors actual console balance; starting allocation is not current balance |
| R-02 | High | Bounded FFmpeg and file-fed browser capture verified | Backend owner: preserve regressions; participant verifies broader HTTPS microphone/browser coverage |
| R-03 | Medium | Actual 15-recording Hindi/English/Hinglish development corpus scored 12/15; Tamil unverified | Same-corpus rule refinement disclosed; three ASR failures require human correction; no population accuracy claim |
| R-04 | High | Exact spans/parser version and catalog/human validation implemented; unknown ASR words stay unresolved | Reject unknown/mismatched IDs; retain negative/multilingual/hazard regressions and explicit human confirmation |
| R-05 | High | Concurrent replay, unique intake and atomic writes verified | Backend owner: retain race/idempotency checks |
| R-06 | Low | Real Timbre WAV verified; provider availability external | Backend owner: independent saved-ticket audio; outage cannot undo order |
| R-07 | High | Free Render HTTPS workflow/restart verified; cold starts remain possible | Deployment owner: readiness before demo, reproducible local fallback and final video; 15-clip evaluation and ten genuine workflows are now recorded |
| R-08 | Critical | Deadline near; development merged | Team: prioritize hosted/audio proof and media; defer P2 |
| R-09 | Critical | Environment/audio excluded from Git/image context | All: secret/content scans and video review; rotate any exposed key |
| R-10 | Critical | Video/post/form unfinished; form reserved for user | Participants: final checklist, exact URLs and confirmation |
| R-11 | Critical | Genuine local proof exists; fixtures explicitly labeled | All: distinguish local/file-fed/new-speech/hosted evidence |
| R-12 | Medium | Names/institution supplied; individual contributions undecided | Participants: verifiable personal statements; no invented attribution |
| R-13 | High | Additive migrations and isolated backup/restore verified | Deployment owner: private export before demo; compatible app rollback |
| R-14 | Critical | Synthetic inventory and consenting private sample | Participants: consent, media review and bounded retention |
| R-15 | High | Remote main/protection/exact-head CI verified | Maintainer: protected PR, current quality result, no force push |
| R-16 | High | Free Render PostgreSQL expires in 30 days; no managed backup | Deployment owner: private export/recovery; paid upgrade needs separate authorization |

Review before G3/G4. Known Critical/High defects block release; absent evidence stays pending even when CI passes.

## November 14 improvement candidate risks

| ID | Impact | Current evidence / remaining trigger | Mitigation / owner |
|---|---|---|---|
| R-17 | Critical rollout blocker | Local ledger migration `0005` is additive, but old image startup cannot resolve that revision and exact-head readiness expects `0004` | Operator: stage and verify a compatibility rollback image before any production migration; private backup and deployment approval; never downgrade/delete records |
| R-18 | High evaluation limitation | No verified human reference transcripts or independent held-out result; offline tool is tested on synthetic examples only | Participant: supply consented verified references and separately approve any bounded live study; retain historical 12/15 and no 95-point claim |
| R-19 | High demo access | Intentionally shared synthetic worker/supervisor accounts can spend quota or mutate shared demo data | Preserve owner policy; monitor real credits and pause if needed; no new public report visibility or credential changes |
| R-20 | Medium deployment assumption | Login limiter is now thread-safe locally but process-local; startup trusts forwarded headers from its ingress | Preserve one worker/replica; operator must verify ingress sanitizes forwarded client headers before any broader exposure |
| R-21 | High verification gap | Candidate has local gates only; current hosted revision/health were rechecked November 15; direct schema SQL, exact candidate CI and container build remain unverified | No release claim; Docker engine unavailable locally; operator reviews exact CI/backup and health/provenance after approved deployment |

November 15: exact old deployed API source independently reproduced the `0005` startup/readiness incompatibility; [executed evidence](evidence/improvement-rollback-compatibility.json). Current operator API confirms database expiry 2026-12-09; backup retention and balance remain owner-managed. See [handoff](improvement-handoff.md).
