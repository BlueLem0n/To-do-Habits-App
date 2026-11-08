from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_current_user
from core.exceptions import (
    CompletionAlreadyExistsError,
    CompletionNotFoundError,
    HabitNotFoundError,
    )
from db.session import get_db
from models.users import UserModel
from repositories.habit_completions import HabitCompletionRepository
from repositories.habits import HabitRepository
from schemas.habit_completions import (
    HabitCompletionCreateSchema,
    HabitCompletionGetSchema,
    )
from services.habit_completions import HabitCompletionService
from services.habits import HabitService

router = APIRouter()


def get_completion_service(db: AsyncSession = Depends(get_db)) -> HabitCompletionService:
    return HabitCompletionService(
        HabitCompletionRepository(db),
        HabitService(HabitRepository(db)),
    )


@router.post(
    "/{habit_id}/completions",
    response_model=HabitCompletionGetSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_completion(
    habit_id: int,
    data: HabitCompletionCreateSchema,
    user: UserModel = Depends(get_current_user),
    service: HabitCompletionService = Depends(get_completion_service),):
    try:
        return await service.create(user, habit_id, data.completed_on)
    except HabitNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Привычка не найдена")
    except CompletionAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Отметка за этот день уже есть")


@router.get("/{habit_id}/completions", response_model=list[HabitCompletionGetSchema])
async def list_completions(
    habit_id: int,
    user: UserModel = Depends(get_current_user),
    service: HabitCompletionService = Depends(get_completion_service),):
    try:
        return await service.list_for_habit(user, habit_id)
    except HabitNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Привычка не найдена")


@router.delete("/{habit_id}/completions/{completion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_completion(
    habit_id: int,
    completion_id: int,
    user: UserModel = Depends(get_current_user),
    service: HabitCompletionService = Depends(get_completion_service),):
    try:
        await service.delete(user, habit_id, completion_id)
    except HabitNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Привычка не найдена")
    except CompletionNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Отметка не найдена")