Latest ownership update: production backup is handled by the participant and
completion is not yet confirmed. The agent completes automatic source publication,
protected merge, CI and local/main synchronization. Engineering and image rollback
are verified; live migration waits for backup confirmation. See
[current status](release-finalisation.md). Earlier checkpoint statements below retain their scope.

# Latest finalisation checkpoint

**307 backend tests and the real four-phase container rollback pass locally.**
The compatibility blocker is resolved for the prepared build; independent audio
evaluation is explicitly deferred by participant decision. Both source CI runs pass; production approval/backup/deployment remains pending. Read
[the current release finalisation](release-finalisation.md) and
[release evidence](evidence/improvement-finalisation-release.json).
The earlier checkpoint below is preserved as history and is superseded where it
calls the local compatibility build unavailable or reports 295 tests.

# FieldSaarthi improvement handoff — 2026-11-15

Status: **LOCAL VERIFIED — NOT DEPLOYED. Hold production migration/release.**
The authorized local implementation and verification are finished. All 34 planned
test IDs have a disposition: 30 pass locally, one genuine held-out gate is deferred,
and three migration/release gates remain blocked. No requirement was waived.

- Plan baseline/main: `0fca9716e3589eb9cac70f12e2468aacf7cadb5a`; remote main still matches.
- Verified application/test source: `84366153682af65f96874dc717e4aa6febed10be`, `feature/95-improvements`.
  Later local commits contain documentation/evidence; use `git rev-parse HEAD`
  for the final handoff commit. No push, PR, merge or candidate remote CI is claimed.
- Live application independently observed through the operator API:
  `85e1a5e20c1f623c0ce664493c8f002e7d5cff10`.
  Both health endpoints returned 200; the current baseline's
  [exact CI](https://github.com/rdx644/FieldSarthi-AI/actions/runs/42850275143) passed.
- Existing release tag `demo-verified-2026-11-10` is unchanged. Historical rollback
  target: `6f702c26f5d0ebca99cc71ba870bb7031fdd4dcd`. Neither is a compatible
  rollback target for `0005` without a separately verified compatibility release.

## Completed local changes

| Change | Result and reason | Main files / evidence |
|---|---|---|
| IMP-00 | Guard compressed backups, runtime/private paths and committed-source ZIPs; private workspace preserved | `api/scripts/repository_guard.py`, `.gitignore`, `.dockerignore`; [archive verification](evidence/improvement-archive-final.json) |
| IMP-01 | Clear public read-only scope and returned-example shortcut, active docs/deadline aligned; direct judge speech/mutation denials verified | `web/src/pages/Orders.tsx`, `api/tests/integration/test_judge_access.py`; [judge result](evidence/improvement-judge.json) |
| IMP-02 | SQL role-scoped totals independent of pages/filters, truthful source/priority/duration cards | `api/app/services/analytics.py`, queue contracts/router/UI; [25-order test results](evidence/improvement-dashboard.json) |
| IMP-03 | Original evidence and explicit confirmation preserved; incompatible equipment and prior confirmation clear on location edits; language readiness explicit | `web/src/pages/Review.tsx`, `Report.tsx`; [fresh cached replay](evidence/improvement-extraction-final.json) |
| IMP-04A | Network-free WER/CER scorer with explicit denominators, split/privacy validation and hardlink-safe private inputs | `api/scripts/score_transcripts.py`; [methodology](tests/offline-asr-methodology.md) |
| IMP-05 | Committed PostgreSQL operation admissions survive restart; concurrent limits, expiry, pause and fail-closed paths tested; login check serialized | `api/app/services/provider_admission.py`, migration `0005`, route/limiter tests; [quota semantics](adrs/ADR-010-durable-provider-admission.md) |
| IMP-06 local | Full quality checks, browser verification, current hosting readback, coverage and handoff; release held | [release manifest](evidence/improvement-release.json), [all 34 T-IMP IDs](evidence/improvement-completion-audit.json) |

The specification's safer-baseline option applies to extraction: `rules-v4` is
retained because none of the three failed development cases has shared aliases
that location filtering could safely recover. Optional re-extraction, charting and
daily-cap features were not required and were not introduced. Provider choices,
workflows, all production records and account/publication policies are preserved.
The newly found hardlink overwrite bug was reproduced with two failing synthetic
tests before fixing it; all 30 scoring tests then passed. Review also closed the
missing direct judge STT/assignment/status/confirmation/correction test coverage.

## Executed verification and evidence limits

The candidate passed **295 tests in 56.84 seconds** against `fieldsaarthi_test`;
no skipped/disabled tests or weakened gates were introduced. Ruff lint/format,
strict mypy (24 application files), frontend lint/Prettier/TypeScript/Vite and both
dependency audits passed. The Chrome fixture workflow passed **16 axe/layout
views**, widths 320/768/1024/1440, keyboard shortcut, empty/unavailable/stale states,
review confirmation, idempotency, supervisor resolution and refresh. It recorded
zero JavaScript errors and zero live provider requests. Screenshots are synthetic
local fixture evidence, not hosted speech results.

The initial DB-offline suite and focused reproduction timed out; starting the
documented localhost cluster resolved that setup issue. Fresh full results above
supersede that attempt. Docker Desktop's engine was unavailable; no new container
build is claimed. The exact candidate remote CI has not run. Previous baseline
199-test and candidate 293-test runs remain historical November 14 results.

Fresh offline development replay: **12/15 automatic complete cases**, location
12/14, asset 11/14, issue 13/14, urgency suggestion 14/14; **6/6 expected blocks**,
zero previously correct complete-case regressions. Cached explicit correction
recovery passed **3/3** in 2.67 seconds. These are the tuned development corpus,
not independent generalization or new provider responses. Historic genuine
coverage stays 14/15; the ten hosted reliability runs reused one consenting clip.
Verified human references are missing, so genuine WER/CER remain unmeasured.

**Actual live speech calls, new recordings, production domain writes, migrations,
deploys, rollbacks, access changes and submissions during this work: zero.**
Judge-session issuance and public GETs performed no domain writes. Readback
confirmed only WO-AFF1E3EE3BD2 is visible, OPEN/version 1, original transcript hash
unchanged, real Prisma provenance present and TTS disabled for judge access.
No private transcript, credential, raw recording or backup was published.

## Remaining release gates and exact next actions

1. **T-IMP-043 / IMP-04B — deferred, participant.** Independent consented data,
   verified human references and explicit credit/recording authorization are absent.
   Keep the existing accuracy deductions; no synthetic or tuned case becomes held-out.
2. **T-IMP-056 / IMP-05 — blocked for production, engineering/operator.** Local
   `0004 -> 0005` additive upgrade preserves domain details/audits/provenance.
   Executing the exact old deployed API source at `0005` proved startup cannot
   resolve that revision and readiness returns 503. This is stronger than the
   earlier simulated head check, but it is not an executed container rollback.
   Prepare a staged compatibility image containing the migration graph and explicit
   startup/readiness handling for the approved `0004`/`0005` transition. Verify it
   on both schemas and as the rollback target before advancing production. Do not
   accept arbitrary future heads or down-migrate/delete history. See the
   [executed compatibility blocker](evidence/improvement-rollback-compatibility.json).
3. **T-IMP-062 — blocked, maintainer/operator.** Review the concrete candidate,
   obtain exact candidate CI/container success, a private production backup with
   isolated restore evidence, current balance check and deployment approval.
   Preserve protected main and deliberate `autoDeployTrigger: off`. No publication
   or production action was authorized merely by this implementation request.
4. **T-IMP-063 — blocked, operator.** Once the compatible image and release plan
   are approved, verify candidate rollback/restoration and privately compare
   unchanged order/audit/provenance snapshots. The old 12-order drill cannot stand
   in for the new schema. Until then, retain the live known-good application.

Production schema was not read directly: the stored external connection returned
an operational error. The unchanged old application's 200 readiness implies its
expected `0004` head; this is an inference, not a successful direct SQL query.
Render's operator API freshly reports the free PostgreSQL 18 instance available,
expiring **2026-12-09T12:16:30.004422Z**. Current backup retention remains owner-managed;
there is no managed-backup/SLA claim. The provider balance was not observed.
Pause both speech endpoints using the existing environment flag and approved host
deployment procedure when the balance is uncertain. Quotas count admissions, not
money; failed processing retains reservations and STT retries may add requests.
Keep one worker/replica. Login limits remain process-local; forwarded-header trust
still depends on a correctly sanitized ingress.

## Provisional seven-dimension reassessment

This is a local engineering self-assessment against the supplied rubric, not an
official score or a deployed reassessment. The live application retains its
historical assessment until an approved release is independently evaluated.

| Dimension | Supplied baseline | Provisional local candidate | Evidence / withheld credit |
|---|---:|---:|---|
| Problem relevance/business value | 18/20 | 19/20 | Correct scoped KPIs and synthetic supervisor workflow; no invented time savings |
| Genuine Gnani integration | 19/20 | 19/20 | Real baseline provenance retained; no fresh genuine evaluation |
| Functional completeness | 18/20 | 19/20 | SQL totals, correction and direct role tests |
| Architecture/security/reliability | 13/15 | 13/15 | Durable limiter tested locally; production compatibility remains blocked |
| UI/UX/accessibility | 8/10 | 9/10 | 16 fixture axe/layout views and keyboard/empty/error coverage |
| Accuracy/evaluation | 7/10 | 7/10 | No independent held-out or verified-reference WER/CER |
| Repository/documentation | 4/5 | 5/5 | Traceable evidence, safe export and current handoff |
| Total | 87/100 | **91/100 provisional local** | **95/100 not established** |

The official [challenge page](https://www.gnani.ai/internship), rechecked November
15, states the dated cutoff **November 15, 2026, 18:00 IST**. Contributions,
eligibility attestations, public video/post and the official form remain
participant-owned and were not performed. Local completion does not mark these
or the blocked release gates complete.
