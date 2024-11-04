from pydantic import EmailStr
from sqlmodel import Field, SQLModel
from app.models.tag_model import Tag
from app.models.user_model import UserBase
import uuid
from enum import Enum
from .role_schema import RoleRead


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  
    # password: str | None = Field(default=None, min_length=8, max_length=40)
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    role_id: uuid.UUID


class UserPublic(UserBase):
    city: str | None = None
    state: str | None = None
    country: str | None = None
    address: str | None = None
    picture: str | None = None
    role: RoleRead


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# class UserStatus(str, Enum):
#     active = "active"
#     inactive = "inactive"


# Properties to receive via API on update, all are optional
# class UserUpdate(SQLModel):
#     email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
#     first_name: str | None = Field(default=None, max_length=255)
#     last_name: str | None = Field(default=None, max_length=255)
#     role: list


class UserUpdateSelf(SQLModel):
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    city: str | None = None
    state: str | None = None
    country: str | None = None
    address: str | None = None
    picture: str | None = None
    phone: str | None = None


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)