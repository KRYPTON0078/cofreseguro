"""CofreSeguro API entrypoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from sqlalchemy import select, text

from cofreseguro import __version__
from cofreseguro.admin.router import router as admin_router
from cofreseguro.analyze.router import router as analyze_router
from cofreseguro.auth.router import router as auth_router
from cofreseguro.auth.security import hash_password
from cofreseguro.behaviour.router import router as behaviour_router
from cofreseguro.feedback.router import router as feedback_router
from cofreseguro.literacy.router import router as tips_router
from cofreseguro.shared.config import get_settings
from cofreseguro.shared.database import get_engine, get_session_factory, init_db
from cofreseguro.shared.logging import configure_logging, get_logger
from cofreseguro.shared.metrics import metrics_response
from cofreseguro.shared.models import User
from cofreseguro.shared.rate_limit import SlidingWindowLimiter, analyze_limiter

configure_logging()
logger = get_logger("api")
auth_limiter = SlidingWindowLimiter(max_requests=30, window_s=60.0)


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
    analyze_limiter.max_requests = settings.rate_limit_analyze
    auth_limiter.max_requests = settings.rate_limit_auth
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
    app.include_router(behaviour_router)
    app.include_router(admin_router)
    app.include_router(feedback_router)
    app.include_router(tips_router)

    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        client = request.client.host if request.client else "unknown"
        path = request.url.path
        if path.startswith("/v1/analyze") and not analyze_limiter.allow(client):
            return JSONResponse(
                {"detail": "rate limit exceeded"},
                status_code=429,
                headers={"Retry-After": "60"},
            )
        if path.startswith("/v1/auth/") and not auth_limiter.allow(client):
            return JSONResponse(
                {"detail": "rate limit exceeded"},
                status_code=429,
                headers={"Retry-After": "60"},
            )
        return await call_next(request)

    @app.get("/health")
    async def health() -> dict:
        return {
            "status": "healthy",
            "service": "cofreseguro-api",
            "version": __version__,
            "ollama_enabled": settings.ollama_enabled,
        }

    @app.get("/ready")
    async def ready():
        try:
            async with get_engine().connect() as conn:
                await conn.execute(text("SELECT 1"))
            return {"status": "ready", "database": "ok"}
        except Exception as exc:  # noqa: BLE001
            return JSONResponse(
                {"status": "not_ready", "database": str(exc)},
                status_code=503,
            )

    @app.get("/metrics")
    async def metrics() -> PlainTextResponse:
        return PlainTextResponse(metrics_response(), media_type="text/plain")

    return app


app = create_app()
