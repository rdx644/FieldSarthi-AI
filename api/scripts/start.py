"""One-worker deployment entry point. Run migrations before accepting traffic."""

import os
import subprocess
import sys

subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], check=True)
subprocess.run([sys.executable, "-m", "app.seed"], check=True)
os.execvp(
    "uvicorn",
    [
        "uvicorn",
        "app.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        os.environ.get("PORT", "8000"),
        "--workers",
        "1",
        "--proxy-headers",
        "--forwarded-allow-ips",
        "*",
        "--no-access-log",
    ],
)
