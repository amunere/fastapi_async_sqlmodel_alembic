from sqlmodel import select
from app.core.security import get_password_hash
from app.core.session import AsyncSessionLocal
from app.core.config import settings
from app.crud.user_crud import create_user_role, get_role
from app.models.role_model import Role
from app.schemas.user_schema import UserCreate
from app.schemas.role_schema import RoleEnum, RoleCreate
from app.models.user_model import User


async def init_db():
    async with AsyncSessionLocal() as session:
        statement = select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
        user = await session.scalar(statement=statement)
        if not user:
            print('Create superuser') #todo set log
            user_in = UserCreate(
                nickname=settings.FIRST_SUPERUSER_NICKNAME,
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
                is_active=True,
            )
            user = User.model_validate(
                user_in, update={"hashed_password": get_password_hash(user_in.password)}
            )
            session.add(user)

            #Set admin role
            admin_role = RoleEnum.admin
            role = Role(name=admin_role, description=f"Role for {admin_role.name}", user_id=user.id)
            session.add(role)
            await session.commit()
        
            