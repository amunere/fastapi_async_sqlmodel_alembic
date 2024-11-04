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
    nickname: str | None = Field(default=None, max_length=55)
    first_name: str | None = Field(default=None, max_length=55)
    last_name: str | None = Field(default=None, max_length=55)
    email: EmailStr = Field(sa_column=Column(String, index=True, unique=True))
    phone: str | None = Field(default=None, max_length=12)


# Database model, database table inferred from class name
class User(BaseUUIDModel, UserBase, table=True):    
    is_active: bool = False
    is_superuser: bool = False
    gender: Gender = Gender.other
    city: str | None = None
    state: str | None = None
    country: str | None = None
    address: str | None = None
    picture: str | None = None
    phone: str | None = None
    hashed_password: str
    posts: list["Post"] = Relationship(back_populates="author", cascade_delete=True) # type: ignore
    roles: list["Role"] = Relationship(back_populates="user", sa_relationship_kwargs={'lazy': 'selectin'}) # type: ignore
    groups: list["Group"] = Relationship(back_populates="creater", cascade_delete=True) # type: ignore
    gender: str

    def __str__(self):
        return self.first_name

