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
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

El servicio quedará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000).
La conexión Socket.IO usa `http://localhost.proxyman.io:8000/socket.io/`, con
los transportes `polling` y `websocket`.
El servidor acepta clientes que envían `EIO=4` y también completa `EIO=4`
cuando un cliente legado envía únicamente `transport=polling&b64=1`.
El upgrade de polling a WebSocket requiere que Proxyman conserve los headers
`Upgrade: websocket` y `Connection: Upgrade`; si el proxy no los reenvía, el
cliente puede configurarse temporalmente con `transports: ["polling"]`.

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
| POST   | `/registrar_tokens.php` | Registrar el token push FCM de un usuario |
| POST   | `/selfie.php`           | Subir la foto de perfil de un usuario |
| POST   | `/publicaciones.php`     | Subir una foto o video a la galería |
| POST   | `/detalle_evento.php`  | Obtener el detalle de bienvenida de un evento |
| POST   | `/galeria.php`          | Obtener la galería de fotos y videos de un evento |
| POST   | `/detalle_publicacion.php` | Obtener el detalle de una publicación |
| POST   | `/comentarios.php` | Obtener los comentarios de una publicación |
| POST   | `/agregar_comentarios.php` | Agregar un comentario a una publicación |
| POST   | `/likes.php` | Agregar o quitar un like de una publicación |
| POST   | `/trivias.php` | Obtener las preguntas de trivia de un evento |
| POST   | `/respuesta_trivia.php` | Registrar una respuesta de trivia y obtener el puntaje total |
| POST   | `/mensajes_chat.php` | Obtener los mensajes del chat de un evento |
| POST   | `/ranking.php` | Obtener el ranking de puntajes de un evento |
| POST   | `/lista_playlist.php` | Obtener la lista de canciones de la playlist de un evento |
| POST | `/agregar_playlist.php` | Agregar una canción a la playlist y devolver la lista actualizada |
| POST | `/pedir_cancion.php` | Solicitar una canción de la playlist |
| POST   | `/logout.php` | Cerrar sesión del usuario |

### Chat Socket.IO

El servidor acepta los eventos `join` y `message` en la ruta `/socket.io/`.
Los clientes que se unen al mismo evento comparten una sala con el formato
`event_<idEvent>`.

```javascript
socket.emit("join", 3);
socket.emit("message", "Hola");
socket.on("message", (message) => {
  console.log(message.messageText);
});
```

También se puede enviar `join` como un objeto para asociar los metadatos del
usuario al mensaje:

```javascript
socket.emit("join", {
  idEvent: 3,
  idUser: 1,
  userName: "Usuario",
  userImage: "",
});
```

### Ejemplo de request para consultar el detalle de un evento

```json
{
  "idEvent": 1
}
```

### Ejemplo de request para registrar un token push

```json
{
  "idUser": 1,
  "token": "token-fcm-del-dispositivo"
}
```

### Ejemplo de request para consultar la galería

```json
{
  "idEvent": 1,
  "postStatus": 1
}
```

### Ejemplo de request para consultar el detalle de una publicación

```json
{
  "idUserSesion": 1,
  "idPost": 1
}
```

### Ejemplo de request para consultar las trivias de un evento

```json
{
  "idEvent": 1,
  "questionStatus": 1,
  "idUserSession": 1
}
```

### Ejemplo de request para responder una trivia

```json
{
  "idAlternative": 1,
  "idUserSession": 1
}
```

### Ejemplo de request para consultar los mensajes del chat

```json
{
  "idUser": 1,
  "idEvent": 1
}
```

### Ejemplo de request para consultar el ranking

```json
{
  "idUser": 1,
  "idEvent": 1
}
```

### Ejemplo de request para consultar la playlist

```json
{
  "idEvent": 1,
  "search": "canción"
}
```

### Ejemplo de request para agregar una canción a la playlist

```json
{
  "idEvent": 1,
  "playlistBand": "Farruko",
  "playlistRegistrationDate": "2025-01-01",
  "playlistSong": "Pepas",
  "playlistStatus": true,
  "playListURL": "https://s3.amazonaws.com/kargopolov/kukushka.mp3"
}
```

### Ejemplo de request para pedir una canción

```json
{
  "idUser": 1,
  "idPlaylist": 1
}
```

### Ejemplo de request para cerrar sesión

```json
{
  "idUser": 1
}
```

### Ejemplo de request para consultar los comentarios de una publicación

```json
{
  "idPost": 1
}
```

### Ejemplo de request para agregar un comentario

```json
{
  "idPost": 1,
  "idUserComment": 1,
  "comment": "Excelente publicación."
}
```

### Ejemplo de request para agregar o quitar un like

```json
{
  "idUserSesion": 1,
  "idPost": 1
}
```

`/publicaciones.php` recibe los datos como `multipart/form-data`:

- `file`: archivo de la foto o video.
- `idUser`: identificador del usuario.
- `idEvent`: identificador del evento.
- `postType`: tipo de publicación.
- `postTitle`: título de la publicación.

### Usuarios de prueba para chat

Hay dos códigos de invitación activos para el mismo evento:

| Código | `idUser` | `idEvent` |
| ------ | -------- | --------- |
| `123456` | `1` | `1` |
| `654321` | `2` | `1` |

Valida cada código con `POST /consulta_codigo.php`. Ambos usuarios quedan
asociados al mismo `idEvent` y pueden consultar el mismo chat mediante
`POST /mensajes_chat.php`.

### Ejemplo de request para crear un item

```json
{
  "name": "Manzana",
  "description": "Fruta roja y jugosa",
  "price": 1.5
}
```
