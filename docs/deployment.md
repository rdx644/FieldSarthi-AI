# Deployment package - Render submission demo
User approved using the verified Gnani key for hosting and supplied https://github.com/rdx644/FieldSarthi-AI.git. No hosted URL is claimed yet.

A multi-stage non-root Docker image builds React, installs the frozen Python lockfile and serves the entire app from one FastAPI origin. `scripts/start.py` applies migrations and seeds before starting exactly one Uvicorn worker. Render Blueprint `render.yaml` provisions a free Singapore web service and separate free PostgreSQL 18 database. TLS is platform-managed. Auto-deploy is disabled so releases are deliberate.

1. Publish the reviewed repository; connect that GitHub repository to Render.
2. Create a Blueprint from this repository and review `render.yaml`.
3. Enter private GNANI_API_KEY_ID and the three strong DEMO_*_PASSWORD values. JWT_SECRET is generated; DATABASE_URL is supplied from the managed database. Never add these to Git or frontend variables.
4. Review that both resources remain on the free plan; no paid upgrade is authorized by this package.
5. Deploy and verify /health/ready over HTTPS, login, microphone permission, newly spoken voice, genuine Gnani provenance, order confirmation, supervisor resolution, refresh and optional TTS.
6. Record the real hosted URL and smoke evidence in release-gate.md; do not substitute a local test for this step.

The standard Render PostgreSQL connection URL is normalized to SQLAlchemy's psycopg driver. Runtime cookies are Secure in production; same-origin browser requests use the CSRF header. CORS permits no external origins in the Blueprint; add exact trusted origins only if the architecture changes.

**Limitations:** free services sleep after inactivity; free databases expire after 30 days. Do not present this as enterprise production hosting. The Docker image built successfully in GitHub CI. Local Docker execution and public hosted execution are not claimed. The local native application and its real provider workflow were verified separately.

Sources checked: https://render.com/docs/blueprint-spec , https://render.com/docs/free , https://render.com/docs/postgresql-creating-connecting , https://docs.astral.sh/uv/guides/integration/docker/ .
