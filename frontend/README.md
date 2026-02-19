# 🖥️ Web Scraping Pro -- Frontend

Interfaz de usuario moderna, reactiva y optimizada para la comparación de precios en tiempo real. Construida con **Vue 3 (Composition API)** y **Tailwind CSS v4**.

---

## ✨ Características Principales

- **Dashboard de Búsqueda Inteligente**:
    - Consultas asíncronas con sistema de **Polling automático**.
    - Barra de búsqueda con soporte para teclas de acceso rápido.
    - Visualización de tarjetas de producto con badges de comercio.
- **Filtrado y Ordenamiento Avanzado (Lado Cliente)**:
    - Filtrado dinámico por **Comercio** (Éxito, Alkosto).
    - Selección por **Rango de Precios** (Mínimo / Máximo).
    - Ordenamiento por precio (**Menor a Mayor** y viceversa).
    - Normalización automática de caracteres para evitar errores en nombres acentuados.
- **Historial de Búsquedas Interactivo**:
    - Audit Trail completo de búsquedas pasadas.
    - **Navegación Histórica**: Pulsa en una búsqueda pasada para ver los resultados exactos en la vista principal.
    - **Previsualización Rápida**: Filtra y explora los productos del historial directamente desde la pestaña de historial sin cambiar de vista.
- **Seguridad**:
    - Sistema de autenticación con **JWT**.
    - Persistencia de sesión mediante **Pinia** y LocalStorage.
    - Middleware de protección de rutas (Guards).

---

## 🛠️ Stack Tecnológico

- **Vue 3**: Framework progresivo para interfaces de usuario.
- **Vite**: Herramienta de construcción rápida de siguiente generación.
- **Tailwind CSS v4**: Framework de utilidades CSS para un diseño ultra-rápido.
- **Pinia**: Almacén de estados oficial para Vue (Auth y Gestión de Búsquedas).
- **Vue Router**: Navegación SPA fluida.
- **Lucide Icons**: Set de iconos elegantes y ligeros.
- **Axios**: Cliente HTTP para comunicación con la API.

---

## 🚀 Desarrollo Local

Para correr el frontend fuera de Docker (requiere Node.js 18+):

### 1. Instalar dependencias
```bash
npm install
```

### 2. Iniciar servidor de desarrollo
```bash
npm run dev
```
La aplicación estará disponible en [http://localhost:5173](http://localhost:5173).

---

## 📁 Estructura del Proyecto

```text
src/
├── api/                # Cliente Axios y servicios de API
├── modules/            # Módulos funcionales (Auth, Search)
│   └── search/         # Vistas: SearchView.vue, HistoryView.vue
├── stores/             # Gestión de estados (auth.js, search.js)
├── components/         # Componentes comunes
├── router/             # Configuración de Vue Router
└── assets/             # Estilos globales y favicon
```

---

## 👤 Autores

**José Gomez**  
*Arquitecto / Backend Developer*

**Alejandro Ruiz**  
*Arquitecto / Backend Developer*

