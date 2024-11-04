import uuid
from sqlmodel import Field, SQLModel
from sqlalchemy.orm import declared_attr
from datetime import datetime


class BaseUUIDModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)  
    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow()}
    )
    created_at: datetime | None = Field(
        default_factory=datetime.utcnow
    )