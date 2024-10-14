import uuid
from sqlmodel import Field, SQLModel
from app.models.tag_model import TagBase


class TagCreate(TagBase):
    pass


# Properties to receive on post update
class TagtUpdate(TagBase):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    post: uuid.UUID

# Properties to return via API, id is always required
class TagPublic(TagBase):
    id: uuid.UUID
    post_id: uuid.UUID
    name: str


class TagsPublic(SQLModel):
    name: list[TagPublic]
    count: int