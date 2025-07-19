from fastapi import FastAPI, HTTPException
from models import Item
import crud

app = FastAPI()

@app.post("/items/")
async def create(item: Item):
    item_id = await crud.create_item(item)
    return {"item_id": item_id}

@app.get("/items/{item_id}")
async def read(item_id: str):
    item = await crud.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}")
async def update(item_id: str, item: Item):
    updated = await crud.update_item(item_id, item)
    return updated

@app.delete("/items/{item_id}")
async def delete(item_id: str):
    deleted = await crud.delete_item(item_id)
    if deleted:
        return {"message": "Deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
