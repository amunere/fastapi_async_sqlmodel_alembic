import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class TagBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)


class Tag(TagBase, table=True):  
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str 
    post_id: uuid.UUID = Field(
        foreign_key="post.id", nullable=False, ondelete="CASCADE"
    )
    post: list["Post"] | None = Relationship(back_populates="tags")  # type: ignore

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"