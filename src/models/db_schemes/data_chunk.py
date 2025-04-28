from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any, Dict
from bson import ObjectId

class DataChunk(BaseModel):
    _id: Optional[Any] = None
    chunk_project_id: Any
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: Dict[str, Any] = Field(default_factory=dict)
    chunk_order: int = Field(..., gt=0)
        

    @field_validator('_id', 'chunk_project_id')
    @classmethod
    def validate_object_ids(cls, v):
        if v is not None and not isinstance(v, ObjectId):
            raise ValueError('Must be a valid ObjectId')
        return v

    model_config = {
        "json_encoders": {
            ObjectId: str
        }
    }