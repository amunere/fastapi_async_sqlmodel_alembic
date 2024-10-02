
from sqlmodel import Session, select

from app.core.security import get_password_hash
from app.core.session import AsyncSessionLocal
from app.api.deps import SessionDep
from app.core.config import settings
from app.crud.user_crud import create_user_role, create_user, get_role
from app.schemas.user_schema import UserCreate
from app.schemas.role_schema import RoleEnum, RoleCreate
from app.models.user_model import User


async def init_db():
    async with AsyncSessionLocal() as session:
        db_role = await get_role(session=session, role=RoleEnum.admin)
        if not db_role:
            for role in RoleEnum:
                role_in = RoleCreate(
                    name=role.name,
                    description=f"Role for {role.name}"
                )
                await create_user_role(session=session, role_in=role_in)

        statement = select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
        user = await session.scalar(statement=statement)
        if not user:
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
                is_active=True,
                role_id=db_role.id
            )
            print(user_in)
            # user = await create_user(session=SessionDep, user_create=user_in)
            db_obj = User.model_validate(
                user_in, update={"hashed_password": get_password_hash(user_in.password)}
            )
            session.add(db_obj)
            await session.commit() 