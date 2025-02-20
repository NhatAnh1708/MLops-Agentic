FROM python:3.11-slim-bookworm AS base

FROM base AS builder
COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
COPY uv.lock pyproject.toml /app/


RUN apt-get update && apt-get install -y \
    gcc \
    portaudio19-dev \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcups2 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-install-project --no-dev

RUN pip install playwright
RUN playwright install

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev

FROM base
COPY --from=builder /app /app
ARG LOGFIRE_TOKEN
ENV LOGFIRE_TOKEN=$LOGFIRE_TOKEN
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 80
CMD ["/app/.venv/bin/fastapi", "dev", "app/server.py", "--port", "80", "--host", "0.0.0.0"]
