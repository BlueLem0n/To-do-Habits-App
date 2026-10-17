from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_current_user
from db.session import get_db
from models.tasks import TaskModel
from models.users import UserModel
from schemas.tasks import TaskCreateSchema, TaskGetSchema, TaskUpdateSchema

router = APIRouter()


async def check_user_task(task_id: int, current_user: UserModel, db: AsyncSession) -> TaskModel:
    task = await db.get(TaskModel, task_id)
    # Одинаковый ответ 404, чтобы не раскрывать существование чужих задач
    if task is None or task.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с id={task_id} не найдена",
        )
    return task


@router.post("/", response_model=TaskGetSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreateSchema,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    new_task = TaskModel(**task_data.model_dump(), user_id=current_user.id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@router.get("/", response_model=List[TaskGetSchema])
async def get_tasks(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(TaskModel).where(TaskModel.user_id == current_user.id))
    return result.scalars().all()


@router.get("/{task_id}", response_model=TaskGetSchema)
async def get_task(
    task_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await check_user_task(task_id, current_user, db)


@router.patch("/{task_id}", response_model=TaskGetSchema)
async def update_task(
    task_id: int,
    task_data: TaskUpdateSchema,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = await check_user_task(task_id, current_user, db)
    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    task = await check_user_task(task_id, current_user, db)
    await db.delete(task)
    await db.commit()