from enum import Enum
from app.models.role_model import RoleBase
import uuid


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: uuid.UUID


class RoleEnum(str, Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"
    author = "author"