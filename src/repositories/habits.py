from sqlalchemy.ext.asyncio import AsyncSession
from models.habits import HabitModel
from sqlalchemy import select

class HabitRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_user(self, user_id: int) -> list[HabitModel]:
        result = await self.db.execute(select(HabitModel).where(HabitModel.user_id==user_id))
        return list(result.scalars().all())

    async def get_by_id(self, habit_id: int) -> HabitModel:
        return await self.db.get(HabitModel, habit_id)

    async def add(self, habit: HabitModel) -> HabitModel:
        self.db.add(habit)
        await self.db.commit()
        await self.db.refresh(habit)
        return habit

    async def delete(self, habit: HabitModel) -> None:
        await self.db.delete(habit)
        await self.db.commit()
    
        