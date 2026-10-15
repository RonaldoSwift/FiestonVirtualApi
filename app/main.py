"""Aplicación FastAPI de ejemplo: CRUD simple de items en memoria."""

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

#Importamos los modelos Pydantic desde el archivo schemas.py
from app.schemas import (
    ConsultaCodigoRequest,
    ConsultaCodigoResponse,
    DetalleEventoRequest,
    DetalleEventoResponse,
    DetallePublicacionRequest,
    DetallePublicacionResponse,
    DetalleUsuarioRequest,
    DetalleUsuarioResponse,
    GaleriaRequest,
    GaleriaResponse,
    ItemRequest,
    ItemResponse,
    PublicacionResponse,
    RegistrarTokenRequest,
    RegistrarTokenResponse,
    SelfieResponse,
)

app = FastAPI(
    title="FastAPI Hello World",
    description="Ejemplo simple de CRUD con FastAPI, Pydantic y Poetry.",
    version="0.1.0",
)

# "Base de datos" en memoria, solo para este ejemplo.
items_db: dict[int, ItemResponse] = {}
next_id = 1

#No es una base de datos real, solo un diccionario para simular la validación de códigos de invitación.
#Y que es un diccionario: guarda datos (llave -> valor) y en este caso la llave es el código de invitación y el valor es un diccionario con los datos del usuario y del evento.

invitation_codes_db = {
    123456: {
        "idUser": 1,
        "idEvent": 1,
    }
}

users_db = {
    1: {
        "idUser": 1,
        "idEvent": 1,
        "userName": "Usuario",
        "userLastName": "De Prueba",
        "userSurName": "",
        "userEmail": "usuario@example.com",
        "userPhone": "",
        "userCell": "",
        "userTotalScore": 0,
        "userStatus": 1,
        "avatar": "",
        "userLikesPhotos": 0,
        "userLikesVideos": 0,
        "userRanking": 0,
    }
}

events_db = {
    1: {
        "eventHost": "Organizador del evento",
        "eventImagePrize": "",
        "eventLogo": "",
        "eventName": "Evento de prueba",
        "eventPrize": "Premio del evento",
        "eventStartDate": "2026-01-01",
        "eventStatus": 1,
        "eventWelcomeText": "Bienvenido al evento.",
        "idEvent": 1,
    }
}

push_tokens_db: dict[int, str] = {}
selfie_posts_db: dict[int, dict[str, int | str]] = {}
next_post_id = 3
gallery_posts_db: list[dict[str, int | str]] = [
    {
        "idPost": 1,
        "idEvent": 1,
        "postFile": "https://picsum.photos/id/1015/800/600",
        "postTitle": "Publicación de prueba",
        "postLike": False,
        "postLikeCount": 0,
        "postStatus": 1,
        "postType": 1,
        "preview": "https://picsum.photos/id/1015/300/200",
    },
    {
        "idPost": 2,
        "idEvent": 1,
        "postFile": "https://picsum.photos/id/1016/800/600",
        "postTitle": "Segunda publicación de prueba",
        "postLike": False,
        "postLikeCount": 0,
        "postStatus": 1,
        "postType": 1,
        "preview": "https://picsum.photos/id/1016/300/200",
    },
]


@app.get("/", tags=["health"])
def read_root() -> dict[str, str]:
    """Endpoint de saludo para verificar que el servicio está corriendo."""
    return {"message": "Hello World"}


@app.post("/items", response_model=ItemResponse, status_code=201, tags=["items"])
def create_item(item: ItemRequest) -> ItemResponse:
    """Crea un nuevo item."""
    global next_id
    new_item = ItemResponse(id=next_id, **item.model_dump())
    items_db[next_id] = new_item
    next_id += 1
    return new_item


@app.get("/items", response_model=list[ItemResponse], tags=["items"])
def list_items() -> list[ItemResponse]:
    """Lista todos los items."""
    return list(items_db.values())


@app.get("/items/{item_id}", response_model=ItemResponse, tags=["items"])
def get_item(item_id: int) -> ItemResponse:
    """Obtiene un item por su id."""
    item = items_db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item


@app.put("/items/{item_id}", response_model=ItemResponse, tags=["items"])
def update_item(item_id: int, item: ItemRequest) -> ItemResponse:
    """Actualiza un item existente."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    updated_item = ItemResponse(id=item_id, **item.model_dump())
    items_db[item_id] = updated_item
    return updated_item


@app.delete("/items/{item_id}", status_code=204, tags=["items"])
def delete_item(item_id: int) -> None:
    """Elimina un item por su id."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    del items_db[item_id]

@app.post(
    "/consulta_codigo.php",
    response_model=ConsultaCodigoResponse,
    tags=["consulta_codigo"],
)

# Endpoint para validar un código de invitación del evento.
def consulta_codigo(request: ConsultaCodigoRequest) -> ConsultaCodigoResponse:
    """Valida el código de invitación del evento."""

    invitation = invitation_codes_db.get(request.userInvitationCode)

    if invitation is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Código de invitación no encontrado",
                "message": "El código de invitación no es válido",
            },
        )

    return ConsultaCodigoResponse(
        data={
            "user": {
                "idUser": invitation["idUser"],
            },
            "event": {
                "idEvent": invitation["idEvent"],
            },
        },
        message="Código de invitación válido",
    )

#DETALLE USUARIO
@app.post(
    "/detalle_usuario.php",
    response_model=DetalleUsuarioResponse,
    tags=["detalle_usuario"],
)
def detalle_usuario(request: DetalleUsuarioRequest) -> DetalleUsuarioResponse:
    """Devuelve los datos del usuario asociado al código de invitación."""

    user = users_db.get(request.idUser)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Usuario no encontrado",
                "message": "El usuario solicitado no existe",
            },
        )

    return DetalleUsuarioResponse(
        message="Usuario encontrado",
        data={"user": user},
    )


@app.post(
    "/registrar_tokens.php",
    response_model=RegistrarTokenResponse,
    tags=["registrar_tokens"],
)
def registrar_token(request: RegistrarTokenRequest) -> RegistrarTokenResponse:
    """Registra o actualiza el token FCM de un usuario."""
    if users_db.get(request.idUser) is None:
        raise HTTPException(
            status_code=400,
            detail={
                "code": 400,
                "title": "Usuario inválido",
                "message": "El usuario solicitado no existe",
            },
        )

    if not request.token.strip():
        raise HTTPException(
            status_code=400,
            detail={
                "code": 400,
                "title": "Token inválido",
                "message": "El token FCM es obligatorio",
            },
        )

    push_tokens_db[request.idUser] = request.token

    return RegistrarTokenResponse(
        data={"rpta": True},
        message="Token FCM registrado correctamente",
    )


@app.post(
    "/selfie.php",
    response_model=SelfieResponse,
    tags=["selfie"],
)
async def selfie(
    file: UploadFile = File(...),
    idUser: int = Form(...),
    postType: int = Form(...),
) -> SelfieResponse:
    """Registra la foto de perfil enviada por un usuario."""
    global next_post_id

    if users_db.get(idUser) is None:
        raise HTTPException(
            status_code=404,
            detail="El usuario solicitado no existe",
        )

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="El archivo de la foto de perfil es obligatorio",
        )

    post = {
        "idPost": next_post_id,
        "postFile": file.filename,
        "postType": postType,
    }
    selfie_posts_db[next_post_id] = post
    next_post_id += 1

    return SelfieResponse(
        data={"post": post},
        message="Foto de perfil subida correctamente",
    )


@app.post(
    "/publicaciones.php",
    response_model=PublicacionResponse,
    tags=["publicaciones"],
)
async def publicaciones(
    file: UploadFile = File(...),
    idUser: int = Form(...),
    idEvent: int = Form(...),
    postType: int = Form(...),
    postTitle: str = Form(...),
) -> PublicacionResponse:
    """Registra una foto o video en la galería del evento."""
    global next_post_id

    if users_db.get(idUser) is None:
        raise HTTPException(
            status_code=404,
            detail="El usuario solicitado no existe",
        )

    if events_db.get(idEvent) is None:
        raise HTTPException(
            status_code=404,
            detail="El evento solicitado no existe",
        )

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="El archivo de la publicación es obligatorio",
        )

    if not postTitle.strip():
        raise HTTPException(
            status_code=400,
            detail="El título de la publicación es obligatorio",
        )

    post = {
        "idPost": next_post_id,
        "idEvent": idEvent,
        "idUser": idUser,
        "postFile": file.filename,
        "postTitle": postTitle,
        "postLike": False,
        "postLikeCount": 0,
        "postStatus": 1,
        "postType": postType,
        "preview": file.filename,
    }
    gallery_posts_db.append(post)
    next_post_id += 1

    return PublicacionResponse(
        data={
            "post": {
                "idPost": post["idPost"],
                "postFile": post["postFile"],
                "postType": post["postType"],
            }
        },
        message="Publicación subida correctamente",
    )


@app.post(
    "/detalle_evento.php",
    response_model=DetalleEventoResponse,
    tags=["detalle_evento"],
)
def detalle_evento(request: DetalleEventoRequest) -> DetalleEventoResponse:
    """Devuelve el detalle de bienvenida del evento."""

    event = events_db.get(request.idEvent)
    if event is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Evento no encontrado",
                "message": "El evento solicitado no existe",
            },
        )

    return DetalleEventoResponse(
        message="Evento encontrado",
        data={"event": event},
    )

# SERVICIO_GALERIA
@app.post(
    "/galeria.php",
    response_model=GaleriaResponse,
    tags=["galeria"],
)
def galeria(request: GaleriaRequest) -> GaleriaResponse:
    """Devuelve las publicaciones de la galería filtradas por evento y estado."""

    event = events_db.get(request.idEvent)
    if event is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Evento no encontrado",
                "message": "El evento solicitado no existe",
            },
        )

    posts = [
        post
        for post in gallery_posts_db
        if post["idEvent"] == request.idEvent
        and post["postStatus"] == request.postStatus
    ]

    return GaleriaResponse(
        data={"posts": posts},
        message="Galería consultada correctamente",
    )

# DETALLE DE PUBLICACIÓN
@app.post(
    "/detalle_publicacion.php",
    response_model=DetallePublicacionResponse,
    tags=["detalle_publicacion"],
)
def detalle_publicacion(
    request: DetallePublicacionRequest,
) -> DetallePublicacionResponse:
    """Devuelve el detalle de una publicación para un usuario en sesión."""

    user = users_db.get(request.idUserSesion)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Usuario no encontrado",
                "message": "El usuario de sesión no existe",
            },
        )

    post = next(
        (post for post in gallery_posts_db if post["idPost"] == request.idPost),
        None,
    )
    if post is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Publicación no encontrada",
                "message": "La publicación solicitada no existe",
            },
        )

    return DetallePublicacionResponse(
        data={
            "user": {
                "userName": user["userName"],
                "userImage": user["avatar"],
            },
            "post": {
                "idPost": post["idPost"],
                "postFile": post["postFile"],
                "postLike": post["postLike"],
                "postLikeCount": post["postLikeCount"],
                "postStatus": post["postStatus"],
                "postTitle": post["postTitle"],
                "postType": post["postType"],
            },
        },
        message="Detalle de publicación consultado correctamente",
    )
