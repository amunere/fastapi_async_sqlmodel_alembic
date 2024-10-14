import enum
import uuid
from pydantic import EmailStr

from sqlalchemy import ARRAY, Column, String
from sqlalchemy.dialects.postgresql import ENUM as Enum
from sqlmodel import Field, Relationship, SQLModel
from app.models.base_uuid_model import BaseUUIDModel


class Gender(str, enum.Enum):
    female = "Female"
    male = "Male"
    other = "Other"


# Shared properties
class UserBase(SQLModel):
    first_name: str | None = Field(default=None, max_length=255)
    last_name: str | None = Field(default=None, max_length=255)
    email: EmailStr = Field(sa_column=Column(String, index=True, unique=True))
    is_active: bool = True
    is_superuser: bool = False
    gender: Gender = Gender.other
    state: str | None = None
    country: str | None = None
    address: str | None = None
    picture: str | None = None
    phone: str | None = None


# Database model, database table inferred from class name
class User(BaseUUIDModel, UserBase, table=True):
    hashed_password: str
    posts: list["Post"] = Relationship(back_populates="author", cascade_delete=True) # type: ignore
    role_id: uuid.UUID = Field(foreign_key="roles.id", nullable=False, ondelete="CASCADE")
    role: list["Role"] | None = Relationship(back_populates="users", sa_relationship_kwargs={'lazy': 'selectin'})   # type: ignore
    groups: list["Group"] = Relationship(back_populates="creater", cascade_delete=True) # type: ignore
    gender: str

