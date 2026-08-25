"""Aplicación FastAPI de ejemplo: CRUD simple de items en memoria."""

from fastapi import FastAPI, HTTPException

from app.schemas import ItemRequest, ItemResponse

app = FastAPI(
    title="FastAPI Hello World",
    description="Ejemplo simple de CRUD con FastAPI, Pydantic y Poetry.",
    version="0.1.0",
)

# "Base de datos" en memoria, solo para este ejemplo.
items_db: dict[int, ItemResponse] = {}
next_id = 1


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
