# Offline ASR scoring (IMP-04A)

Requirements: FR-06–15; NFR-01/02/03/05/06/09/13/14. Test mapping:
T-IMP-040/041/042/044 → `api/tests/unit/test_transcript_scoring.py`.
These tests use synthetic text fixtures, never genuine speech-quality evidence.

From `api/`, run the network-free scorer against two explicit **private** JSON files:

```powershell
.venv/Scripts/python.exe scripts/score_transcripts.py --manifest ../private/scoring/development.json --transcripts ../private/scoring/results.json --dataset-id development-v1 --parser-version rules-v4 --output ../private/scoring/summary.json
```

On Linux use `uv run python` in place of `.venv/Scripts/python.exe`. The script
imports only Python's standard library, reads no environment configuration, and
has no network, database, provider or audio-decoding path. It does not run the
parser: observed fields must come from a separately verified, matching parser
run. An explicit parser version is a label/check against supplied observations,
not proof that the requested parser was executed.

## Input contract, schema version 1

The following is a **synthetic schema example**, not an audio measurement. Keep
real transcripts, conditions, original IDs and field values in ignored `private/`.

Private manifest:

```json
{
  "schema_version": 1,
  "dataset_id": "development-v1",
  "split": "development",
  "evidence_kind": "synthetic_fixture",
  "conditions": {"noise": "text fixture only"},
  "cases": [{
    "case_id": "TEST-01",
    "language_code": "en-IN",
    "spoken_language_tags": ["English"],
    "reference_transcript": "pump is leaking",
    "reference_verified": true,
    "consent_obtained": true,
    "audio_duration_seconds": 2,
    "expected_fields": {
      "location_code": "LOCATION-TEST",
      "asset_code": "PUMP-TEST",
      "issue_category": "LEAKAGE",
      "priority_suggestion": "NORMAL"
    },
    "expected_safety_block": false
  }]
}
```

Separate private responses file:

```json
[{
  "case_id": "TEST-01",
  "provider_status": "success",
  "transcript": "pump leaking",
  "parser_version": "rules-v4",
  "observed_fields": {
    "location_code": "LOCATION-TEST",
    "asset_code": "PUMP-TEST",
    "issue_category": "LEAKAGE",
    "priority_suggestion": "NORMAL"
  },
  "safety_blocked": false
}]
```

The standalone validator in `scripts/score_transcripts.py` enforces this contract:

- Manifest `dataset_id` must equal `--dataset-id`. Dataset/parser labels are
  1–80 ASCII letters, digits, dots, underscores or hyphens, starting alphanumeric.
  Use pseudonymous dataset IDs. `conditions` is a private object, never exported.
- `split` is exactly `development` or `heldout`; `evidence_kind` is exactly
  `genuine_human_audio` or `synthetic_fixture`. Per-case overrides must agree.
  Never combine fixtures and genuine recordings, or development and held-out data.
- A held-out manifest additionally requires `independence` with
  `independent_of_tuning: true`, `criteria_frozen_before_evaluation: true`, and
  `frozen_source_sha` containing the complete 40-character Git SHA. These are
  operator attestations; the scorer cannot establish independence itself.
- Each case has a unique nonempty private ID with exactly one result. Missing,
  extra or duplicate results are rejected; failures cannot silently disappear.
  `provider_status` is `success`, `failed` or `empty`. A failed result may retain
  private text but that text receives no ASR or field success credit. Empty status
  requires empty text. Every result must name the requested `parser_version`.
  Results accept exactly the documented keys plus optional `error_code`; unsupported
  status flags such as `success`/`attempted` are rejected. A success/empty result
  cannot also carry an error code. Map cached provider records explicitly into
  this schema; do not pass raw provider payloads. Every row attests an actual
  attempted input; the scorer cannot independently authenticate that fact.
- Selected `language_code` is `hi-IN`, `en-IN` or `ta-IN`. Spoken tags are one or
  more unique values from Hindi/English/Hinglish/Tamil. Support for metadata does
  not establish Tamil speech readiness. Tag groups overlap; never sum them.
- Consent must be explicitly true; duration must be finite and greater than zero,
  at most 30 seconds. References/transcripts are bounded to 4,000 codepoints, input
  files to 16 MiB each and cases to 1,000. Larger datasets require a reviewed change.
- A reference is either null (unavailable) or independently verified text with
  `reference_verified: true`. A prompt/script or ASR-derived correction does not
  establish a verified human reference. Empty/punctuation-only references remain
  unscorable for WER/CER; their count stays visible.
- `expected_fields`/`observed_fields` accept only `location_code`, `asset_code`,
  `issue_category` and `priority_suggestion`. Omit field expectations if unmeasured.
  A missing observed key is incorrect even when expected value is null. Safety
  expectation/observation is boolean or null (unmeasured). Ground truth is reviewed
  before evaluation and not regenerated from observations.
- Optional `expected_error: "NO_SPEECH_DETECTED"` is permitted only with no field
  expectations and `expected_safety_block: true`; the response needs matching
  `error_code` and failed status. A transport error never earns safety credit.

## Normalization and denominators

Freeze this policy before scoring: Unicode NFC, casefold, Unicode punctuation
replaced by spaces, whitespace collapsed. Scripts, diacritics, number spellings,
digits and loan words remain literal; no transliteration or number conversion.
Hindi `पानी` and romanized `paani` mismatch. Words are whitespace tokens. CER uses
Unicode codepoints with all whitespace excluded, **not grapheme clusters**.

Levenshtein alignment uses unit insertion/deletion/substitution cost; equal-cost
ties choose substitution, deletion, insertion in that order. WER/CER are corpus
micro-averages: summed edits / summed reference units, with edit counts, reference
units and scored-case counts exported. A WER above 1.0 is legitimate. A zero
denominator produces null, never a perfect score.

Coverage is raw nonempty successful transcripts / all attempted cases. End-to-end
WER/CER includes every attempted case with a valid nonempty verified reference;
failed/empty results are all deletions. Successful-nonempty WER/CER is separately
named and excludes failures; missing/empty references are counted explicitly.
Per-field correctness reports both all expected cases and successful nonempty
cases, so it cannot be confused with historical 14-case field denominators.

Automatic complete-case count uses all attempted cases as its denominator and
requires all **four** field expectations and any safety expectation to match;
partial/missing field expectations earn per-field credit only. An explicitly
expected and observed no-speech
error can pass a silence case. Safety false accepts/blocks are measured only with
actual usable observations; transport outages are unassessed. Correction recovery
is explicitly not measured. Selected-language and spoken-tag breakdowns use the
same policies and retain all relevant failures.

## Privacy, reproducibility and current limitations

Output contains aggregate metrics, pseudonyms `CASE-0001` in frozen manifest order,
normalization, split/kind/version labels, validated held-out freeze metadata when
applicable and input SHA256 hashes. It omits original
case IDs, transcripts, field values, raw conditions, provider IDs, paths and audio.
Errors do not echo input values. Output cannot overwrite either resolved input
path or an existing hard link to either input (checked using filesystem identity). Freeze manifest ordering and retain private inputs to reproduce the report.
Review the sanitized summary before explicitly publishing it.

On 2026-11-14, the existing private 15-case manifest had recording prompts and
field ground truth but **zero explicitly verified reference transcripts**. The
prompts were not promoted to references. Existing genuine 12/15 complete-case,
14/15 nonempty, 6/6 expected blocks and 3/3 correction evidence remains historical
and unchanged. Development WER/CER is currently **not measured**; verified human
references are needed before scoring cached responses. Held-out genuine evaluation
is deferred pending independent consented data and explicit live-call approval.
