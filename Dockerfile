# ============================================================================
# OverWatch - Advanced System Monitoring CLI Tool
# Multi-stage build for minimal image size
# ============================================================================
# Build:  docker build -t overwatch .
# Run:    docker run -it overwatch
# API:    docker run -p 8000:8000 overwatch api
# ============================================================================

FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt pyproject.toml setup.py README.md ./
COPY overwatch/ ./overwatch/

RUN pip install --no-cache-dir --prefix=/install .

# --- Runtime ---
FROM python:3.12-slim

LABEL maintainer="Yasir N. <y451rmahar@gmail.com>"
LABEL description="OverWatch - Advanced System Monitoring CLI Tool"
LABEL url="https://github.com/sudoyasir/overwatch"
LABEL version="0.1.0"

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy source (for plugins directory)
COPY overwatch/ /app/overwatch/
WORKDIR /app

# Healthcheck for API mode
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" 2>/dev/null || exit 0

# Default: launch dashboard
ENTRYPOINT ["overwatch"]
CMD ["start"]

# Expose API port (used when running: docker run -p 8000:8000 overwatch api)
EXPOSE 8000
