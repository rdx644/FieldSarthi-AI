# syntax=docker/dockerfile:1
FROM node:26-bookworm-slim AS frontend
WORKDIR /frontend
COPY web/package.json web/package-lock.json ./
RUN npm ci --ignore-scripts --no-audit
COPY web/ ./
RUN npm run build

FROM python:3.12-slim-bookworm AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 UV_LINK_MODE=copy
RUN pip install --no-cache-dir uv==0.11.1
WORKDIR /app/api
COPY api/pyproject.toml api/uv.lock ./
RUN uv sync --locked --no-dev
COPY api/app/ ./app/
COPY api/alembic/ ./alembic/
COPY api/alembic.ini ./
COPY api/scripts/start.py ./scripts/start.py
COPY --from=frontend /frontend/dist /app/web/dist
RUN useradd --create-home --uid 10001 fieldsaarthi && mkdir -p /app/private && chown -R fieldsaarthi:fieldsaarthi /app
ENV PATH="/app/api/.venv/bin:$PATH" APP_ENV=production
USER fieldsaarthi
EXPOSE 8000
CMD ["python", "scripts/start.py"]
