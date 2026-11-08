from pydantic import BaseModel, Field, ConfigDict, field_serializer
from datetime import datetime
from typing import Optional
from core.date_serializer import format_datetime

class TaskCreateSchema(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    priority: int = Field(default=1, ge=1, le=4)
    due_date: Optional[datetime] = None

class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    priority: Optional[int] = Field(None,  ge=1, le=4) 
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None

class TaskGetSchema(TaskCreateSchema):
    id: int 
    is_completed: bool  
    created_at: datetime  

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("created_at", "due_date")
    def serialize_dates(self, dt: datetime | None) -> str | None:
        return format_datetime(dt)
    