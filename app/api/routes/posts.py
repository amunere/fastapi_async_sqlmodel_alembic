import uuid
from typing import Annotated, Any

from app.crud.post_crud import get_post_by_title, post_create

from fastapi import APIRouter, Form, HTTPException, UploadFile
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models.post_model import Post
from app.models.tag_model import Tag
from app.schemas.post_schema import PostsPublic, PostPublic, PostUpdate
from app.schemas.common_schema import Message

router = APIRouter()


@router.get("/", response_model=PostsPublic)
async def read_posts(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve posts.
    """

    if current_user.is_superuser:        
        count_statement = select(func.count()).select_from(Post)        
        count = await session.scalar(count_statement)        
        statement = select(Post).offset(skip).limit(limit)
        posts = await session.scalars(statement)
    else:
        count_statement = (
            select(func.count())
            .select_from(Post)
            .where(Post.owner_id == current_user.id)
        )
        count = await session.scalar(count_statement)
        statement = (
            select(Post)
            .where(Post.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        posts = await session.scalar(statement)

    return PostsPublic(data=posts, count=count)


@router.get("/{id}", response_model=PostPublic)
async def read_post(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get post by ID.
    """
    post = await session.get(Post, id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if not current_user.is_superuser and (post.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return post


@router.post("/", response_model=PostPublic)
async def create_post(
    *, session: SessionDep, 
    current_user: CurrentUser, 
    title: Annotated[str, Form()], 
    description: Annotated[str, Form()],
    tags: Annotated[list[str], Form()],
    file: UploadFile
) -> Any:
    """
    Create new post.
    """
    
    db_post = await get_post_by_title(session=session, title=title)
    if db_post:
        raise HTTPException(status_code=400, detail="This title is already in use.")
    
    post = await post_create(
        session=session, 
        current_user=current_user, 
        title=title,
        description=description,
        tags=tags,        
        file=file       
    )

    return post


@router.put("/{id}", response_model=PostPublic)
async def update_post(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    post_in: PostUpdate,
) -> Any:
    """
    Update an post.
    """
    post = await session.get(Post, id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if not current_user.is_superuser and (post.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    if post.title == post_in.title:
        raise HTTPException(status_code=400, detail="This title is already in use.")
    db_post = await get_post_by_title(session=session, title=post_in.title)
    if db_post:
        raise HTTPException(status_code=400, detail="This title is already in use.")
    update_dict = post_in.model_dump(exclude_unset=True)
    post.sqlmodel_update(update_dict)
    session.add(post)
    await session.commit()
    session.refresh(post)
    return post


@router.delete("/{id}")
async def delete_post(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an post.
    """
    post = await session.get(Post, id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if not current_user.is_superuser and (post.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    await session.delete(post)
    await session.commit()
    return Message(message="Post deleted successfully")


@router.get("/tag/{tag}")
async def get_post_by_tag(session: SessionDep, current_user: CurrentUser, tag: str) -> Any:
    statement = select(Tag).where(Tag.name == tag)
    posts = await session.scalars(statement)
    return posts