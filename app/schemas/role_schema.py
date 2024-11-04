from enum import Enum
from sqlmodel import SQLModel
from app.models.role_model import RoleBase
import uuid


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    pass


class RoleEnum(str, Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"
    author = "author"


class RolesRead(SQLModel):
    data: list[RoleRead]