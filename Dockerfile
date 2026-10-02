FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# Install dependencies first so this layer is cached between builds
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8000

CMD [".venv/bin/fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
