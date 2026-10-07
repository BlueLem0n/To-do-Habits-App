from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from models.tasks import TaskModel
from schemas.tasks import TaskCreateSchema, TaskGetSchema, TaskUpdateSchema

router = APIRouter()


async def check_task(task_id: int, db: AsyncSession) -> TaskModel:
    task = await db.get(TaskModel, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с id={task_id} не найдена",
        )
    return task


@router.post("/", response_model=TaskGetSchema, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreateSchema, db: AsyncSession = Depends(get_db)):
    new_task = TaskModel(**task_data.model_dump())
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@router.get("/", response_model=List[TaskGetSchema])
async def get_tasks(db: AsyncSession = Depends(get_db)):
    query = select(TaskModel)
    result = await db.execute(query)
    tasks = result.scalars().all()
    return tasks


@router.get("/{task_id}", response_model=TaskGetSchema)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    return await check_task(task_id, db)


@router.patch("/{task_id}", response_model=TaskGetSchema)
async def update_task(
    task_id: int, task_data: TaskUpdateSchema, db: AsyncSession = Depends(get_db)
):
    task = await check_task(task_id, db)

    update_dict = task_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(task, key, value)

    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await check_task(task_id, db)
    await db.delete(task)
    await db.commit()