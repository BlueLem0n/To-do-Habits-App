from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_current_user
from core.exceptions import HabitNotFoundError
from db.session import get_db
from models.users import UserModel
from repositories.habits import HabitRepository
from schemas.habits import HabitCreateSchema, HabitGetSchema, HabitUpdateSchema
from services.habits import HabitService

router = APIRouter()


def get_habit_service(db: AsyncSession = Depends(get_db)) -> HabitService:
    return HabitService(HabitRepository(db))


@router.post("/", response_model=HabitGetSchema, status_code=status.HTTP_201_CREATED)
async def create_habit(
    data: HabitCreateSchema,
    user: UserModel = Depends(get_current_user),
    service: HabitService = Depends(get_habit_service)):
    return await service.create(user, data)


@router.get("/", response_model=list[HabitGetSchema])
async def list_habits(
    user: UserModel = Depends(get_current_user),
    service: HabitService = Depends(get_habit_service)):
    return await service.list_for_user(user)


@router.get("/{habit_id}", response_model=HabitGetSchema)
async def get_habit(
    habit_id: int,
    user: UserModel = Depends(get_current_user),
    service: HabitService = Depends(get_habit_service)):
    try:
        return await service.get_owned(user, habit_id)
    except HabitNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Привычка не найдена")


@router.patch("/{habit_id}", response_model=HabitGetSchema)
async def update_habit(
    habit_id: int,
    data: HabitUpdateSchema,
    user: UserModel = Depends(get_current_user),
    service: HabitService = Depends(get_habit_service)):
    try:
        return await service.update(user, habit_id, data)
    except HabitNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Привычка не найдена")


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(
    habit_id: int,
    user: UserModel = Depends(get_current_user),
    service: HabitService = Depends(get_habit_service)):
    try:
        await service.delete(user, habit_id)
    except HabitNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Привычка не найдена")