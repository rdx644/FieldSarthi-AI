# FieldSaarthi release finalisation

Status: **engineering and CI verified; production backup is participant-owned and not yet confirmed**.

The final backend suite passed **307 tests in 91.84 seconds**. Strict Ruff/format,
mypy and the Python dependency audit pass. Exact candidate CI repeats frontend checks and all 16 Chrome fixture views successfully. Both candidate and
compatibility Docker images built successfully after a local Docker storage
failure recovered. No existing images/containers were pruned or reset.

The [actual container report](evidence/improvement-container-release.json) verifies:

| Phase | Application | Schema | Readiness | Data |
|---|---|---|---|---|
| Stage | Previous app with five reviewed compatibility changes | 0004 | 200 | Seven domain tables preserved |
| Activate | Candidate with durable provider admissions | 0005 | 200 | Same records; two test admissions reserved |
| Roll back | Compatibility build, speech forced paused | 0005 | 200 | Domain and admission records preserved |
| Restore | Candidate | 0005 | 200 | Domain and admission records preserved |

The rehearsal used only synthetic data and a new internal Docker network/database,
with no host ports or live provider access. It is not hosted release evidence.
Five additional tests prove timeout cleanup preserves other Docker resources and
UTF-8 decoding preserves Hindi/Tamil catalog output. All seven source-level
compatibility tests also pass, including rejection of missing/mixed/future heads.

## Reviewable sources

- Candidate: `c94e06f04dfb75c8e1384298ea2dc1aaa2fea4ff`, `feature/95-improvements`.
- Compatibility/rollback: `be608cb4ea807d8fd0280633f05595e89d83fb2d`, `release/schema-compatibility`.
- The compatibility build starts from baseline `0fca971`; its original app,
  frontend, dependencies, startup and migration tree match live `85e1a5e` before
  the five explicit compatibility changes. It neither migrates on startup nor
  accepts arbitrary future heads, and always pauses paid speech.
- The candidate keeps exact 0005 readiness and the durable operation ledger.
- [Current audit](evidence/improvement-finalisation-audit.json) maps all 39
  specification headings and 34 T-IMP IDs. The canonical section-12 ID meanings
  correct the reordered labels in the earlier audit; no coverage was removed.

The CI workflow now builds both images and runs the actual activation/rollback/
restoration script automatically. Both exact branch CI runs passed: [candidate](https://github.com/rdx644/FieldSarthi-AI/actions/runs/43686208851) and [compatibility](https://github.com/rdx644/FieldSarthi-AI/actions/runs/43686213536). The [release manifest](evidence/improvement-finalisation-release.json) records them.
The compatibility branch is a reviewed rollback artifact; do not merge its paused
old-application behavior into the candidate feature branch.

## Approved evaluation scope

The participant supplied `private/evaluation`; metadata inspection confirmed the
same 15 tuned development clips and no separate verified-reference held-out set.
The participant then explicitly chose **finalise with independent evaluation
deferred**. See [the recorded decision](evidence/improvement-evaluation-disposition.json).
Original files remain unchanged. Existing 12/15 complete cases, 14/15 nonempty
transcripts, 6/6 expected blocks and 3/3 cached correction recovery keep their
original denominators. Genuine WER/CER and held-out generalisation remain unmeasured.
No 95-point result or new speech accuracy uplift is claimed.

## Production release plan - owner backup gate

1. Review exact candidate/compatibility CI and container evidence.
2. The participant takes care of production backup and restore readiness.
   Confirm that the backup is current and restore-ready before migration. The
   agent does not change database ingress, export production data or claim backup
   completion. Backup ownership does not waive the migration safety gate.
3. Complete protected source merge and exact main CI. After owner backup confirmation, deploy the compatibility
   build first; it must remain at 0004 and healthy with paid speech paused.
4. Deploy the candidate; its startup advances additively to 0005. Perform read-only
   health, judge/provenance and private baseline-data comparisons. Make no new
   billable smoke calls. Keep speech paused if the owner has not verified balance.
5. With approval, rehearse rollback to the compatibility build at 0005, compare
   records/admissions, then restore the candidate and verify again. Never downgrade
   or delete evidence to make an old image boot.

Specification section 11.1 step 4 explicitly requires an approved deployment plan
and private backup before production migration. Source preparation, local tests and approved source publication/CI
are complete; actual production execution must remain distinguished
in the final status. Official contribution/eligibility, video, public post and
submission form remain participant-owned and untouched.

The existing live app remains the previous known-good release while owner backup
confirmation is pending. Updating protected main does not deploy it because
Render auto-deploy remains disabled. Existing account passwords, public judge visibility,
provider choice and all production data remain unchanged by this work.


## Latest participant scope and automatic completion

The participant explicitly owns backup and asked the agent to finish all remaining
steps requiring no manual configuration. Engineering/code, 307 tests, both image
builds, source and real-container rollback, exact source CI, and sanitized evidence
are verified. The agent can publish the latest status, complete PR #18 through
required checks and keep local/main synchronized. PR #19 remains the separate
rollback artifact and must not be merged into the candidate.

The [owner handoff](evidence/improvement-owner-handoff.json) records the split.
Production backup completion is not inferred from the promise to take care of it;
no live migration or hosted rollback is marked complete. Independent evaluation
remains explicitly deferred. No additional manual configuration, paid test,
credential rotation or participant submission is introduced.
