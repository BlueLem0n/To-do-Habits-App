from typing import TYPE_CHECKING

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.roles import UserRoles

from db.base import Base

if TYPE_CHECKING:
    from models.tasks import TaskModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRoles] = mapped_column(Enum(UserRoles, native_enum=False), default=UserRoles.User, nullable=False)

    tasks: Mapped[list["TaskModel"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )