from typing import Optional, Set
import uuid
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel
from app.models.post_model import PostBase


class PostCreate(PostBase):
    pass


# Properties to receive on post update
class PostUpdate(PostBase):
    title: str | None = Field(default=None, min_length=1, max_length=255, unique=True) 
    description: str | None = Field(default=None, max_length=255)
    tags: Optional[Set[str]] = Field(default=None, sa_column=Column(ARRAY(String())))  
    

# Properties to return via API, id is always required
class PostPublic(PostBase):
    id: uuid.UUID
    author_id: uuid.UUID


class PostsPublic(SQLModel):
    data: list[PostPublic]
    count: int