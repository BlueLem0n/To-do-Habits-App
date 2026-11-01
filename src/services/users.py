from models.users import UserModel
from core.security import get_password_hash
from core.exceptions import UserAlreadyExistsError
from schemas.users import UserCreateSchema
from repositories.users import UserRepository


def normalize_email(email: str) -> str:
    return email.strip().lower()

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, data: UserCreateSchema) -> UserModel:
        email = normalize_email(data.email)
        if await self.repo.get_by_email(email) is None:
            raise UserAlreadyExistsError
        
        user = UserModel(
                username=data.username,
                email=email,
                hashed_password=get_password_hash(data.password))
        
        return await self.repo.add(user)