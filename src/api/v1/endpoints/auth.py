from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import create_access_token, get_password_hash, verify_password
from db.session import get_db
from models.users import UserModel
from schemas.users import TokenSchema, UserCreateSchema, GetUserSchema

router = APIRouter()


@router.post("/register", response_model=GetUserSchema, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    email = user_data.email.lower()

    existing = await db.execute(select(UserModel).where(UserModel.email == email))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )

    user = UserModel(
        username=user_data.username,
        email=email,
        hashed_password=get_password_hash(user_data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=TokenSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    email = form_data.username.lower()

    result = await db.execute(select(UserModel).where(UserModel.email == email))
    user = result.scalar_one_or_none()

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"sub": str(user.id)})
    return TokenSchema(access_token=token)