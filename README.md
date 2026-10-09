# FastAPI Hello World

Proyecto simple de ejemplo con [FastAPI](https://fastapi.tiangolo.com/), que implementa un CRUD de "items" en memoria usando modelos de request/response con Pydantic. Gestionado con [Poetry](https://python-poetry.org/).

## Requisitos

- Python 3.11 o superior
- [Poetry](https://python-poetry.org/docs/#installation) instalado

### Instalar los requisitos en macOS (con Homebrew)

Si no tienes [Homebrew](https://brew.sh/) instalado:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Instalar Python y Poetry:

```bash
brew install python@3.11
brew install poetry
```

Verifica las versiones instaladas:

```bash
python3 --version
poetry --version
```

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

Este proyecto incluye una configuración en `.vscode/launch.json`. Sigue estos pasos:

1. Ejecuta `poetry install` al menos una vez (ver arriba) para crear el entorno virtual.
2. Abre la paleta de comandos (⇧⌘P) y ejecuta **"Python: Select Interpreter"**.
3. Elige el intérprete que apunte al entorno virtual de este proyecto (algo como `fastapi-hello-world-XXXX-py3.XX`). Si no aparece en la lista, ejecuta `poetry env info` en la terminal para obtener la ruta y selecciónala con **"Enter interpreter path..."**.
4. Abre el panel "Run and Debug" (⇧⌘D), selecciona **"Python Debugger: FastAPI"** y presiona ▶️.

> Este paso solo se necesita hacer una vez por proyecto (o si borras/recreas el entorno virtual). VS Code recuerda el intérprete seleccionado.

## Endpoints

| Método | Ruta            | Descripción                  |
| ------ | --------------- | ----------------------------- |
| GET    | `/`             | Mensaje de saludo (health)    |
| POST   | `/items`        | Crear un item                 |
| GET    | `/items`        | Listar todos los items        |
| GET    | `/items/{id}`   | Obtener un item por id        |
| PUT    | `/items/{id}`   | Actualizar un item por id     |
| DELETE | `/items/{id}`   | Eliminar un item por id       |
| POST   | `/consulta_codigo.php` | Validar un código de invitación |
| POST   | `/detalle_usuario.php` | Obtener el detalle de un usuario |
| POST   | `/selfie.php`           | Subir la foto de perfil de un usuario |
| POST   | `/detalle_evento.php`  | Obtener el detalle de bienvenida de un evento |

### Ejemplo de request para consultar el detalle de un evento

```json
{
  "idEvent": 1
}
```

### Ejemplo de request para crear un item

```json
{
  "name": "Manzana",
  "description": "Fruta roja y jugosa",
  "price": 1.5
}
```
