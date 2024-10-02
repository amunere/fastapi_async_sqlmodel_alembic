import uuid

from sqlmodel import Field, SQLModel
from app.models.post_model import PostBase


class PostCreate(PostBase):
    pass


# Properties to receive on post update
class PostUpdate(PostBase):
    title: str | None = Field(default=None, min_length=1, max_length=255, unique=True) 
    

# Properties to return via API, id is always required
class PostPublic(PostBase):
    id: uuid.UUID
    author_id: uuid.UUID


class PostsPublic(SQLModel):
    data: list[PostPublic]
    count: int