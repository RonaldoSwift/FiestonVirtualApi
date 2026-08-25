# FastAPI Hello World

Proyecto simple de ejemplo con [FastAPI](https://fastapi.tiangolo.com/), que implementa un CRUD de "items" en memoria usando modelos de request/response con Pydantic. Gestionado con [Poetry](https://python-poetry.org/).

## Requisitos

- Python 3.11 o superior
- [Poetry](https://python-poetry.org/docs/#installation) instalado

## Instalación

```bash
poetry install
```

## Ejecutar el servicio

```bash
poetry run uvicorn app.main:app --reload
```

El servicio quedará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000).

Documentación interactiva (Swagger UI): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Ejecutar desde VS Code

Este proyecto incluye una configuración en `.vscode/launch.json`. Solo abre el panel "Run and Debug" (⇧⌘D), selecciona **"Python Debugger: FastAPI"** y presiona ▶️.

> Asegúrate de que VS Code esté usando el intérprete de Python del entorno virtual creado por Poetry (`Python: Select Interpreter`).

## Endpoints

| Método | Ruta            | Descripción                  |
| ------ | --------------- | ----------------------------- |
| GET    | `/`             | Mensaje de saludo (health)    |
| POST   | `/items`        | Crear un item                 |
| GET    | `/items`        | Listar todos los items        |
| GET    | `/items/{id}`   | Obtener un item por id        |
| PUT    | `/items/{id}`   | Actualizar un item por id     |
| DELETE | `/items/{id}`   | Eliminar un item por id       |

### Ejemplo de request para crear un item

```json
{
  "name": "Manzana",
  "description": "Fruta roja y jugosa",
  "price": 1.5
}
```
