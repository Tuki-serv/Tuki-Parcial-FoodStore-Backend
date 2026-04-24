# Tuki-FoodStore API 🚀

Este es el núcleo de procesamiento de la plataforma **Tuki-FoodStore**, una API REST profesional desarrollada con **FastAPI** y **SQLModel**. El proyecto implementa una arquitectura modular diseñada para gestionar relaciones complejas entre productos, categorías e ingredientes, garantizando la integridad de los datos y un alto rendimiento en las consultas.

## 🛠️ Tecnologías Utilizadas

* **Framework:** FastAPI (Python 3.10+).
* **ORM:** SQLModel (basado en SQLAlchemy y Pydantic).
* **Base de Datos:** PostgreSQL (v15+).
* **Gestión de Transacciones:** Implementación de los patrones **Unit of Work** y **Repository**.
* **Contenerización:** Docker y Docker Compose para el entorno de base de datos.

## 📂 Estructura del Proyecto

El código está organizado siguiendo una estructura modular por dominios:
* `app/core/`: Configuración global, conexión a base de datos y clases base del repositorio.
* `app/modules/`: Lógica de negocio dividida en módulos: `categoria`, `producto`, `ingrediente` y tablas intermedias para relaciones N:M.
* `app/utils/`: Manejadores globales de errores y excepciones personalizadas.

## 🌟 Características Principales

* **Relaciones N:M:** Gestión avanzada de productos con múltiples categorías e ingredientes, incluyendo lógica de "Categoría Principal" y "Ingrediente Alérgeno".
* **Carga Eficiente:** Uso de `selectinload` para evitar el problema de N+1 queries al traer datos relacionados.
* **Borrado Lógico:** Implementación de `deleted_at` para preservar la integridad referencial.
* **Paginación:** Endpoints optimizados con `offset` y `limit` mediante `Annotated` y `Query`.

## 🚀 Instalación y Uso

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/FoodStore-Backend.git](https://github.com/tu-usuario/FoodStore-Backend.git)
    ```
2.  **Configurar variables de entorno:** Crear un archivo `.env` basado en `Variables de entorno.md`.
3.  **Iniciar base de datos:**
    ```bash
    docker-compose up -d
    ```
4.  **Instalar dependencias e iniciar:**
    ```bash
    pip install -r requirements.txt
    fastapi dev main.py
    ```
5.  **Cargar datos de prueba:**
    ```bash
    python seed.py
    ```