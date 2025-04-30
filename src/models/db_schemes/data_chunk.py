from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any, Dict
from bson import ObjectId
from models.enums import DataBaseEnum

class DataChunk(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    chunk_project_id: ObjectId
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: Dict[str, Any] = Field(default_factory=dict)
    chunk_order: int = Field(..., gt=0)
    chunk_asset_id: ObjectId
    
    @classmethod
    def get_indexes(cls):
        collection_name = DataBaseEnum.COLLECTION_CHUNK_NAME.value
        indexes = [
            {
                "key":[
                    ("chunk_project_id", 1)
                ],
                "name": "chunk_project_id_index_1",
                "unique": False
            }
        ]
        return collection_name, indexes


    class Config:
        arbitrary_types_allowed = True

