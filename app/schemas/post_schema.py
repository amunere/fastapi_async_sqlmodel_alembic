from typing import Optional, Set
import uuid
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel
from app.models.post_model import PostBase
from app.models.tag_model import Tag
from app.schemas.user_schema import UserPublic
# from app.schemas.post_image_schema import ImagePublic
from datetime import datetime


class PostCreate(PostBase):
    pass


# Properties to receive on post update
class PostUpdate(PostBase):
    title: str | None = Field(default=None, min_length=1, max_length=255, unique=True) 
    description: str | None = Field(default=None, max_length=255)
    tags: list
    content: str | None = Field(min_length=10, max_length=255)    
    

# Properties to return via API, id is always required
class PostPublic(PostBase):
    id: uuid.UUID
    created_at: datetime
    slug: str
    content: str
    poster: str
    author: UserPublic


class PostsPublic(SQLModel):
    data: list[PostPublic]
    count: int
