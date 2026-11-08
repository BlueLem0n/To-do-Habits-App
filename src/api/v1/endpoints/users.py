from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import require_admin
from db.session import get_db
from models.users import UserModel
from repositories.users import UserRepository
from schemas.users import GetUserSchema

router = APIRouter()


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


@router.get("/", response_model=list[GetUserSchema])
async def get_all_users(
    admin: UserModel = Depends(require_admin),
    repo: UserRepository = Depends(get_user_repository),
):
    return await repo.list_all()