from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(
    title="Web Scraping Éxito Demo",
    description="API demo para scraping de productos del Éxito usando Playwright",
    version="1.0.0",
)

# Registrar rutas
app.include_router(api_router, prefix="/api")

# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "message": "API running correctly"
    }
