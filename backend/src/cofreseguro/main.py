"""CofreSeguro API entrypoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from sqlalchemy import select

from cofreseguro import __version__
from cofreseguro.analyze.router import router as analyze_router
from cofreseguro.auth.router import router as auth_router
from cofreseguro.auth.security import hash_password
from cofreseguro.shared.config import get_settings
from cofreseguro.shared.database import get_session_factory, init_db
from cofreseguro.shared.logging import configure_logging, get_logger
from cofreseguro.shared.metrics import metrics_response
from cofreseguro.shared.models import User

configure_logging()
logger = get_logger("api")


async def seed_demo_users() -> None:
    factory = get_session_factory()
    async with factory() as session:
        for email, password, role, name in [
            ("demo@cofreseguro.app", "demo123!", "user", "Demo User"),
            ("admin@cofreseguro.app", "admin123!", "admin", "Admin"),
        ]:
            existing = (
                await session.execute(select(User).where(User.email == email))
            ).scalar_one_or_none()
            if not existing:
                session.add(
                    User(
                        email=email,
                        password_hash=hash_password(password),
                        full_name=name,
                        role=role,
                        locale="en",
                    )
                )
        await session.commit()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    await seed_demo_users()
    logger.info("startup", version=__version__)
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=__version__, lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth_router)
    app.include_router(analyze_router)

    @app.get("/health")
    async def health() -> dict:
        return {
            "status": "healthy",
            "service": "cofreseguro-api",
            "version": __version__,
            "ollama_enabled": settings.ollama_enabled,
        }

    @app.get("/metrics")
    async def metrics() -> PlainTextResponse:
        return PlainTextResponse(metrics_response(), media_type="text/plain")

    return app


app = create_app()
