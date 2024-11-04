import uuid
from sqlmodel import Field, Relationship, SQLModel
from app.models.base_uuid_model import BaseUUIDModel


# Shared properties
class TagBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)


class Tag(BaseUUIDModel, TagBase, table=True):  
    name: str 
    post_id: uuid.UUID = Field(
        foreign_key="post.id", nullable=False, ondelete="CASCADE"
    )
    post: list["Post"] | None = Relationship(back_populates="tags")  # type: ignore

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"