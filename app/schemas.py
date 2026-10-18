"""Modelos Pydantic para las peticiones (request) y respuestas (response) de la API."""

from pydantic import BaseModel, Field


class ItemRequest(BaseModel):
    """Datos que el cliente envía para crear o actualizar un item."""

    name: str = Field(..., min_length=1, examples=["Manzana"])
    description: str | None = Field(default=None, examples=["Fruta roja y jugosa"])
    price: float = Field(..., gt=0, examples=[1.5])


class ItemResponse(BaseModel):
    """Datos que la API devuelve al cliente al representar un item."""

    id: int
    name: str
    description: str | None = None
    price: float


class ConsultaCodigoRequest(BaseModel):
    """Datos que el cliente envía para validar un código de invitación."""
    userInvitationCode: int = Field(..., examples=[123456])


class ConsultaCodigoUser(BaseModel):
    """Información del usuario asociado al código de invitación."""
    idUser: int


class ConsultaCodigoEvent(BaseModel):
    """Información del evento asociado al código de invitación."""
    idEvent: int


class ConsultaCodigoData(BaseModel):
    """Datos devueltos cuando el código de invitación es válido."""
    user: ConsultaCodigoUser
    event: ConsultaCodigoEvent


class ConsultaCodigoResponse(BaseModel):
    """Respuesta exitosa de la consulta del código de invitación."""
    data: ConsultaCodigoData
    message: str

#DETALLE DE USUARI

class DetalleUsuarioRequest(BaseModel):
    """Datos que el cliente envía para consultar un usuario."""
    idUser: int = Field(..., examples=[1])


class DetalleUsuarioData(BaseModel):
    """Información del usuario devuelta por la API."""
    idUser: int
    idEvent: int
    userName: str
    userLastName: str
    userSurName: str
    userEmail: str
    userPhone: str
    userCell: str
    userTotalScore: int
    userStatus: int
    avatar: str
    userLikesPhotos: int
    userLikesVideos: int
    userRanking: int


class DetalleUsuarioResponseData(BaseModel):
    """Contenedor de la información del usuario."""
    user: DetalleUsuarioData


class DetalleUsuarioResponse(BaseModel):
    """Respuesta exitosa de la consulta de usuario."""
    message: str
    data: DetalleUsuarioResponseData


class SelfiePost(BaseModel):
    """Datos de la foto de perfil subida."""
    idPost: int
    postFile: str
    postType: int


class SelfieResponseData(BaseModel):
    """Contenedor de la publicación creada."""
    post: SelfiePost


class SelfieResponse(BaseModel):
    """Respuesta exitosa de la subida de foto de perfil."""
    data: SelfieResponseData
    message: str

# PUBLICACIÓN
class PublicacionPost(BaseModel):
    """Datos de la publicación creada."""
    idPost: int
    postFile: str
    postType: int


class PublicacionResponseData(BaseModel):
    """Contenedor de la publicación creada."""
    post: PublicacionPost


class PublicacionResponse(BaseModel):
    """Respuesta exitosa de la subida de una publicación."""
    data: PublicacionResponseData
    message: str


# DETALLE DE EVENTO
class DetalleEventoRequest(BaseModel):
    """Datos que el cliente envía para consultar un evento."""
    idEvent: int = Field(..., examples=[1])


class DetalleEventoEvent(BaseModel):
    """Información de bienvenida del evento."""
    eventHost: str
    eventImagePrize: str
    eventLogo: str
    eventName: str
    eventPrize: str
    eventStartDate: str
    eventStatus: int
    eventWelcomeText: str
    idEvent: int


class DetalleEventoResponseData(BaseModel):
    """Contenedor del detalle del evento."""
    event: DetalleEventoEvent


class DetalleEventoResponse(BaseModel):
    """Respuesta exitosa del detalle del evento."""
    data: DetalleEventoResponseData
    message: str


#REGISTRAR TOKENS
class RegistrarTokenRequest(BaseModel):
    """Datos que el cliente envía para registrar su token FCM."""
    idUser: int = Field(..., examples=[1])
    token: str = Field(..., examples=["token-fcm-del-dispositivo"])


class RegistrarTokenResponseData(BaseModel):
    """Resultado del registro del token FCM."""
    rpta: bool


class RegistrarTokenResponse(BaseModel):
    """Respuesta exitosa del registro del token FCM."""
    data: RegistrarTokenResponseData
    message: str


#SERVICIO_GALERIA
class GaleriaRequest(BaseModel):
    """Filtros para consultar la galería de un evento."""
    idEvent: int = Field(..., examples=[1])
    postStatus: int = Field(..., examples=[1])


class GaleriaPost(BaseModel):
    """Publicación disponible en la galería."""
    idPost: int
    postFile: str
    postStatus: int
    postType: int
    preview: str


class GaleriaResponseData(BaseModel):
    """Contenedor de las publicaciones de la galería."""
    posts: list[GaleriaPost]


class GaleriaResponse(BaseModel):
    """Respuesta exitosa de la consulta de galería."""
    data: GaleriaResponseData
    message: str

# DETALLE DE PUBLICACIÓN

class DetallePublicacionRequest(BaseModel):
    """Datos para consultar el detalle de una publicación."""
    idUserSesion: int = Field(..., examples=[1])
    idPost: int = Field(..., examples=[1])


class DetallePublicacionUser(BaseModel):
    """Información del autor de la publicación."""
    userName: str
    userImage: str


class DetallePublicacionPost(BaseModel):
    """Información detallada de una publicación."""
    idPost: int
    postFile: str
    postLike: bool
    postLikeCount: int
    postStatus: int
    postTitle: str
    postType: int


class DetallePublicacionResponseData(BaseModel):
    """Datos del usuario y de la publicación."""
    user: DetallePublicacionUser
    post: DetallePublicacionPost


class DetallePublicacionResponse(BaseModel):
    """Respuesta del servicio de detalle de publicación."""
    data: DetallePublicacionResponseData
    message: str


# COMENTARIOS DE PUBLICACIÓN

class ComentariosRequest(BaseModel):
    """Datos para consultar los comentarios de una publicación."""
    idPost: int = Field(..., examples=[1])


class Comentario(BaseModel):
    """Comentario publicado en una publicación."""
    comment: str
    commentRegistrationDate: str
    commentStatus: int
    idComment: int
    idUserComment: int
    userComment: str
    avatar: str


class ComentariosResponseData(BaseModel):
    """Contenedor de los comentarios de una publicación."""
    comments: list[Comentario]


class ComentariosResponse(BaseModel):
    """Respuesta del listado de comentarios."""
    data: ComentariosResponseData
    message: str

# AGREGAR COMENTARIO A PUBLICACIÓN
class AgregarComentarioRequest(BaseModel):
    """Datos para agregar un comentario a una publicación."""
    idPost: int = Field(..., examples=[1])
    idUserComment: int = Field(..., examples=[1])
    comment: str = Field(..., examples=["Excelente publicación."])


class AgregarComentarioResponseData(BaseModel):
    """Contenedor del comentario agregado."""
    comment: Comentario


class AgregarComentarioResponse(BaseModel):
    """Respuesta del servicio para agregar comentarios."""
    data: AgregarComentarioResponseData
    message: str


# LIKE DE PUBLICACIÓN
class LikeRequest(BaseModel):
    """Datos para agregar o quitar un like de una publicación."""
    idUserSesion: int = Field(..., examples=[1])
    idPost: int = Field(..., examples=[1])


class LikeResponseData(BaseModel):
    """Resultado del like del usuario."""
    userLikes: int


class LikeResponse(BaseModel):
    """Respuesta del servicio para agregar o quitar likes."""
    data: LikeResponseData
    message: str


# TRIVIAS
class TriviasRequest(BaseModel):
    """Filtros para consultar las preguntas de trivia de un evento."""
    idEvent: int = Field(..., examples=[1])
    questionStatus: int = Field(..., examples=[1])
    idUserSession: int = Field(..., examples=[1])


class TriviaAlternative(BaseModel):
    """Alternativa de respuesta de una pregunta."""
    alternativeAnswer: bool
    alternativeDescription: str
    idAlternative: int


class TriviaQuestion(BaseModel):
    """Pregunta de trivia disponible para el evento."""
    idQuestion: int
    question: str
    questionAlternative: list[TriviaAlternative]
    questionImage: str
    questionName: str
    questionScore: int
    questionStatus: int
    questionType: str


class TriviasResponseData(BaseModel):
    """Contenedor de las preguntas de trivia."""
    question: list[TriviaQuestion]


class TriviasResponse(BaseModel):
    """Respuesta del listado de preguntas de trivia."""
    data: TriviasResponseData
    message: str


# RESPUESTA DE TRIVIA
class RespuestaTriviaRequest(BaseModel):
    """Datos para registrar la respuesta de una trivia."""
    idAlternative: int = Field(..., examples=[1])
    idUserSession: int = Field(..., examples=[1])


class RespuestaTriviaResponseData(BaseModel):
    """Puntaje total actualizado del usuario."""
    userTotalScore: int


class RespuestaTriviaResponse(BaseModel):
    """Respuesta del registro de una respuesta de trivia."""
    data: RespuestaTriviaResponseData
    message: str


# MENSAJES DE CHAT
class MensajesChatRequest(BaseModel):
    """Datos para consultar los mensajes de chat de un evento."""
    idUser: int = Field(..., examples=[1])
    idEvent: int = Field(..., examples=[1])


class MensajeChat(BaseModel):
    """Mensaje publicado en el chat del evento."""
    idMessage: int
    idUserMessage: int
    messageRegistrationDate: str
    messageText: str
    userImage: str
    userMessage: str


class MensajesChatResponseData(BaseModel):
    """Contenedor de los mensajes del chat."""
    messages: list[MensajeChat]


class MensajesChatResponse(BaseModel):
    """Respuesta del listado de mensajes de chat."""
    data: MensajesChatResponseData
    message: str


# RANKING DE USUARIOS
class RankingRequest(BaseModel):
    """Datos para consultar el ranking de usuarios de un evento."""
    idUser: int = Field(..., examples=[1])
    idEvent: int = Field(..., examples=[1])


class RankingUser(BaseModel):
    """Usuario incluido en el ranking del evento."""
    idUserRanking: int
    userRankingLogo: str
    userRankingName: str
    userRankingPosition: int
    userRankingTotalScore: int


class RankingResponseData(BaseModel):
    """Ranking y puntaje del usuario de sesión."""
    raking: list[RankingUser]
    userTotalScore: str


class RankingResponse(BaseModel):
    """Respuesta del ranking de usuarios."""
    data: RankingResponseData
    message: str


# LISTA DE PLAYLIST
class ListaPlaylistRequest(BaseModel):
    """Filtros para consultar las canciones de la playlist de un evento."""
    idEvent: int = Field(..., examples=[1])
    search: str = Field(default="", examples=["canción"])


class PlaylistSong(BaseModel):
    """Canción disponible en la playlist del evento."""
    idPlaylist: int
    playlistBand: str
    playlistRegistrationDate: str
    playlistSong: str
    playlistStatus: bool


class ListaPlaylistResponseData(BaseModel):
    """Contenedor de las canciones de la playlist."""
    playlist: list[PlaylistSong]


class ListaPlaylistResponse(BaseModel):
    """Respuesta del listado de playlist."""
    data: ListaPlaylistResponseData
    message: str
