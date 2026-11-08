from core.exceptions import HabitNotFoundError
from models.habits import HabitModel
from models.users import UserModel
from repositories.habits import HabitRepository
from schemas.habits import HabitCreateSchema, HabitUpdateSchema

class HabitService:
    def __init__(self, repo: HabitRepository):
        self.repo = repo

    async def create(self, user: UserModel, data: HabitCreateSchema) -> HabitModel:
        habit = HabitModel(
            title=data.title,
            description=data.description,
            user_id=user.id,
        )
        return await self.repo.add(habit)

    async def list_for_user(self, user: UserModel) -> list[HabitModel]:
        return await self.repo.list_by_user(user.id)

    async def get_owned(self, user: UserModel, habit_id: int) -> HabitModel:
        habit = await self.repo.get_by_id(habit_id)
        # чужая привычка и несуществующая дают одинаковую ошибку
        if habit is None or habit.user_id != user.id:
            raise HabitNotFoundError()
        return habit

    async def update(self, user: UserModel, habit_id: int, data: HabitUpdateSchema) -> HabitModel:
        habit = await self.get_owned(user, habit_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(habit, key, value)
        return await self.repo.add(habit)

    async def delete(self, user: UserModel, habit_id: int) -> None:
        habit = await self.get_owned(user, habit_id)
        await self.repo.delete(habit)