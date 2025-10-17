from fastapi import FastAPI
from app.core.config import settings


def create_app() -> FastAPI:
    settings.ensure_data_dir()

    app = FastAPI(
        title=settings.APP_NAME,
        openapi_url=settings.OPENAPI_URL,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
    )

    from app.api.v1.routes_terms import router as terms_router

    app.include_router(terms_router, prefix="/api/v1", tags=["terms"])

    # migrations are executed externally in the container entrypoint

    return app


app = create_app()

