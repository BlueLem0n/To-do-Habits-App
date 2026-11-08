from datetime import date
from core.exceptions import CompletionAlreadyExistsError, CompletionNotFoundError
from models.habit_completions import HabitCompletionModel
from models.users import UserModel
from repositories.habit_completions import HabitCompletionRepository
from services.habits import HabitService


class HabitCompletionService:
    def __init__(self, repo: HabitCompletionRepository, habit_service: HabitService):
        self.repo = repo
        self.habit_service = habit_service

    async def create(self, user: UserModel, habit_id: int, completed_on: date) -> HabitCompletionModel:
        # Бросит HabitNotFoundError если привычка не найдена или чужая
        await self.habit_service.get_owned(user, habit_id)

        # Быстрая проверка окончательную гарантию даёт UniqueConstraint в БД
        if await self.repo.get_by_habit_and_date(habit_id, completed_on) is not None:
            raise CompletionAlreadyExistsError()

        completion = HabitCompletionModel(habit_id=habit_id, completed_on=completed_on)
        return await self.repo.add(completion)

    async def list_for_habit(self, user: UserModel, habit_id: int) -> list[HabitCompletionModel]:
        await self.habit_service.get_owned(user, habit_id)
        return await self.repo.list_by_habit(habit_id)

    async def delete(self, user: UserModel, habit_id: int, completion_id: int) -> None:
        await self.habit_service.get_owned(user, habit_id)
        completion = await self.repo.get_by_id(completion_id)
        # Отметка должна принадлежать именно этой привычке
        if completion is None or completion.habit_id != habit_id:
            raise CompletionNotFoundError()

        await self.repo.delete(completion)