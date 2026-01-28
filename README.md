# 🕷️ Web Scraping Éxito -- Demo Backend

Backend demo en **Python** que expone una API REST para buscar productos
en un e-commerce (Éxito), utilizando **Playwright** para web scraping.

El proyecto está diseñado con una **arquitectura limpia**, soporta
**integraciones habilitables por variables de entorno**, y puede
ejecutarse **localmente o con Docker**.

------------------------------------------------------------------------

## 🚀 Funcionalidad

-   Endpoint `GET /api/search`
-   Recibe el nombre de un producto (ej: `licuadora`)
-   Retorna los **primeros 3 resultados**
-   Soporta:
    -   🔌 Integración real (scraping)
    -   🧪 Datos mock (sin scraping)
-   Selección de integración controlada por `.env`

------------------------------------------------------------------------

## 🧠 Arquitectura (alto nivel)

    API (FastAPI)
       ↓
    SearchService
       ↓
    IntegrationResolver
       ↓
    [ ExitoScraper | MockProductsProvider ]

------------------------------------------------------------------------

## 📁 Estructura del proyecto

    app/
    ├── api/
    │   └── routes.py
    ├── core/
    │   └── config.py
    ├── models/
    │   └── product.py
    ├── services/
    │   ├── exito_scraper.py
    │   ├── mock_products_provider.py
    │   ├── integration_resolver.py
    │   └── search_service.py
    ├── main.py
    Dockerfile
    docker-compose.yml
    requirements.txt
    .env
    README.md

------------------------------------------------------------------------

## ⚙️ Variables de entorno

    EXITO_ENABLED=false

------------------------------------------------------------------------

## ▶️ Ejecución con Docker

    docker compose up --build

-   Swagger: http://localhost:8000/docs
-   Health: http://localhost:8000/health

------------------------------------------------------------------------

## ▶️ Ejecución local

    py -m venv venv
    venv\Scripts\activate
    py -m pip install -r requirements.txt
    playwright install
    python -m uvicorn app.main:app --reload

------------------------------------------------------------------------

## 📌 Endpoint

    GET /api/search?product=licuadora

------------------------------------------------------------------------

## 🛠️ Tecnologías

-   Python 3.12
-   FastAPI
-   Playwright
-   Docker
-   python-dotenv

------------------------------------------------------------------------

## 👤 Autor

José Gomez\
Arquitecto / Backend Developer
