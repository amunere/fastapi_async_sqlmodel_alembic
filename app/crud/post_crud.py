from fastapi import HTTPException, UploadFile
from slugify import slugify
from sqlmodel import Session, select
from app.api.deps import CurrentUser
from app.models.post_image_model import Image
from app.models.post_model import Post
from app.models.tag_model import Tag
from app.utils import thumbnail_post_image


async def get_post_by_title(*, session: Session, title: str) -> Post | None:    
    statement = select(Post).where(Post.title == title)
    session_post = await session.scalar(statement)
    return session_post

async def post_create(*, session: Session, current_user: CurrentUser, title: str, description: str, tags: list, file: UploadFile) -> Post:
    post = Post(
        title=title, 
        description=description, 
        author_id=current_user.id, 
        slug=slugify(title, allow_unicode=True, separator="_")
    )       
    
    # Post image create
    fp = thumbnail_post_image(file=file, email=current_user.email)
    if fp:
        image = Image(filename=fp, post_id=post.id)        
    else:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image")
    
    # Post tag create
    tags = [item.strip() for item in tags[0].split(',')]    
    for i in range(len(tags)):
        tag = Tag(name=tags[i], post_id=post.id)
        session.add(tag)
    session.add(image)
    session.add(post)
    await session.commit()

    return post