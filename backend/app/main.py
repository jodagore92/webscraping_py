from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.routes import router as api_router
from app.api.auth_routes import router as auth_router
from app.api.user_routes import router as user_router
from app.core.celery import celery_app
from app.infrastructure.queue.celery_adapter import CeleryAdapter
from app.services.queue_factory import QueueFactory
from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicializa recursos al startup y limpia al shutdown"""
    # Startup
    queue_adapter = CeleryAdapter(celery_app)
    QueueFactory.init(queue_adapter)
    logger.info("✓ QueueFactory inicializado con Celery")

    yield

    # Shutdown
    logger.info("✓ Aplicación cerrada")


app = FastAPI(
    title="Sistema comparador de precios",
    description="API scraping de productos en ecommerce",
    version="2.0.0",
    lifespan=lifespan,
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, usa ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(auth_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(api_router, prefix="/api")


# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "API running correctly"}
