from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession


from db.session import get_db
from schemas.users import TokenSchema, UserCreateSchema, GetUserSchema
from core.exceptions import UserAlreadyExistsError, IncorrectEmailOrPass
from repositories.users import UserRepository
from schemas.users import UserCreateSchema, GetUserSchema
from services.users import UserService
from services.auth import AuthService

router = APIRouter()


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))
def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))

@router.post("/register", response_model=GetUserSchema, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreateSchema, service = Depends(get_user_service)):
    try: 
        return await service.register(user_data)
    except UserAlreadyExistsError: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )


@router.post("/login", response_model=TokenSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    try:
        token = await service.login(form_data.username, form_data.password)
    except IncorrectEmailOrPass:
           raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenSchema(access_token=token)
        