# 🕷️ Web Scraping Pro -- Multi-Tenant Backend

Backend profesional en **Python 3.13** que expone una API REST para buscar productos en múltiples e-commerce simultáneamente (Éxito, Alkosto), utilizando **Playwright** para web scraping, **Celery** para procesamiento asíncrono y **MongoDB** para persistencia de usuarios y resultados.

El proyecto está diseñado bajo los principios de **Arquitectura Hexagonal (Puertos y Adaptadores)**, permitiendo un desacoplamiento total entre la lógica de negocio y la infraestructura (Bases de datos, Mensajería, Scrapers).

---

## 🚀 Funcionalidades Actuales

- **Sistema de Usuarios y Seguridad**: 
    - Registro e inicio de sesión con **JWT (OAuth2)**.
    - Contraseñas cifradas con **Bcrypt**.
    - **Roles de Usuario**: Soporte para `ADMIN` y `GENERAL`.
- **Búsqueda Multi-Proveedor**: 
    - Scrapers reales optimizados para **Éxito** y **Alkosto** (concurrencia mediante `asyncio`).
    - Búsquedas asíncronas vía **Celery** para evitar bloqueos.
- **Persistencia y Consultas**: 
    - Almacenamiento distribuido en **MongoDB 8.0**.
    - **Historial de Búsquedas**: Cada usuario tiene acceso a su propio historial con soporte para **Paginación**.
- **Configuración Robusta**: Variables de entorno estrictamente validadas con **Pydantic Settings** (Zero Hardcoded Defaults).

---

## 🧠 Arquitectura

```mermaid
graph TD
    subgraph "Capa de Presentación (Input)"
        Auth_API[app/api/auth_routes.py]
        User_API[app/api/user_routes.py]
        Search_API[app/api/routes.py]
    end

    subgraph "Capa de Aplicación (Casos de Uso)"
        UC_Auth[Login/Register Use Cases]
        UC_Search[Search Use Cases]
        UC_History[Get History Use Case]
    end

    subgraph "Capa de Infraestructura (Adaptadores)"
        DB_Mongo[app/infrastructure/database/mongo_adapter.py]
        Queue_Celery[app/infrastructure/queue/celery_adapter.py]
        Scrap_Playwright[app/infrastructure/scraping/providers/]
    end

    subgraph "Worker Asíncrono"
        Worker[app/infrastructure/worker/celery_tasks.py]
    end

    Search_API --> UC_Search
    UC_Search --> Queue_Celery
    Queue_Celery -.->|Publish| Worker
    Worker --> UC_Search
    UC_Search --> DB_Mongo
    Auth_API --> UC_Auth
    UC_Auth --> DB_Mongo
    User_API --> UC_History
    UC_History --> DB_Mongo
```

---

## 📁 Estructura del Proyecto

```text
app/
├── api/                       # Interfaces REST (FastAPI)
│   ├── auth_routes.py         # Registro y Login
│   ├── user_routes.py         # Perfil e Historial
│   └── routes.py              # Endpoints de búsqueda
├── application/               # Lógica de Orquestación (Casos de Uso)
├── core/                      # Configuración Global, Celery, Seguridad, Logs
├── infrastructure/            # Adaptadores Técnicos
│   ├── database/              # Persistencia (MongoDB Adapter)
│   ├── queue/                 # Mensajería (Celery Adapter)
│   ├── scraping/              # Implementación de Scrapers (Playwright)
│   └── worker/                # Tareas de Celery
├── models/                    # Entidades de Dominio (Pydantic/User/Product)
├── services/                  # Lógica de Negocio (SearchService, Factories)
└── main.py                    # Punto de entrada FastAPI
```

---

## ⚙️ Configuración (.env)

El proyecto utiliza un sistema de configuración estricto. **No se permiten valores por defecto quemados** en el código. Para iniciar, debes copiar el template:

```bash
cp .env.template .env
```

### Variables requeridas:
- `REDIS_URL`: Broker de Celery (ej. `redis://redis:6379/0`).
- `MONGO_URL`: Conexión a MongoDB (ej. `mongodb://admin:pass@mongodb:27017`).
- `SECRET_KEY`: Clave para firmar los JWT.
- `EXITO_ENABLED / ALKOSTO_ENABLED`: Activan/Desactivan scrapers específicos.

---

## ▶️ Ejecución con Docker (Recomendado)

Levanta todo el stack (API, Worker, MongoDB 8.0, Redis 7.0):

```bash
docker compose up --build
```

- **API**: http://localhost:8000
- **Documentación Interactiva (Swagger)**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🛠️ Flujo de Uso (Endpoints)

### 1. Autenticación
- **POST** `/api/auth/register`: Crea un nuevo usuario.
- **POST** `/api/auth/login`: Obtiene el `access_token` (JWT).

### 2. Búsqueda (Requiere Token)
- **POST** `/api/search?product=televisor`: Encola búsqueda asíncrona. Retorna `job_id`.
- **GET** `/api/search/{job_id}`: Consulta resultados del scraping.

### 3. Usuario & Historial (Requiere Token)
- **GET** `/api/users/me/history?limit=10&skip=0`: Consulta tus búsquedas pasadas de forma paginada.

---

## 🛠️ Tecnologías

- **Python 3.13** + **uv**
- **FastAPI**: API Web de alto rendimiento.
- **MongoDB 8.0**: Almacenamiento NoSQL.
- **Celery & Redis**: Gestión de tareas distribuidas.
- **Playwright**: Scraping de SPAs modernas.
- **Jose / Passlib**: Seguridad JWT y hashing de contraseñas.

---

## 👤 Autores

**José Gomez**  
*Arquitecto / Backend Developer*

**Alejandro Ruiz**  
*Arquitecto / Backend Developer*