from sqlalchemy import Enum

class UserRoles(str, Enum):
    User = "user"
    Admin = "admin"