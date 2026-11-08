from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, field_serializer

from core.date_serializer import format_datetime


class HabitCompletionCreateSchema(BaseModel):
    completed_on: date


class HabitCompletionGetSchema(BaseModel):
    id: int
    habit_id: int
    completed_on: date
    completed_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer("completed_at")
    def serialize_completed_at(self, dt: datetime) -> str:
        return format_datetime(dt)