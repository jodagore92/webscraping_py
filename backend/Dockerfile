FROM python:3.13-slim

# Variables básicas
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT=/usr/local

# Instalar uv desde imagen distroless oficial
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copiar archivos de configuración
COPY pyproject.toml uv.lock ./

# Instalar dependencias Python con uv
RUN uv sync --frozen --no-dev --no-install-project

# Instalar navegadores de Playwright
RUN uv run playwright install --with-deps --only-shell

# Copiar el código
COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
