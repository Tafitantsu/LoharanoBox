from fastapi import APIRouter

from app.api.v1 import metiers, users, suggestions, auth, hierarchy, references, search, roles, permissions

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(permissions.router, prefix="/permissions", tags=["permissions"])
api_router.include_router(metiers.router, prefix="/metiers", tags=["metiers"])
api_router.include_router(suggestions.router, prefix="/suggestions", tags=["suggestions"])
api_router.include_router(hierarchy.router, prefix="/hierarchy", tags=["Hierarchy"])
api_router.include_router(references.router, prefix="/references", tags=["references"])
api_router.include_router(search.http_router, prefix="/search", tags=["search"])
