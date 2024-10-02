import uuid
from sqlmodel import Field, Relationship, SQLModel
from app.models.base_uuid_model import BaseUUIDModel


# Shared properties
class ImageBase(SQLModel):
    filename: str


# Database model, database table inferred from class name
class Image(BaseUUIDModel, ImageBase, table=True):
    __tablename__ = "post_images"

    post_id: uuid.UUID = Field(
        foreign_key="post.id", nullable=False, ondelete="CASCADE"
    )
    post: list["Post"] | None = Relationship(back_populates="images")  # type: ignore

