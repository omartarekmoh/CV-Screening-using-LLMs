from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime, timezone
from models.enums import DataBaseEnum

class Asset(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    asset_project_id: ObjectId = Field(...)
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: int = Field(gt=0, default=None)
    asset_config: Optional[dict] = Field(default=None)
    asset_pushed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    @classmethod
    def get_indexes(cls):
        # Define collection name directly in the model
        collection_name = DataBaseEnum.COLLECTION_ASSET_NAME.value
        indexes = [
            {
                "key": [
                    ("asset_project_id", 1)
                ],
                "name": "asset_project_id_index_1",
                "unique": False
            },
            {
                "key": [
                    ("asset_project_id", 1),
                    ("asset_name", 1),
                ],
                "name": "asset_project_id_and_name_index_1",
                "unique": True
            }
        ]
        return collection_name, indexes
        

    class Config:
        arbitrary_types_allowed = True