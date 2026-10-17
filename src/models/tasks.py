from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from models.users import UserModel


class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    priority: Mapped[int] = mapped_column(default=1)
    is_completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    due_date: Mapped[datetime | None] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    owner: Mapped["UserModel"] = relationship(back_populates="tasks")