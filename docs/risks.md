# Risk register - reviewed 2026-11-09

Severity describes impact if the risk occurs, not proof that a defect exists. See [the complete audit](evidence/roadmap-audit.md) for missing requirements and tests.

| ID | Impact | Current evidence / remaining trigger | Mitigation / owner |
|---|---|---|---|
| R-01 | Critical | Local and hosted genuine STT/TTS verified; current balance unqueried | Participant monitors actual console balance; starting allocation is not current balance |
| R-02 | High | Bounded FFmpeg and file-fed browser capture verified | Backend owner: preserve regressions; participant verifies broader HTTPS microphone/browser coverage |
| R-03 | Medium | Hindi sample verified; 15 audio cases/other languages missing | Participants: consented corpus and actual field/transcript comparison; limit claims |
| R-04 | High | Catalog validation/human confirmation implemented; evidence-span/parser-version gaps | Backend owner: reject unknown/mismatched catalog IDs; track audit gaps |
| R-05 | High | Concurrent replay, unique intake and atomic writes verified | Backend owner: retain race/idempotency checks |
| R-06 | Low | Real Timbre WAV verified; provider availability external | Backend owner: independent saved-ticket audio; outage cannot undo order |
| R-07 | High | Free Render HTTPS workflow/restart verified; cold starts remain possible | Deployment owner: readiness before demo, reproducible local fallback and 15-clip evaluation and final video |
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
