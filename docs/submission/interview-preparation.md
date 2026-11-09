# Technical interview preparation - roadmap section 20

Use the source and executed evidence below. Participants must supply their own contribution statements; this guide does not assign authorship or claim a rehearsal has happened.

| Topic | Explain using actual implementation / evidence |
|---|---|
| Why Gnani? | Prisma v2.5 supplies actual speech recognition; the application supplies extraction, catalog validation and workflow. See `api/app/integrations/gnani.py` and `docs/evidence/gnani-stt-live.md`. Timbre v2.5 was requested for optional Hindi acknowledgment; do not claim the TTS response echoed a model ID. |
| Input/output contract | Backend multipart `audio_file`, one selected language and model; real nonempty transcript/model/request ID; bounded typed failures, no fabricated metadata. |
| Browser audio | MediaRecorder detects supported formats. Server FFmpeg normalizes to mono 16 kHz PCM; actual decoded sample count bounds duration. A separate ffprobe is intentionally unnecessary; see architecture. |
| Provider outage | Bounded retries on selected transient failures; no retry on auth/credits/input errors or ambiguous read timeout. Failed STT cannot become a confirmed order; TTS is separate after persistence. |
| Wrong equipment | Unicode alias matching against seeded catalog; unresolved fields require review; server rejects wrong asset/location. Explain missing exact-span/parser-version gaps in the audit. |
| Duplicate/race prevention | Advisory key lock, intake row lock, unique intake, canonical-body hash; order/audit/idempotency write atomically. Workflow uses row lock and expected version. |
| Data model | Seven relational tables, original and corrected transcript separate, immutable audit/provider triggers; administrative DB owners remain privileged. |
| Accuracy | 15/15 measured parser text fixtures are not 15 audio cases. One real Hindi baseline and prerecorded browser proof exist; authentic multilingual ASR evaluation remains pending. No invented WER/CER or confidence score. |
| Threat model | Backend secrets, Argon2, current-DB RBAC/ownership, cookie CSRF, bounded media, safe text rendering, synthetic data and temporary audio. Dedicated missing negative tests are listed in the audit; no full pentest claim. |
| Scaling | Single worker and in-memory budget are deliberate demo limits. Shared persistent limits, queue/concurrency design, capacity measurements and a managed backup plan are needed before scaling. Telephony/streaming remain future work. |
| Personal contribution | Each member should identify actual commits/modules/tests, decisions and defects they handled. Confirm this privately; do not infer authorship from team membership or AI-generated code. |
| Lightweight CMMI | Requirements, RTM, risks, evidence and protected checks aid traceability; no certification claim. G3/G4/G5 need their actual evidence regardless of CI success. |

Before the interview, each member should rehearse the full working flow and explain one error path. Before submission, record the required 2-3 minute video; the optional 60-second cut is a separate showcase.
