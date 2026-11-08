from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import CompletionAlreadyExistsError
from models.habit_completions import HabitCompletionModel


class HabitCompletionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_habit(self, habit_id: int) -> list[HabitCompletionModel]:
        result = await self.db.execute(
            select(HabitCompletionModel)
            .where(HabitCompletionModel.habit_id == habit_id)
            .order_by(HabitCompletionModel.completed_on)
        )
        return list(result.scalars().all())

    async def get_by_id(self, completion_id: int) -> HabitCompletionModel | None:
        return await self.db.get(HabitCompletionModel, completion_id)

    async def get_by_habit_and_date(self, habit_id: int, completed_on: date) -> HabitCompletionModel | None:
        result = await self.db.execute(
            select(HabitCompletionModel).where(
                HabitCompletionModel.habit_id == habit_id,
                HabitCompletionModel.completed_on == completed_on,))
        return result.scalar_one_or_none()

    async def add(self, completion: HabitCompletionModel) -> HabitCompletionModel:
        self.db.add(completion)
        try:
            await self.db.commit()
        except IntegrityError:
            # Сработал UniqueConstraint: отметка за этот день уже есть
            # Откатываем сессию или её нельзя будет использовать дальше
            await self.db.rollback()
            raise CompletionAlreadyExistsError()
        await self.db.refresh(completion)
        return completion

    async def delete(self, completion: HabitCompletionModel) -> None:
        await self.db.delete(completion)
        await self.db.commit()