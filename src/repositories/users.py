from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.users import UserModel

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> UserModel:
        result = await self.db.execute(select(UserModel).where(UserModel.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> UserModel:
        return await self.db.get(UserModel, user_id)

    async def add(self, user: UserModel) -> UserModel:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user