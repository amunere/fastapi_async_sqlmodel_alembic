from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel, Relationship
from app.models.base_uuid_model import BaseUUIDModel


class RoleBase(SQLModel):
    name: str = Field(sa_column=Column(String, unique=True))
    description: str


class Role(BaseUUIDModel, RoleBase, table=True): 
    __tablename__ = 'roles'
    users: list["User"] = Relationship(back_populates="role", sa_relationship_kwargs={'lazy': 'selectin'}) # type: ignore