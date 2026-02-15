from typing import List
import asyncio

from app.core.celery import celery_app
from app.services.search_service import SearchService


@celery_app.task(name="app.infrastructure.worker.celery_tasks.search_task", bind=True)
def search_task(self, product: str) -> List[dict]:
    """
    Tarea Celery que actúa como Wrapper para SearchService.
    """

    # Callback para reportar progreso a Celery de forma desacoplada
    def report_progress(current: int, total: int):
        self.update_state(state="PROCESSING", meta={"current": current, "total": total})

    service = SearchService()

    # Ejecutar búsqueda dentro del loop de asyncio necesario para el worker
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(
            service.search_and_format(product, on_progress=report_progress)
        )
    except Exception:
        # Dejar que Celery maneje la excepción nativamente para evitar errores de metadatos
        raise
    finally:
        loop.close()
