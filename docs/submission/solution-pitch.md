# FieldSaarthi AI
## From a field worker's voice to an accountable repair
**Team:** Shubham Putitundi and Shambhavi Kumar  
**Repository:** https://github.com/rdx644/FieldSarthi-AI

**Problem.** Maintenance faults reported through informal calls and voice notes lose equipment, location and ownership context. Supervisors spend time interpreting reports instead of acting on them.

**Solution.** A worker records a short report in a selected language or uploads a consenting recording. Genuine Gnani Prisma speech recognition produces the transcript. FieldSaarthi matches approved equipment/location aliases, shows the supporting phrases, and asks the worker to correct and explicitly confirm every report. The server creates one durable PostgreSQL work order. A supervisor assigns a worker, sets priority, moves work through controlled states and records a resolution. An immutable history explains what was heard, corrected and done.

**Gnani integration.** Prisma v2.5 is verified with actual Hindi recordings, returned model/request IDs and a complete browser-to-database workflow. Optional Timbre v2.5 produces a verified Hindi WAV acknowledgment after saving; its failure never removes an order. Hindi/Hinglish is the validated speech baseline. English/Tamil are selectable, but equivalent recognition quality is not claimed without authentic evaluation.

**Engineering.** React/TypeScript, FastAPI, SQLAlchemy/Alembic and PostgreSQL; temporary bounded audio conversion; HTTP-only sessions and CSRF checks; role/ownership enforcement; transactional idempotency; optimistic versions and database-enforced audit/provenance protection. Tests, cross-model review, real integration evidence and a backup/restore drill support the claims.

**Demonstrated value.** A voice report becomes a reviewed, persisted task with a real owner and an inspectable resolution. Human confirmation and supervisor triage remain essential. All demo identities and operational data are synthetic.

**Status.** Reproducible local working build; public hosting and final submission must be independently confirmed. See repository evidence and the linked demonstration.
