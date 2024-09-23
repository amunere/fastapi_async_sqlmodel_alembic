from typing import Any
from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import User, UserCreate, UserUpdate, Post


async def create_user(*, session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    await session.commit()
    return db_obj


async def update_user(*, session: Session, current_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    current_user.sqlmodel_update(user_data, update=extra_data)
    session.add(current_user)
    await session.commit()
    session.refresh(current_user)
    return current_user


async def get_user_by_email(*, session: Session, email: str) -> User | None:    
    statement = select(User).where(User.email == email)
    session_user = await session.scalar(statement)
    return session_user


async def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = await get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


# def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
#     db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
#     session.add(db_item)
#     session.commit()
#     session.refresh(db_item)
#     return db_item


async def get_post_by_title(*, session: Session, title: str) -> Post | None:    
    statement = select(Post).where(Post.title == title)
    session_post = await session.scalar(statement)
    return session_post