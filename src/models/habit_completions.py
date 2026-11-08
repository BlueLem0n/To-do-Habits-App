from datetime import date, datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from models.habits import HabitModel


class HabitCompletionModel(Base):
    __tablename__ = "habit_completions"
    __table_args__ = (UniqueConstraint("habit_id", "completed_on", name="uq_habit_completion_day"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    completed_on: Mapped[date] = mapped_column(nullable=False)
    completed_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id", ondelete="CASCADE"), nullable=False)
    habit: Mapped["HabitModel"] = relationship(back_populates="completions")