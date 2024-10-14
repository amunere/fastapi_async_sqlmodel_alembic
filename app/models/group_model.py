from sqlmodel import Field, Relationship, SQLModel
from app.models.base_uuid_model import BaseUUIDModel
from app.models.user_group_model import UserGroup
# from app.models.user_model import User
import uuid


class GroupBase(SQLModel):
    name: str
    description: str


class Group(BaseUUIDModel, GroupBase, table=True):
    creater_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    creater: list["User"] | None = Relationship(back_populates="groups")     # type: ignore
    users: list["User"] = Relationship( # type: ignore
        back_populates="groups",
        link_model=UserGroup,
        sa_relationship_kwargs={"lazy": "selectin"},
    )