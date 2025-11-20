from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.ws.v1.ws_api import ws_router as ws_api_router
from app.core.config import settings
from app.db.init_db import init_db
from app.db.session import SessionLocal

app = FastAPI()

# CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], #[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

app.include_router(api_router, prefix="/api/v1")
app.include_router(ws_api_router, prefix="/ws/v1")

@app.get("/")
def read_root():
    return {"Hello": "World"}
