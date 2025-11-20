from fastapi import APIRouter
from app.ws.v1 import search

ws_router = APIRouter()
ws_router.include_router(search.ws_router, prefix="/search", tags=["search_ws"])