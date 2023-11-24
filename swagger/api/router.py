from fastapi import APIRouter
from api.semantic_search import semantic_app

api_router = APIRouter()

api_router.include_router(
    semantic_app.router,
    prefix="",
    tags=["semantic apis"],
)