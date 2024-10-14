from pydantic import EmailStr
from sqlmodel import Field, SQLModel
from app.models.user_model import UserBase
from app.models.group_model import GroupBase
import uuid
from enum import Enum
from .role_schema import RoleRead


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  
    password: str | None = Field(default=None, min_length=8, max_length=40)


# This schema is used to avoid circular import
class GroupRead(GroupBase):
    id: uuid.UUID


class UserPublic(UserBase):
    id: uuid.UUID
    


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"


# Properties to receive via API on update, all are optional
class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    # password: str | None = Field(default=None, min_length=8, max_length=40)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)


class UserUpdateSelf(SQLModel):
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255) # type: ignore


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)