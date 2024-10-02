import uuid
from typing import Any
from fastapi import (
    BackgroundTasks, 
    Depends, 
    APIRouter, 
    File, 
    HTTPException, 
    UploadFile,
)
from sqlmodel import col, delete, func, select
from app.crud import user_crud as crud
from app.core.config import settings
from app.models.user_model import User
from app.models.post_model import Post
from app.schemas.user_schema import (
    UserPublic, 
    UserCreate, 
    UserUpdateSelf,
    UsersPublic, 
    UpdatePassword,
    UserUpdate
)
from app.schemas.common_schema import Message

from app.core import security
from app.api.deps import (
    SessionDep, 
    get_current_active_superuser, 
    CurrentUser
)
from app.utils import (
    generate_new_account_email, 
    send_email, 
)

router = APIRouter()


@router.post("/create", summary="Create new user", response_model=UserPublic)
async def create_user(background_tasks: BackgroundTasks, user_in: UserCreate, session: SessionDep) -> Any:
    """
    Create new user.
    """
    db_user = await crud.get_user_by_email(session=session, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Invalid user credentials")
    user = await crud.create_user(session=session, user_create=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
        background_tasks.add_task(
            send_email, 
            email_to=user_in.email, 
            subject=email_data.subject, 
            html_content=email_data.html_content
        )
    return user


@router.patch("/me", summary="Update user", response_model=UserPublic)
async def update_user(*, session: SessionDep, user_in: UserUpdateSelf, current_user: CurrentUser) -> Any: 
    """
    Update own user.
    """     
    if user_in.email:
        existing_user = await crud.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )
        
    user = await crud.update_user(session=session, current_user=current_user, user_in=user_in)
    return user


@router.get(
    "/", 
    summary="Get all users", 
    response_model=list, 
    dependencies=[Depends(get_current_active_superuser)]
)
async def get_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all users.
    """

    count_statement = select(func.count()).select_from(User)
    count = await session.scalar(count_statement)

    statement = select(User).offset(skip).limit(limit)
    users = await session.exec(statement)

    return UsersPublic(data=users, count=count)


@router.get("/me", response_model=UserPublic, summary="Get current user")
async def get_user(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """    
    return current_user


@router.patch("/me/password", response_model=Message, summary="Update user password")
async def update_user_password(
    *, session: SessionDep, body: UpdatePassword, current_user: CurrentUser
) -> Any:
    """
    Update user password.
    """
    if not security.verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one"
        )
    hashed_password = security.get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    await session.commit()
    return Message(message="Password updated successfully")


@router.delete("/me", response_model=Message, summary="Delete own user")
async def delete_user(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Delete own user.
    """
    if current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )
    statement = delete(Post).where(col(Post.owner_id) == current_user.id)
    await session.exec(statement)  
    await session.delete(current_user)
    await session.commit()
    return Message(message="User deleted successfully")


@router.get("/{user_id}", response_model=UserPublic)
async def read_user_by_id(
    user_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Get a user by id.
    """
    user = await session.get(User, user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )
    return user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
    summary="Update a user"
)
async def update_user(
    *,
    session: SessionDep,
    user_id: uuid.UUID,
    user_in: UserUpdate,
) -> Any:
    """
    Update a user.
    """
    current_user = await session.get(User, user_id)
    if not current_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    if user_in.email:
        existing_user = await crud.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

    current_user = await crud.update_user(session=session, current_user=current_user, user_in=user_in)
    return current_user


@router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)])
async def delete_user(
    session: SessionDep, current_user: CurrentUser, user_id: uuid.UUID
) -> Message:
    """
    Delete a user by id.
    """
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )
    statement = delete(Post).where(col(Post.owner_id) == user_id)
    await session.exec(statement) 
    await session.delete(user)
    await session.commit()
    return Message(message="User deleted successfully")


# @router.post("/avatar", response_model=Message, summary="Create user avatar") 
# async def create_avatar(background_tasks: BackgroundTasks, session: SessionDep, current_user: CurrentUser, file:UploadFile = File(...)):
#     """
#     Create user avatar.
#     """
#     image = Image.open(file.file)
#     image.thumbnail(settings.AVATAR_SIZE)
#     image.save(settings.FILE_PATH + "/" + current_user.email + "_" + "settings.TIMESTAMP" + "." + image.format)
#     return Message(message="File saved successfully")