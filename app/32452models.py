from typing import List, Optional
import uuid
from pydantic import EmailStr

from sqlalchemy import ARRAY, Column, String
from sqlmodel import Field, Relationship, SQLModel



# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    posts: list["Post"] = Relationship(back_populates="author", cascade_delete=True)
    # categories: list["Category"] = Relationship(back_populates="author", cascade_delete=True)
    image: str = None
    role_id: uuid.UUID = Field(
        foreign_key="user_role.id", nullable=False, ondelete="CASCADE"
    )
    role: list["UserRole"] | None = Relationship(back_populates="users")  


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

    # Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# Shared properties
class PostBase(SQLModel):
    title: str = Field(min_length=1, max_length=255, unique=True)  
    description: str | None = Field(default=None, max_length=255)
    

# Properties to receive on post creation
class PostCreate(PostBase):
    pass

# Properties to receive on post update
class PostUpdate(PostBase):
    title: str | None = Field(default=None, min_length=1, max_length=255, unique=True)  # type: ignore


# Database model, database table inferred from class name
class Post(PostBase, table=True):
    __tablename__ = "posts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(min_length=10, max_length=255, unique=True)
    description: str = Field(min_length=10, max_length=255)
    content: str | None = Field(min_length=10, max_length=255)
    author_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    author: User | None = Relationship(back_populates="posts")    
    slug: str
    images: list["Image"] = Relationship(back_populates="post", cascade_delete=True)
    tags: List[str] = Field(default=None, sa_column=Column(ARRAY(String())))
    # categories: 
    

# Properties to return via API, id is always required
class PostPublic(PostBase):
    id: uuid.UUID
    author_id: uuid.UUID


class PostsPublic(SQLModel):
    data: list[PostPublic]
    count: int


# Shared properties
class ImageBase(SQLModel):
    filename: str


# Properties to receive on image creation
class ImageCreate(ImageBase):
    pass


# Properties to receive on image update
class ImageUpdate(ImageBase):
    pass


# Database model, database table inferred from class name
class Image(ImageBase, table=True):
    __tablename__ = "post_images"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)     
    post_id: uuid.UUID = Field(
        foreign_key="post.id", nullable=False, ondelete="CASCADE"
    )
    post: list[Post] | None = Relationship(back_populates="images")


# Properties to return via API, id is always required
class ImagePublic(ImageBase):
    id: uuid.UUID    


class ImagesPublic(SQLModel):
    data: list[ImagePublic]
    count: int


# # Shared properties
# class CategoryBase(SQLModel):
#     title: str = Field(min_length=1, max_length=255, unique=True)  
#     description: str | None = Field(default=None, max_length=255)
    

# # Properties to receive on category creation
# class CategoryCreate(CategoryBase):
#     pass

# # Properties to receive on category update
# class CategoryUpdate(CategoryBase):
#     title: str | None = Field(default=None, min_length=1, max_length=255, unique=True)  # type: ignore


# # Database model, database table inferred from class name
# class Category(CategoryBase, table=True):
#     id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     title: str = Field(min_length=10, max_length=255, unique=True)
#     description: str = Field(min_length=10, max_length=255)
#     author_id: uuid.UUID = Field(
#         foreign_key="user.id", nullable=False, ondelete="CASCADE"
#     )
#     author: User | None = Relationship(back_populates="categories")    
#     slug: str

#     # posts: list[Post] | None = Relationship(back_populates="categories")
    

# # Properties to return via API, id is always required
# class CategoryPublic(CategoryBase):
#     id: uuid.UUID
#     author_id: uuid.UUID


# class CategoriesPublic(SQLModel):
#     data: list[CategoryPublic]
#     count: int


class UserRole(SQLModel, table=True):
    __tablename__ = "user_roles"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str

    users: list[User] = Relationship(back_populates="role")
