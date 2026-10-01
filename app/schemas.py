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

#DETALLE DE USUARIO 

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