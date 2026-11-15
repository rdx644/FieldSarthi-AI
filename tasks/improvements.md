# FieldSaarthi improvement plan - current finalisation status

Source: `Downloads/FieldSaarthi_AI_95_Improvement_Specification.md`.
Baseline: `0fca9716e3589eb9cac70f12e2468aacf7cadb5a`.

**Local engineering, source compatibility and real container rollback are verified.**
The participant explicitly approved deferring independent audio evaluation.
Production release is pending exact source CI, an approved backup and deployment.
No requirement was silently waived. The previous [audit](../docs/evidence/improvement-completion-audit.json)
and [handoff](../docs/improvement-handoff.md) preserve the earlier 30-pass/3-blocked checkpoint;
this status supersedes those local compatibility blockers.

- [x] IMP-00: archive/security guard and tracked-only exports.
- [x] IMP-01: reviewer docs, restricted judge navigation and all direct API denials.
- [x] IMP-02: SQL role-scoped dashboard counts, correct paging/filter/source/time semantics.
- [x] IMP-03: safer review UX; conservative rules-v4 retained with 6/6 safety outcomes.
- [x] IMP-04A: offline metrics, manifests, privacy and private-input preservation.
- [x] IMP-04B disposition: participant-approved deferral; no independent accuracy claim.
- [x] IMP-05 local: durable admissions and a separate verified compatibility rollback build.
- [x] IMP-06 local: 307 backend tests, strict checks and actual four-phase Docker rehearsal.
- [ ] IMP-06 external: exact source CI, approved private production backup and staged release.

Candidate code: `c94e06f04dfb75c8e1384298ea2dc1aaa2fea4ff`.
Compatibility build: `be608cb4ea807d8fd0280633f05595e89d83fb2d`, branch `release/schema-compatibility`.
The compatibility build is a rollback artifact, not a feature merge target; it
forces paid speech paused, accepts only exact schemas 0004/0005 and never migrates
the database at startup. The candidate retains strict 0005 readiness and durable
admissions. Deploy compatibility first at 0004, then activate the candidate.

## All planned test identifiers

The meanings below follow section 12 of the supplied specification. Earlier
010..012 and 020..025 labels were reordered in the old audit; this matrix corrects
the labels while preserving all test coverage.

| ID | Requirement | Actual verification | Status |
|---|---|---|---|
| T-IMP-001 | guarded archive | `api/tests/unit/test_repository_guard.py::test_imp_001_clean_archive_is_allowed` | PASSED LOCAL |
| T-IMP-002 | synthetic forbidden paths/secrets | `api/tests/unit/test_repository_guard.py::test_imp_001_archive_checks_paths_and_contents_without_disclosing_secrets`; `api/tests/unit/test_repository_guard.py::test_imp_002_backup_archive_and_runtime_paths_are_blocked` | PASSED LOCAL |
| T-IMP-010 | judge access and hidden-report denial | `api/tests/integration/test_judge_access.py::test_public_judge_is_read_only_and_sees_only_approved_reports` | PASSED LOCAL |
| T-IMP-011 | desktop/mobile quick review | `api/tests/browser/workflow_check.py` | PASSED LOCAL |
| T-IMP-012 | current documentation consistency | `docs/evidence/improvement-documentation-check.json` | PASSED LOCAL |
| T-IMP-020 | more than 20 orders and pagination | `api/tests/integration/test_queue_analytics.py::test_summary_is_role_scoped_and_stable_across_pages_filters` | PASSED LOCAL |
| T-IMP-021 | scope and filter invariance | `api/tests/integration/test_queue_analytics.py::test_summary_is_role_scoped_and_stable_across_pages_filters` | PASSED LOCAL |
| T-IMP-022 | source/status/operational priority counts | `api/tests/integration/test_queue_analytics.py::test_summary_is_role_scoped_and_stable_across_pages_filters` | PASSED LOCAL |
| T-IMP-023 | empty results and valid/null resolution time | `api/tests/integration/test_queue_analytics.py::test_empty_summary_has_no_invented_resolution_time`; `api/tests/integration/test_queue_analytics.py::test_summary_is_role_scoped_and_stable_across_pages_filters` | PASSED LOCAL |
| T-IMP-024 | role count leakage | `api/tests/integration/test_queue_analytics.py::test_summary_is_role_scoped_and_stable_across_pages_filters` | PASSED LOCAL |
| T-IMP-025 | browser refresh and stale state | `api/tests/browser/workflow_check.py` | PASSED LOCAL |
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
| T-IMP-043 | genuine frozen held-out corpus | `docs/evidence/improvement-evaluation-disposition.json` | DEFERRED BY PARTICIPANT |
| T-IMP-044 | split/fixture separation | `api/tests/unit/test_transcript_scoring.py::test_heldout_requires_predeclared_independence_and_stays_separate`; `api/tests/unit/test_transcript_scoring.py::test_private_manifest_rejects_invalid_or_mixed_cases` | PASSED LOCAL |
| T-IMP-050 | durable rolling cap | `api/tests/integration/test_provider_admission.py::test_actor_cap_is_shared_by_stt_tts_and_new_instances` | PASSED LOCAL |
| T-IMP-051 | concurrent shared STT/TTS cap | `api/tests/integration/test_provider_admission.py::test_global_cap_and_concurrent_operations_do_not_oversubscribe`; `api/tests/integration/test_provider_admission.py::test_concurrent_same_actor_limit_is_atomic` | PASSED LOCAL |
| T-IMP-052 | restart resilience | `api/tests/integration/test_provider_admission.py::test_actor_cap_is_shared_by_stt_tts_and_new_instances` | PASSED LOCAL |
| T-IMP-053 | DB-time expiry and bounded cleanup | `api/tests/integration/test_provider_admission.py::test_expired_reservations_release_capacity_by_database_time`; `api/tests/integration/test_provider_admission.py::test_cleanup_is_bounded_and_keeps_recent_reservations` | PASSED LOCAL |
| T-IMP-054 | pause and role denial | `api/tests/integration/test_provider_admission.py::test_pause_inactive_and_judge_do_not_reserve`; `api/tests/integration/test_provider_pause.py` | PASSED LOCAL |
| T-IMP-055 | fail-closed DB/commit errors | `api/tests/integration/test_provider_admission.py::test_admission_transaction_rolls_back_failed_commit`; `api/tests/integration/test_provider_admission.py::test_denied_database_admission_never_calls_provider_or_changes_saved_order` | PASSED LOCAL |
| T-IMP-056 | additive upgrade and old-app rollback compatibility | `api/tests/integration/test_compatibility_release.py` | PASSED LOCAL |
| T-IMP-060 | full CI-equivalent local quality suite | `docs/evidence/improvement-release.json` | PASSED LOCAL |
| T-IMP-061 | immutable data and readiness | `api/tests/integration/test_workflow.py::test_audit_and_provider_provenance_are_immutable`; `api/tests/integration/test_roadmap_regressions.py::test_readiness_fails_when_database_is_unavailable`; `api/tests/integration/test_foundation.py::test_live_and_ready` | PASSED LOCAL |
| T-IMP-062 | exact candidate CI/deployment | `docs/evidence/improvement-release.json` | PENDING RELEASE |
| T-IMP-063 | candidate rollback rehearsal | `api/tests/container/release_check.py`; `api/tests/integration/test_compatibility_release.py` | PASSED LOCAL |

## Scope and release decision

32 checks pass locally, independent evaluation is deferred by explicit participant
decision, and one release gate remains pending. The image rehearsal preserved all
seven domain tables, one synthetic order/audit/idempotency workflow and both
admission records through stage -> activation -> rollback -> restoration.
The internal test network had no provider access or host-port exposure.

A production backup requires a temporary current-operator-IP/32 ingress rule,
a consistent read-only export, isolated local restore, and restoration of the
original ingress allowlist. Deployment and this infrastructure change require
approval of the concrete release plan. Do not down-migrate, delete data, rotate
accounts or change the public judge allowlist. Participant submission stays owned
by the participant. No new speech call or production action was made.

See [current release details](../docs/release-finalisation.md),
[finalisation audit](../docs/evidence/improvement-finalisation-audit.json) and
[release evidence](../docs/evidence/improvement-finalisation-release.json).
