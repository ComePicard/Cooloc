from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import Settings
from app.db.settings import initialize_postgres_pool, close_postgres_pool
from app.api.v1.endpoints import users, documents

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for the FastAPI application.
    """
    await initialize_postgres_pool()
    yield
    await close_postgres_pool()

def make_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    conf = Settings()
    app: FastAPI = FastAPI(title="Cooloc", lifespan=lifespan)
    app.include_router(users.router, prefix="/users", tags=["Users"])
    app.include_router(documents.router, prefix="/documents", tags=["Documents"])

    return app
