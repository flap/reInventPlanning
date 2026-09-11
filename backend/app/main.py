from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.config import settings
from app.routers import plan, share

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plan.router, prefix="/api/v1", tags=["Plan"])
app.include_router(share.router, prefix="/api/v1/share", tags=["Location Share"])


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "version": "0.1.0"}


# AWS Lambda entry point (API Gateway HTTP API + Mangum).
handler = Mangum(app)
