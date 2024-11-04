import uuid
from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel, Relationship
from app.models.base_uuid_model import BaseUUIDModel


class RoleBase(SQLModel):
    name: str = Field(sa_column=Column(String, unique=True))
    description: str
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")


class Role(BaseUUIDModel, RoleBase, table=True): 
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    user: list["User"] | None = Relationship(back_populates="roles", sa_relationship_kwargs={'lazy': 'selectin'})   # type: ignore