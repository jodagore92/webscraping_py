from typing import List
import asyncio

from app.core.celery import celery_app
from app.services.search_service import SearchService
from app.core.logger import logger


@celery_app.task(name="app.infrastructure.worker.celery_tasks.search_task", bind=True)
def search_task(self, product: str) -> List[dict]:
    """
    Tarea Celery que actúa como Wrapper para SearchService.
    """
    logger.info(f"Iniciando tarea de búsqueda para: {product}")

    # Callback para reportar progreso a Celery de forma desacoplada
    def report_progress(current: int, total: int):
        self.update_state(state="PROCESSING", meta={"current": current, "total": total})

    service = SearchService()

    # Ejecutar búsqueda dentro del loop de asyncio necesario para el worker
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(
            service.search_and_format(product, on_progress=report_progress)
        )
        logger.info(f"Tarea completada exitosamente para: {product}")
        return result
    except Exception as e:
        logger.error(f"Falla en la tarea de búsqueda para {product}: {str(e)}")
        # Dejar que Celery maneje la excepción nativamente para evitar errores de metadatos
        raise
    finally:
        loop.close()
