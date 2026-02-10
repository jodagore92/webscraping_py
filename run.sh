#!/bin/bash
set -e

echo "🚀 Sincronizando dependencias con uv..."
uv sync

echo "📥 Instalando navegadores de Playwright..."
.venv/bin/playwright install

echo "▶️  Iniciando API en modo desarrollo..."
uv run python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
