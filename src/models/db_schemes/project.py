from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId
from models.enums import DataBaseEnum

class Project(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    project_id: str = Field(..., min_length=1)

    @field_validator('project_id')
    @classmethod
    def project_id_must_be_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Project id must be alphanumeric')
        return v

    @classmethod
    def get_indexes(cls):
        # Define collection name directly in the model
        collection_name = DataBaseEnum.COLLECTION_PROJECT_NAME.value
        indexes = [
            {
                "key": [
                    ("project_id", 1)
                ],
                "name": "project_id_index_1",
                "unique": True
            }
        ]
        return collection_name, indexes
        

    class Config:
        arbitrary_types_allowed = True