import uuid
from sqlmodel import Field, Relationship, SQLModel
from app.models.base_uuid_model import BaseUUIDModel
from app.models.tag_model import Tag

# Shared properties
class PostBase(SQLModel):
    title: str = Field(min_length=1, max_length=255, unique=True)  
    description: str | None = Field(default=None, max_length=255)
    


# Database model, database table inferred from class name
class Post(BaseUUIDModel, PostBase, table=True):  
    title: str = Field(min_length=10, max_length=255, unique=True)
    description: str = Field(min_length=10, max_length=255)
    content: str | None = Field(min_length=10, max_length=255)    
    author_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    author: list["User"] | None = Relationship(back_populates="posts", sa_relationship_kwargs={'lazy': 'selectin'})     # type: ignore
    slug: str = Field(min_length=10, max_length=255)
    poster: str | None
    tags: list[Tag] = Relationship(back_populates="post", cascade_delete=True, sa_relationship_kwargs={'lazy': 'selectin'}) 
    status: bool = Field(default=False)
    