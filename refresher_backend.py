import os
import category_enums
from typing import Optional, List

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument


app = FastAPI(
    title="Itestra Office Refresher API",
    summary="A sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
)

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client["refresher_db"]
beverages_collection = db["beverages"]

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class BeverageBase(BaseModel):
    # This is the updated configuration for Pydantic v2
    model_config = ConfigDict(populate_by_name=True)

    name: str
    category: category_enums.BeverageCategory
    current_stock: int = Field(alias="currentStock", ge=0)
    threshold: int = Field(ge=0)
    unit: str
    icon: str

class BeverageCreate(BeverageBase):
    pass

class Beverage(BeverageBase):
    id: str
    # This model inherits the config from BeverageBase, so no extra config is needed.


# --- Corrected Snack Models ---

class SnackBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    category: category_enums.SnackCategory
    current_stock: int = Field(alias="currentStock", ge=0)
    threshold: int = Field(ge=0)
    unit: str
    icon: str

class SnackCreate(SnackBase):
    pass

class Snack(SnackBase):
    id: str


db_beverages: List[Beverage] = []

@app.post("/beverages/", response_model=Beverage, status_code=201)
async def create_beverage(beverage_in: BeverageCreate):
    beverage_data = beverage_in.model_dump()
    result = await beverages_collection.insert_one(beverage_data)
    created = await beverages_collection.find_one({"_id": result.inserted_id})
    return Beverage.model_validate({**created, "id": str(created["_id"])})

@app.get("/beverages/", response_model=List[Beverage])
async def get_all_beverages():
    beverages = []
    cursor = beverages_collection.find()
    async for doc in cursor:
        beverages.append(Beverage.model_validate({**doc, "id": str(doc["_id"])}))
    return beverages