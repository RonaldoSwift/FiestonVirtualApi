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
