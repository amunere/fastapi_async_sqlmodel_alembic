from fastapi import APIRouter

from app.api.routes import auth, users, posts

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["login"])
api_router.include_router(users.router, prefix="/user", tags=["user"])
api_router.include_router(posts.router, prefix="/post", tags=["post"])