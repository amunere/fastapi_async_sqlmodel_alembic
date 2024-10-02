from sqlmodel import Session, select
from app.models.post_model import Post


async def get_post_by_title(*, session: Session, title: str) -> Post | None:    
    statement = select(Post).where(Post.title == title)
    session_post = await session.scalar(statement)
    return session_post