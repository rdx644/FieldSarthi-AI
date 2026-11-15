# IMP-03 conservative extraction assessment

The November 14, 2026 read-only replay retained `rules-v4`. No parser or production
catalog changes were made. The frozen development corpus still yields **12/15
automatic complete cases**, location **12/14**, asset **11/14**, issue **13/14**,
priority suggestion **14/14**, and all **6/6 expected safety blocks**. No previously
correct complete case regressed. See [sanitized evidence](../evidence/improvement-extraction.json).

NLP-04 and NLP-12 contain zero exact catalog location matches and one equipment
candidate. NLP-14 contains one location match but zero equipment candidates and an
unresolved issue. None is a shared-alias ambiguity: filtering equipment candidates
by location cannot recover absent words. Adding aliases derived from those errors
without separate semantic evidence could turn unrelated words into inventory facts.
Explicit review and correction remain the safe recovery path. No recall or accuracy
increase is claimed.

## Reproduce without provider requests

From `api/`, with cached lawful transcripts retained under ignored `private/` and
`TEST_DATABASE_URL` configured for **only `fieldsaarthi_test`**:

```powershell
.venv/Scripts/python.exe -m scripts.replay_cached_extraction --results ../private/evaluation/results --output ../docs/evidence/improvement-extraction.json
.venv/Scripts/python.exe -m pytest tests/unit/test_extraction_safety_assessment.py -q
```

The helper validates all 15 cached labels against the reviewed case manifest,
selects existing active catalogs inside a PostgreSQL read-only transaction and
emits only counts, pseudonymous case IDs and field names. It does not seed/reset
the database, modify cached files, call Gnani or publish transcripts/request IDs.
An existing seed catalog is required. Run database checks sequentially with the
project's integration/browser suite because those suites reset the test schema.
Use the Python module invocation above so application imports resolve correctly.

The 17 synthetic no-database tests cover shared aliases and retained candidates,
contradictory/negated locations, multiple issue cues including negation, unknown
equipment, floor-only wording, token boundaries, catalog-code/romanized variants,
Unicode combining marks with original source offsets, always-required human review,
and replay privacy/database-name safeguards. They are regression fixtures, not
ASR accuracy evidence. `rules-v4` does not claim general semantic negation
understanding; a human must check every suggestion, including a lone negated cue.

This is a replay of the development corpus previously used to refine rules.
It is neither held-out generalization nor a new STT/WER/CER measurement. Existing
provider-error and no-speech safety cases retain their original scoring semantics.

November 15: the same read-only cached replay again produced unchanged counts and no regressions; [fresh evidence](../evidence/improvement-extraction-final.json). The three private cached correction replays passed 3/3 without provider calls. Keep the November 14 artifact above unchanged.
