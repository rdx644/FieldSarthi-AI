# Targeted engineering improvements — 2026-11-14

Source: participant-provided Downloads/FieldSaarthi_AI_95_Improvement_Specification.md.
Baseline: 0fca9716e3589eb9cac70f12e2468aacf7cadb5a, main. Existing untracked Gnani.zip stays untouched.
Branch: feature/95-improvements. No paid requests, production writes, deployments, publication or credential changes authorized by this work.

- [x] IMP-00 / T-IMP-001..002: extend archive guard and verify tracked-only source export; preserve private files.
- [x] IMP-01 / T-IMP-010..012: align active reviewer docs and add authorized example shortcut; verify role restrictions and mobile/keyboard.
- [x] IMP-02 / T-IMP-020..025: typed SQL role-scoped summary independent of pages/filters; >20 orders, empty/duration/ACL and UI tests.
- [x] IMP-03 / T-IMP-030..036: verify existing safe parser, review compatibility behavior, language readiness; retain rules-v4 unless measured safe gain.
- [x] IMP-04A / T-IMP-040..042/044: offline WER/CER, explicit denominators/private manifest and fixture tests. Genuine WER blocked without verified references; held-out corpus deferred without separate approval/data.
- [x] IMP-05 / T-IMP-050..056: additive durable quota candidate; isolated concurrency/restart/expiry/fail-closed tests. T-IMP-056 production compatibility is blocked, as recorded below.
- [x] IMP-06 local / T-IMP-060..061: full local quality gates, preserve historical artifacts, evidence and handoff. T-IMP-062..063 candidate CI/hosted deployment/rollback remain blocked, as recorded below.

Dependencies: baseline before changes; typed summary before UI; all DB tests/browser reset only fieldsaarthi_test and run sequentially. Database migration/old-app readiness compatibility must be proven before any rollout. Each increment reviewed and verified before local commit. Owner: engineering agent for implementation; participant/operator for recordings, credits, production and submission.


## Final local verification — 2026-11-15

**Local implementation complete; production release held.** Checkmarks above mean
local engineering work only. The [handoff](../docs/improvement-handoff.md) and
[release manifest](../docs/evidence/improvement-release.json) distinguish every
pending external gate. No requirement is waived or silently omitted.

- 295 backend tests passed; strict static/frontend checks and both dependency audits passed.
- Chrome: 16 clean accessibility/layout views, no JavaScript errors or live speech calls.
- Offline replay: rules-v4 retained, 12/15 complete cases, 6/6 safety blocks, 3/3 correction recovery.
- Remote main unchanged; existing hosted application healthy; only the approved public sample visible.
- Local review fixed private-input hardlink overwriting and completed direct judge API denials.
- Source, private data, historical evidence, public account policy and release tags preserved.

### All planned test IDs

| ID | Requirement | Actual check / evidence | Status |
|---|---|---|---|
| T-IMP-001 | guarded archive | `api/tests/unit/test_repository_guard.py::test_imp_001_clean_archive_is_allowed` | PASSED LOCAL |
| T-IMP-002 | synthetic forbidden paths/secrets | `api/tests/unit/test_repository_guard.py::test_imp_001_archive_checks_paths_and_contents_without_disclosing_secrets`; `api/tests/unit/test_repository_guard.py::test_imp_002_backup_archive_and_runtime_paths_are_blocked` | PASSED LOCAL |
| T-IMP-010 | reviewer links and official date | `docs/evidence/improvement-documentation-check.json` | PASSED LOCAL |
| T-IMP-011 | judge read-only and hidden report ACL | `api/tests/integration/test_judge_access.py::test_public_judge_is_read_only_and_sees_only_approved_reports` | PASSED LOCAL |
| T-IMP-012 | desktop/mobile/keyboard/empty/error | `api/tests/browser/workflow_check.py` | PASSED LOCAL |
| T-IMP-020 | totals reconcile with >20 orders | `api/tests/integration/test_queue_analytics.py::test_summary_is_role_scoped_and_stable_across_pages_filters` | PASSED LOCAL |
| T-IMP-021 | role-scoped aggregates | `api/tests/integration/test_queue_analytics.py::test_summary_is_role_scoped_and_stable_across_pages_filters` | PASSED LOCAL |
| T-IMP-022 | pagination/filter-invariant summary | `api/tests/integration/test_queue_analytics.py::test_summary_is_role_scoped_and_stable_across_pages_filters` | PASSED LOCAL |
| T-IMP-023 | source and actual priority | `api/tests/integration/test_queue_analytics.py::test_summary_is_role_scoped_and_stable_across_pages_filters` | PASSED LOCAL |
| T-IMP-024 | valid/null/negative resolution intervals | `api/tests/integration/test_queue_analytics.py::test_summary_is_role_scoped_and_stable_across_pages_filters` | PASSED LOCAL |
| T-IMP-025 | empty/cancel/refresh and stale state | `api/tests/integration/test_queue_analytics.py::test_empty_summary_has_no_invented_resolution_time`; `api/tests/integration/test_queue_controls.py::test_cancellation_requires_audited_reason_and_is_terminal`; `api/tests/browser/workflow_check.py` | PASSED LOCAL |
| T-IMP-030 | catalog/shared aliases | `api/tests/unit/test_extraction_safety_assessment.py::test_imp_030_shared_alias_retains_all_candidates_and_requires_choice` | PASSED LOCAL |
| T-IMP-031 | contradictory/unresolved cues | `api/tests/unit/test_extraction_safety_assessment.py::test_imp_031_conflicting_or_negated_locations_stay_unresolved`; `api/tests/unit/test_extraction_safety_assessment.py::test_imp_031_multiple_issue_cues_require_review_even_with_negation` | PASSED LOCAL |
| T-IMP-032 | original Unicode spans | `api/tests/unit/test_extraction_safety_assessment.py::test_imp_032_unicode_combining_marks_preserve_original_span_offsets` | PASSED LOCAL |
| T-IMP-033 | original transcript/evidence immutability | `api/tests/integration/test_roadmap_regressions.py::test_edit_preserves_original_and_locks_provenance_after_confirmation`; `api/tests/integration/test_workflow.py::test_audit_and_provider_provenance_are_immutable` | PASSED LOCAL |
| T-IMP-034 | explicit human confirmation | `api/tests/integration/test_workflow.py::test_idor_invalid_asset_and_unconfirmed_create_nothing`; `api/tests/integration/test_release_guards.py::test_numeric_confirmation_is_not_human_confirmation` | PASSED LOCAL |
| T-IMP-035 | corrected location/asset consistency | `api/tests/integration/test_workflow.py::test_idor_invalid_asset_and_unconfirmed_create_nothing`; `api/tests/browser/workflow_check.py` | PASSED LOCAL |
| T-IMP-036 | baseline safety regression/cache replay | `api/tests/unit/test_extraction_safety_assessment.py`; `api/tests/integration/test_asr_correction_recovery.py::test_asr_failure_recovers_with_explicit_review` | PASSED LOCAL |
| T-IMP-040 | offline WER/CER mathematics | `api/tests/unit/test_transcript_scoring.py::test_hand_computed_alignment`; `api/tests/unit/test_transcript_scoring.py::test_cer_uses_normalized_codepoints_without_whitespace` | PASSED LOCAL |
| T-IMP-041 | coverage and denominator honesty | `api/tests/unit/test_transcript_scoring.py::test_micro_average_failures_and_nonempty_denominators_are_distinct`; `api/tests/unit/test_transcript_scoring.py::test_missing_and_empty_references_are_unmeasured_not_perfect` | PASSED LOCAL |
| T-IMP-042 | private manifest and data preservation | `api/tests/unit/test_transcript_scoring.py::test_public_output_omits_transcripts_fields_conditions_and_original_ids`; `api/tests/unit/test_transcript_scoring.py::test_cli_rejects_hardlinked_output_without_changing_private_inputs` | PASSED LOCAL |
| T-IMP-043 | genuine frozen held-out corpus | `docs/evidence/improvement-asr-development.json` | DEFERRED |
| T-IMP-044 | split/fixture separation | `api/tests/unit/test_transcript_scoring.py::test_heldout_requires_predeclared_independence_and_stays_separate`; `api/tests/unit/test_transcript_scoring.py::test_private_manifest_rejects_invalid_or_mixed_cases` | PASSED LOCAL |
| T-IMP-050 | durable rolling cap | `api/tests/integration/test_provider_admission.py::test_actor_cap_is_shared_by_stt_tts_and_new_instances` | PASSED LOCAL |
| T-IMP-051 | concurrent shared STT/TTS cap | `api/tests/integration/test_provider_admission.py::test_global_cap_and_concurrent_operations_do_not_oversubscribe`; `api/tests/integration/test_provider_admission.py::test_concurrent_same_actor_limit_is_atomic` | PASSED LOCAL |
| T-IMP-052 | restart resilience | `api/tests/integration/test_provider_admission.py::test_actor_cap_is_shared_by_stt_tts_and_new_instances` | PASSED LOCAL |
| T-IMP-053 | DB-time expiry and bounded cleanup | `api/tests/integration/test_provider_admission.py::test_expired_reservations_release_capacity_by_database_time`; `api/tests/integration/test_provider_admission.py::test_cleanup_is_bounded_and_keeps_recent_reservations` | PASSED LOCAL |
| T-IMP-054 | pause and role denial | `api/tests/integration/test_provider_admission.py::test_pause_inactive_and_judge_do_not_reserve`; `api/tests/integration/test_provider_pause.py` | PASSED LOCAL |
| T-IMP-055 | fail-closed DB/commit errors | `api/tests/integration/test_provider_admission.py::test_admission_transaction_rolls_back_failed_commit`; `api/tests/integration/test_provider_admission.py::test_denied_database_admission_never_calls_provider_or_changes_saved_order` | PASSED LOCAL |
| T-IMP-056 | additive upgrade and old-app rollback compatibility | `api/tests/integration/test_provider_admission.py::test_0004_upgrade_preserves_domain_data_and_exposes_rollback_readiness_gate` | BLOCKED |
| T-IMP-060 | full CI-equivalent local quality suite | `docs/evidence/improvement-release.json` | PASSED LOCAL |
| T-IMP-061 | immutable data and readiness | `api/tests/integration/test_workflow.py::test_audit_and_provider_provenance_are_immutable`; `api/tests/integration/test_roadmap_regressions.py::test_readiness_fails_when_database_is_unavailable`; `api/tests/integration/test_foundation.py::test_live_and_ready` | PASSED LOCAL |
| T-IMP-062 | exact candidate CI/deployment | `docs/evidence/improvement-release.json` | BLOCKED |
| T-IMP-063 | candidate rollback rehearsal | `docs/evidence/improvement-rollback-compatibility.json` | BLOCKED |

### Explicit unfinished gates

- [ ] IMP-04B / T-IMP-043: participant-approved independent data, references and credit budget.
- [ ] IMP-05 / T-IMP-056: compatible old-app startup/readiness rollback image verified before production migration.
- [ ] IMP-06 / T-IMP-062: exact candidate remote CI/container, approved backup/restore and deployment.
- [ ] IMP-06 / T-IMP-063: candidate rollback/restoration evidence with preserved data.
- [ ] Participant-owned eligibility/contributions/video/public post/form.

30 planned checks pass locally, one is explicitly deferred and three remain blocked.
These dispositions follow sections 9.2, 10.1, 11 and 13 of the supplied specification.
No new provider call, recording campaign, secret rotation, public report or production
write was made. Local provisional reassessment is 91/100, with the unearned
held-out/deployment points withheld. The 95 target is not a verified outcome.
