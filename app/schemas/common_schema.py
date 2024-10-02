import uuid
from enum import Enum

from sqlmodel import Field, SQLModel
from app.schemas.role_schema import RoleRead


class GenderEnum(str, Enum):
    female = "female"
    male = "male"
    other = "other"


class MetaGeneral(SQLModel):
    roles: list[RoleRead]


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


class UserMessage(SQLModel):
    """User message schema."""

    user_id: uuid.UUID | None = None
    message: str


class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)