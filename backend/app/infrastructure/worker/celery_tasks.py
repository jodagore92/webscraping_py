from typing import List
import asyncio

from app.core.celery import celery_app
from datetime import datetime, timezone
from app.services.search_service import SearchService
from app.services.database_factory import DatabaseFactory
from app.core.logger import logger


@celery_app.task(name="app.infrastructure.worker.celery_tasks.search_task", bind=True)
def search_task(self, product: str, user_id: str = None) -> List[dict]:
    """
    Tarea Celery que actúa como Wrapper para SearchService.
    """
    job_id = self.request.id
    logger.info(
        f"Iniciando tarea de búsqueda para: {product} (Job ID: {job_id}, User ID: {user_id})"
    )

    # Callback para reportar progreso a Celery de forma desacoplada
    def report_progress(current: int, total: int):
        self.update_state(state="PROCESSING", meta={"current": current, "total": total})

    service = SearchService()
    db = DatabaseFactory.get_database()

    # Ejecutar búsqueda dentro del loop de asyncio necesario para el worker
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(
            service.search_and_format(product, on_progress=report_progress)
        )

        # Guardar en base de datos
        loop.run_until_complete(
            db.save_search_result(
                job_id,
                {
                    "search_query": product,
                    "user_id": user_id,
                    "result": result,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                },
            )
        )

        logger.info(f"Tarea completada y guardada en BD para: {product}")
        return result
    except Exception as e:
        logger.error(f"Falla en la tarea de búsqueda para {product}: {str(e)}")
        # Dejar que Celery maneje la excepción nativamente para evitar errores de metadatos
        raise
    finally:
        loop.close()
