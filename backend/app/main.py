"""Application factory — wires config, middleware, and routers into a FastAPI app.

Keep this file boring: it composes, it does not contain business logic.
Run locally:  uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.v1.router import api_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=f"{settings.app_name} API",
        version=__version__,
        description=f"{settings.app_name} — retail ERP for US stores (a {settings.app_vendor} product).",
        debug=settings.debug,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/", tags=["root"], summary="Service banner")
    def root() -> dict[str, str]:
        return {"app": settings.app_name, "vendor": settings.app_vendor, "version": __version__}

    return app


app = create_app()
