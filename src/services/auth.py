
from services.users import normalize_email
from repositories.users import UserRepository
from core.security import verify_password, create_access_token
from core.exceptions import IncorrectEmailOrPass

class AuthService:      
    def __init__(self, repo: UserRepository):
        self.repo = repo 

    async def authenticate(self, email: str, password: str):
        user = await self.repo.get_by_email(email)
        if user is None or not verify_password(password, user.hashed_password):
            raise IncorrectEmailOrPass
        return user

    async def login(self, email: str, password: str):
        user = await self.authenticate(email, password)
        return create_access_token({"sub": str(user.id)})
                    
                    
