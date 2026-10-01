FROM python:3.10-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/install/bin:$PATH" \
    PORT=8000

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml setup.cfg* setup.py* README.md* ./

COPY tachyroute/ ./tachyroute/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install .[serve] \
        --extra-index-url https://download.pytorch.org/whl/cpu \
        --prefix=/install ".[serve]"

FROM python:3.10-slim AS runner

WORKDIR /app

RUN groupadd -r -g 10001 appuser && \
    useradd -r -u 10001 -g appuser -d /app -s /sbin/nologin appuser

COPY --from=builder /install /usr/local

COPY --chown=appuser:appuser tachyroute ./tachyroute/

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    &&  rm -rf /var/lib/apt/lists/*

COPY . .

USER appuser

EXPOSE 8000

CMD ["python", "-m", "tachyroute.cli", "--host", "0.0.0.0", "--port", "8000"]
