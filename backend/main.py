from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.session import engine
from app.db.init_db import init_db as initialize_database
from alembic import command
from alembic.config import Config

# Alembic configuration
alembic_cfg = Config("alembic.ini")

# Initialize database objects (tables & seed data)
def run_migrations_and_init():
    try:
        command.upgrade(alembic_cfg, "head")
        initialize_database(engine)
        print("[DB INIT SUCCESS]")
    except Exception as e:
        print(f"[DB INIT ERROR] {e}")

# Startup event
@asynccontextmanager
async def lifespan(app: FastAPI):
    #run_migrations_and_init()
    yield  # Continue app execution

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  #[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )



# Include API routers
from app.api.v1.auth import router as auth_router

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

# Healthcheck endpoint
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
