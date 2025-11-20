from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api
#from app.ws.v1.ws import ws
from app.core.config import settings
from app.services.main_service import onstart



app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    openapi_url="/openapi.json",
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
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  #[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
def on_startup():
    onstart()

app.include_router(api, prefix="/api/v1", tags=["api", "v1"])
#app.include_router(ws, prefix="/ws/v1", tags=["ws", "v1"])

@app.get("/")
def read_root():
    title=settings.PROJECT_NAME
    version=settings.VERSION
    return {"Status": "ok",
            "Title": title,
            "Version": version}

