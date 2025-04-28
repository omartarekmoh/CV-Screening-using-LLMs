from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from bson import ObjectId

class Project(BaseModel):
    _id: Optional[Any] = None
    project_id: str = Field(..., min_length=1)
        
    @field_validator('project_id')
    @classmethod
    def project_id_must_be_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Project id must be alphanumeric')
        return v

    @field_validator('_id')
    @classmethod
    def validate_object_id(cls, v):
        if v is not None and not isinstance(v, ObjectId):
            raise ValueError('_id must be a valid ObjectId')
        return v

    model_config = {
        "json_encoders": {
            ObjectId: str
        }
    }