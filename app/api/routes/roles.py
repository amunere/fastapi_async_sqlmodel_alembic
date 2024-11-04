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
from sqlalchemy import func
from sqlmodel import select
from app.api.deps import (
    SessionDep, 
    get_current_active_superuser, 
    CurrentUser
)

from app.api.deps import get_current_active_superuser
from app.models.role_model import Role
from app.schemas.role_schema import RolesRead, RoleRead


router = APIRouter()

@router.get(
    "/", 
    summary="Get all roles", 
    response_model=RolesRead, 
    dependencies=[Depends(get_current_active_superuser)]
)
async def get_roles(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get all roles.
    """
    statement = select(Role).offset(skip).limit(limit)
    roles = await session.scalars(statement)

    return RolesRead(data=roles)
