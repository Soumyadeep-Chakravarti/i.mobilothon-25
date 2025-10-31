# backend/app/src/main.py (FINAL UPDATED VERSION)
import logging

from api.v1 import auth, ml, user  # IMPORTED NEW ROUTERS
from core.config import settings
from db.client import mongo_client
from fastapi import FastAPI, status

# Configure basic logging for visibility
logging.basicConfig(level=logging.INFO)


def create_app() -> FastAPI:
    """
    Initializes and configures the FastAPI application.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version="v1.3",
        debug=settings.DEBUG,
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
    )

    # --- Database Connection Lifecycle ---
    @app.on_event("startup")
    async def startup_event():
        await mongo_client.connect()

    @app.on_event("shutdown")
    async def shutdown_event():
        await mongo_client.close()

    # ------------------------------------

    # Include V1 routes (Domain Modularity)
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth Service"])
    app.include_router(user.router, prefix="/api/v1/users", tags=["User Service"])
    app.include_router(data.router, prefix="/api/v1/data", tags=["Data Service"])
    app.include_router(ml.router, prefix="/api/v1/ml", tags=["ML & Tasks"])
    app.include_router(
        notification.router, prefix="/api/v1/notify", tags=["Notification Service"]
    )
    app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin Service"])

    # Health Check Strategy
    @app.get("/health/liveness", tags=["Health"])
    def liveness_check():
        return {"status": "ok", "app": settings.APP_NAME}

    @app.get("/health/ready", status_code=status.HTTP_200_OK, tags=["Health"])
    async def readiness_check():
        if mongo_client.client is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="DB not connected",
            )

        # Add Redis/Task broker check here in a complete environment

        return {"status": "ok", "message": "All core components are ready"}

    return app


app = create_app()
