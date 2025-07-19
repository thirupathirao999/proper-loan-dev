from bson import ObjectId
from database import collection
from models import Item, ItemInDB

async def create_item(item: Item):
    result = await collection.insert_one(item.dict())
    return str(result.inserted_id)

async def get_item(item_id: str):
    item = await collection.find_one({"_id": ObjectId(item_id)})
    if item:
        item["_id"] = str(item["_id"]) 
        return ItemInDB(**item)
    return None

async def update_item(item_id: str, item: Item):
    await collection.update_one({"_id": ObjectId(item_id)}, {"$set": item.dict()})
    return await get_item(item_id)

async def delete_item(item_id: str):
    result = await collection.delete_one({"_id": ObjectId(item_id)})
    return result.deleted_count
