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
from app.crud import user_crud, post_crud

router = APIRouter()


@router.get("/all", response_model=PostsPublic)
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
            .where(Post.status == True)
        )
        count = await session.scalar(count_statement)
        statement = (
            select(Post)
            .where(Post.status == True)
            .offset(skip)
            .limit(limit)
        )
        posts = await session.scalars(statement)
    # print(f'AAAAAAAAAAAAAAAAAAAAAAAA {posts.all()}')
    return PostsPublic(data=posts, count=count)


@router.get("/self", response_model=PostsPublic)
async def read_self_posts(
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
            .where(Post.author_id == current_user.id)
        )
        count = await session.scalar(count_statement)
        statement = (
            select(Post)
            .where(Post.author_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        posts = await session.scalars(statement)

    return PostsPublic(data=posts, count=count)


@router.get("/{id}", response_model=PostPublic)
async def read_post(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get post by ID.
    """
    post = await session.get(Post, id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if not current_user.is_superuser and (post.author_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return post


@router.get("/slug/{slug}", response_model=PostPublic)
async def read_post_by_slug(session: SessionDep, current_user: CurrentUser, slug: str) -> Any:
    """
    Get post by slug.
    """
    statement = select(Post).where(Post.slug == slug).where(Post.status == True)
    post = await session.scalar(statement)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/author/{nickname}", response_model=PostsPublic)
async def read_posts_by_author(session: SessionDep, current_user: CurrentUser, nickname: str) -> Any:
    """
    Get posts by author.
    """    
    author = await user_crud.get_user_by_nickname(session=session, nickname=nickname)    
    if author:
        statement = select(Post).where(Post.status == True).filter(Post.author_id == author.id)
        posts = await session.scalars(statement)
        if not posts:
            raise HTTPException(status_code=404, detail="Post not found")
        count_statement = (
            select(func.count())
            .select_from(Post)
            .where(Post.status == True)
            .filter(Post.author_id == author.id)
        )
        count = await session.scalar(count_statement)
        return PostsPublic(data=posts.all(), count=count)
    else:
        raise HTTPException(status_code=404, detail=f'{nickname} posts not found')


@router.post("/", response_model=PostPublic)
async def create_post(
    *, session: SessionDep, 
    current_user: CurrentUser, 
    title: Annotated[str, Form()], 
    description: Annotated[str, Form()],
    tags: Annotated[list[str], Form()],
    file: UploadFile,
    content: Annotated[str, Form()],
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
        file=file,
        content=content
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
    if not current_user.is_superuser and (post.author_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_post = await post_crud.post_update(session=session, current_post=post, post_in=post_in)
    return update_post


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
    if not current_user.is_superuser and (post.author_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    await session.delete(post)
    await session.commit()
    return Message(message="Post deleted successfully")


@router.get("/tag/{tag}")
async def get_post_by_tag(session: SessionDep, current_user: CurrentUser, tag: str) -> Any:
    statement = select(Tag).where(Tag.name == tag)
    posts = await session.scalars(statement)
    return posts