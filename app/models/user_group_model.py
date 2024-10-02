from sqlmodel import Field, SQLModel
from app.models.base_uuid_model import BaseUUIDModel
import uuid


class UserGroup(BaseUUIDModel, SQLModel, table=True):
    group_id: uuid.UUID | None = Field(
        foreign_key="group.id", nullable=False, ondelete="CASCADE"
    )
    user_id: uuid.UUID | None = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
