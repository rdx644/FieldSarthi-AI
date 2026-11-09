# Authentic 15-recording evaluation

Prepare 15 separate consenting team recordings using the machine-readable
[audio cases](audio-cases.json), derived from the team's private implementation plan. Do not use generated speech,
third-party recordings or one recording copied into multiple cases. NLP-15 is
deliberate silence/background hiss. State any accent/code-mix/noise limitations.

The private working directory is `private/evaluation/`. The prepared
`manifest.json` maps NLP-01..NLP-15 to filenames, selected language and expected
fields. Save clips as NLP-01.wav..NLP-15.wav; for WebM/M4A change the `file` value.
Keep each clip under 25 seconds, maximum 30 seconds and 10 MiB. Read and correct
the expected labels to match what was actually said **before** the live run.
The Hindi light example is explicitly labelled MECHANICAL for “खराब”; no electrical
cause is inferred from the asset type alone.

From `api`, using the normal local migrated catalog database:

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluate_audio --prepare
# Free validation: requires all 15 files and rejects duplicate normalized audio.
.\.venv\Scripts\python.exe -m scripts.evaluate_audio
# Only after consent and ground truth have actually been reviewed:
.\.venv\Scripts\python.exe -m scripts.evaluate_audio --live --consent --ground-truth-reviewed
```

The live command makes genuine Gnani requests with retries disabled and checkpoints
each response privately. Repeating it reuses completed matching results. If a
recording or label changed, archive the existing case result deliberately before
rerunning; that new request may spend credits. Configuration, quota or outage
errors stop further requests. Raw recordings/transcripts remain ignored. Only
sanitized per-field/complete-case results and real model/request metadata are
exported to `docs/evidence/audio-evaluation.json` after a full run.

Target: at least 12/15 complete cases correct and every required ambiguity/no-speech
case safely blocked. Report the actual count even if the target is missed.
No WER/CER or broad multilingual quality claim is produced by this small corpus.
