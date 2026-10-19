"""Aplicación FastAPI de ejemplo: CRUD simple de items en memoria."""

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

#Importamos los modelos Pydantic desde el archivo schemas.py
from app.schemas import (
    ConsultaCodigoRequest,
    ConsultaCodigoResponse,
    AgregarComentarioRequest,
    AgregarComentarioResponse,
    ComentariosRequest,
    ComentariosResponse,
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
    LikeRequest,
    LikeResponse,
    ListaPlaylistRequest,
    ListaPlaylistResponse,
    MensajesChatRequest,
    MensajesChatResponse,
    PedirCancionRequest,
    PedirCancionResponse,
    PublicacionResponse,
    RegistrarTokenRequest,
    RegistrarTokenResponse,
    RankingRequest,
    RankingResponse,
    RespuestaTriviaRequest,
    RespuestaTriviaResponse,
    SelfieResponse,
    TriviasRequest,
    TriviasResponse,
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
trivia_answers_db: set[tuple[int, int]] = set()

comments_db: dict[int, list[dict[str, int | str]]] = {
    1: [
        {
            "comment": "Excelente publicación.",
            "commentRegistrationDate": "2026-01-01",
            "commentStatus": 1,
            "idComment": 1,
            "idUserComment": 1,
            "userComment": "Usuario De Prueba",
            "avatar": "",
        }
    ]
}
next_comment_id = 2
likes_db: dict[int, set[int]] = {}
trivias_db: list[dict[str, object]] = [
    {
        "idEvent": 1,
        "idQuestion": 1,
        "question": "¿Cuál es la capital de Francia?",
        "questionAlternative": [
            {
                "alternativeAnswer": True,
                "alternativeDescription": "París",
                "idAlternative": 1,
            },
            {
                "alternativeAnswer": False,
                "alternativeDescription": "Madrid",
                "idAlternative": 2,
            },
        ],
        "questionImage": "",
        "questionName": "Capitales del mundo",
        "questionScore": 10,
        "questionStatus": 1,
        "questionType": "single",
    }
]
chat_messages_db: list[dict[str, int | str]] = [
    {
        "idMessage": 1,
        "idEvent": 1,
        "idUserMessage": 1,
        "messageRegistrationDate": "2026-01-01T10:00:00",
        "messageText": "Bienvenidos al evento.",
        "userImage": "",
        "userMessage": "Usuario De Prueba",
    }
]
playlist_db: list[dict[str, int | str | bool]] = [
    {
        "idPlaylist": 1,
        "idEvent": 1,
        "playlistBand": "Banda de prueba",
        "playlistRegistrationDate": "2026-01-01",
        "playlistSong": "Canción de prueba",
        "playlistStatus": True,
    }
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


# SERVICIO DE TRIVIAS
@app.post(
    "/trivias.php",
    response_model=TriviasResponse,
    tags=["trivias"],
)
def trivias(request: TriviasRequest) -> TriviasResponse:
    """Devuelve las preguntas de trivia de un evento filtradas por estado."""

    if events_db.get(request.idEvent) is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Evento no encontrado",
                "message": "El evento solicitado no existe",
            },
        )

    if users_db.get(request.idUserSession) is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Usuario no encontrado",
                "message": "El usuario de sesión no existe",
            },
        )

    questions = [
        question
        for question in trivias_db
        if question["idEvent"] == request.idEvent
        and question["questionStatus"] == request.questionStatus
    ]

    return TriviasResponse(
        data={"question": questions},
        message="Trivias consultadas correctamente",
    )


@app.post(
    "/respuesta_trivia.php",
    response_model=RespuestaTriviaResponse,
    tags=["trivias"],
)
def respuesta_trivia(
    request: RespuestaTriviaRequest,
) -> RespuestaTriviaResponse:
    """Registra una respuesta y actualiza el puntaje total del usuario."""

    user = users_db.get(request.idUserSession)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Usuario no encontrado",
                "message": "El usuario de sesión no existe",
            },
        )

    selected_question = next(
        (
            question
            for question in trivias_db
            if any(
                alternative["idAlternative"] == request.idAlternative
                for alternative in question["questionAlternative"]
            )
        ),
        None,
    )
    if selected_question is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Alternativa no encontrada",
                "message": "La alternativa solicitada no existe",
            },
        )

    question_id = selected_question["idQuestion"]
    answer_key = (request.idUserSession, question_id)
    if answer_key not in trivia_answers_db:
        selected_alternative = next(
            alternative
            for alternative in selected_question["questionAlternative"]
            if alternative["idAlternative"] == request.idAlternative
        )
        if selected_alternative["alternativeAnswer"]:
            user["userTotalScore"] += selected_question["questionScore"]
        trivia_answers_db.add(answer_key)

    return RespuestaTriviaResponse(
        data={"userTotalScore": user["userTotalScore"]},
        message="Respuesta de trivia registrada correctamente",
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


# COMENTARIOS DE PUBLICACIÓN
@app.post(
    "/comentarios.php",
    response_model=ComentariosResponse,
    tags=["comentarios"],
)
def comentarios(request: ComentariosRequest) -> ComentariosResponse:
    """Devuelve los comentarios de una publicación."""

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

    return ComentariosResponse(
        data={"comments": comments_db.get(request.idPost, [])},
        message="Comentarios consultados correctamente",
    )


# MENSAJES DE CHAT
@app.post(
    "/mensajes_chat.php",
    response_model=MensajesChatResponse,
    tags=["mensajes_chat"],
)
def mensajes_chat(request: MensajesChatRequest) -> MensajesChatResponse:
    """Devuelve los mensajes del chat de un evento."""

    if users_db.get(request.idUser) is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Usuario no encontrado",
                "message": "El usuario de sesión no existe",
            },
        )

    if events_db.get(request.idEvent) is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Evento no encontrado",
                "message": "El evento solicitado no existe",
            },
        )

    messages = [
        message
        for message in chat_messages_db
        if message["idEvent"] == request.idEvent
    ]

    return MensajesChatResponse(
        data={"messages": messages},
        message="Mensajes de chat consultados correctamente",
    )


# RANKING DE USUARIOS
@app.post(
    "/ranking.php",
    response_model=RankingResponse,
    tags=["ranking"],
)
def ranking(request: RankingRequest) -> RankingResponse:
    """Devuelve el ranking de puntajes de los usuarios de un evento."""

    user = users_db.get(request.idUser)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Usuario no encontrado",
                "message": "El usuario de sesión no existe",
            },
        )

    if events_db.get(request.idEvent) is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Evento no encontrado",
                "message": "El evento solicitado no existe",
            },
        )

    event_users = sorted(
        (
            event_user
            for event_user in users_db.values()
            if event_user["idEvent"] == request.idEvent
        ),
        key=lambda event_user: (-event_user["userTotalScore"], event_user["idUser"]),
    )
    ranking_users = [
        {
            "idUserRanking": event_user["idUser"],
            "userRankingLogo": event_user["avatar"],
            "userRankingName": (
                f"{event_user['userName']} {event_user['userLastName']}"
            ).strip(),
            "userRankingPosition": position,
            "userRankingTotalScore": event_user["userTotalScore"],
        }
        for position, event_user in enumerate(event_users, start=1)
    ]

    return RankingResponse(
        data={
            "raking": ranking_users,
            "userTotalScore": str(user["userTotalScore"]),
        },
        message="Ranking consultado correctamente",
    )


# LISTA DE PLAYLIST
@app.post(
    "/lista_playlist.php",
    response_model=ListaPlaylistResponse,
    tags=["lista_playlist"],
)
def lista_playlist(request: ListaPlaylistRequest) -> ListaPlaylistResponse:
    """Devuelve las canciones de la playlist de un evento."""

    if events_db.get(request.idEvent) is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Evento no encontrado",
                "message": "El evento solicitado no existe",
            },
        )

    search = request.search.strip().casefold()
    playlist = [
        song
        for song in playlist_db
        if song["idEvent"] == request.idEvent
        and (
            not search
            or search in str(song["playlistBand"]).casefold()
            or search in str(song["playlistSong"]).casefold()
        )
    ]

    return ListaPlaylistResponse(
        data={"playlist": playlist},
        message="Playlist consultada correctamente",
    )


# PEDIR CANCION
@app.post(
    "/pedir_cancion.php",
    response_model=PedirCancionResponse,
    tags=["pedir_cancion"],
)
def pedir_cancion(request: PedirCancionRequest) -> PedirCancionResponse:
    """Solicita una canción de la playlist."""

    if users_db.get(request.idUser) is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Usuario no encontrado",
                "message": "El usuario solicitante no existe",
            },
        )

    song = next(
        (
            playlist_song
            for playlist_song in playlist_db
            if playlist_song["idPlaylist"] == request.idPlaylist
        ),
        None,
    )
    if song is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": 404,
                "title": "Canción no encontrada",
                "message": "La canción solicitada no existe",
            },
        )

    return PedirCancionResponse(
        data=song,
        message="Canción solicitada correctamente",
    )


# AGREGAR COMENTARIO A PUBLICACIÓN
@app.post(
    "/agregar_comentarios.php",
    response_model=AgregarComentarioResponse,
    tags=["comentarios"],
)
def agregar_comentario(
    request: AgregarComentarioRequest,
) -> AgregarComentarioResponse:
    """Agrega un comentario a una publicación."""
    global next_comment_id

    if not request.comment.strip():
        raise HTTPException(
            status_code=400,
            detail={
                "code": 400,
                "title": "Comentario inválido",
                "message": "El comentario es obligatorio",
            },
        )

    user = users_db.get(request.idUserComment)
    if user is None:
        raise HTTPException(
            status_code=400,
            detail={
                "code": 400,
                "title": "Usuario inválido",
                "message": "El usuario del comentario no existe",
            },
        )

    post = next(
        (post for post in gallery_posts_db if post["idPost"] == request.idPost),
        None,
    )
    if post is None:
        raise HTTPException(
            status_code=400,
            detail={
                "code": 400,
                "title": "Publicación inválida",
                "message": "La publicación solicitada no existe",
            },
        )

    new_comment = {
        "comment": request.comment.strip(),
        "commentRegistrationDate": "2026-01-01",
        "commentStatus": 1,
        "idComment": next_comment_id,
        "idUserComment": request.idUserComment,
        "userComment": (
            f"{user['userName']} {user['userLastName']} {user['userSurName']}"
        ).strip(),
        "avatar": user["avatar"],
    }
    comments_db.setdefault(request.idPost, []).append(new_comment)
    next_comment_id += 1

    return AgregarComentarioResponse(
        data={"comment": new_comment},
        message="Comentario agregado correctamente",
    )


# LIKE DE PUBLICACIÓN
@app.post(
    "/likes.php",
    response_model=LikeResponse,
    tags=["likes"],
)
def like_publicacion(request: LikeRequest) -> LikeResponse:
    """Agrega o quita el like de un usuario en una publicación."""

    if users_db.get(request.idUserSesion) is None:
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

    post_likes = likes_db.setdefault(request.idPost, set())
    if request.idUserSesion in post_likes:
        post_likes.remove(request.idUserSesion)
        user_likes = 0
        message = "Like eliminado correctamente"
    else:
        post_likes.add(request.idUserSesion)
        user_likes = 1
        message = "Like agregado correctamente"

    post["postLikeCount"] = len(post_likes)
    post["postLike"] = bool(post_likes)

    return LikeResponse(
        data={"userLikes": user_likes},
        message=message,
    )
