from typing import Any
from fastapi import HTTPException, UploadFile
from slugify import slugify
from sqlmodel import Session, select
from app.api.deps import CurrentUser
from app.models.post_model import Post
from app.models.tag_model import Tag
from app.utils import thumbnail_post_image
from app.schemas.post_schema import PostUpdate


async def get_post_by_title(*, session: Session, title: str) -> Post | None:    
    statement = select(Post).where(Post.title == title)
    session_post = await session.scalar(statement)
    return session_post

async def post_create(*, session: Session, current_user: CurrentUser, title: str, description: str, tags: list, file: UploadFile, content: str) -> Post:
    poster = thumbnail_post_image(file=file, email=current_user.email)
    post = Post(
        title=title, 
        description=description, 
        author_id=current_user.id, 
        slug=slugify(title, allow_unicode=True, separator="_"),
        content=content,
        poster=poster
    )       
    
    # Post image create
    
    # if fp:
    #     image = Image(filename=fp, post_id=post.id)        
    # else:
    #     raise HTTPException(status_code=400, detail="Uploaded file is not a valid image")
    
    # Post tag create
    tags = [item.strip() and ''.join(letter for letter in item if letter.isalnum()) for item in tags[0].split(',')]
    for i in range(len(tags)):
        tag = Tag(name=tags[i].lower(), post_id=post.id)
        session.add(tag)
    # session.add(image)
    session.add(post)
    await session.commit()

    return post


async def post_update(*, session: Session, current_post: Post, post_in: PostUpdate) -> Any:
    db_post = await get_post_by_title(session=session, title=post_in.title)    
    if db_post and current_post.id != db_post.id:
        raise HTTPException(status_code=400, detail="This title is already in use.")
    else:
        post_data = post_in.model_dump(exclude_unset=True)
        current_post.sqlmodel_update(post_data)
        session.add(current_post)
        await session.commit()
        session.refresh(current_post)
        return current_post