import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import settings
from app.api.matching import router as matching_router
from app.api.roadmap import router as roadmap_router
from app.api.analytics import router as analytics_router
from app.api.nl_search import router as search_router
from app.api.recommendations import router as recommendations_router
from app.api.journeys import router as journeys_router
from app.api.admin_compute import router as admin_compute_router
from app.api.alumni import router as alumni_router
from app.api.opportunities import router as opportunities_router
from app.api.stories import router as stories_router
from app.api.mentorship import router as mentorship_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPI Compute & AI Microservice for College Career & Opportunity Network (SAN)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware for Frontend Connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all API routers under API prefix (/api)
app.include_router(alumni_router, prefix=settings.API_V1_STR)
app.include_router(opportunities_router, prefix=settings.API_V1_STR)
app.include_router(stories_router, prefix=settings.API_V1_STR)
app.include_router(matching_router, prefix=settings.API_V1_STR)
app.include_router(mentorship_router, prefix=settings.API_V1_STR)
app.include_router(roadmap_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix=settings.API_V1_STR)
app.include_router(search_router, prefix=settings.API_V1_STR)
app.include_router(recommendations_router, prefix=settings.API_V1_STR)
app.include_router(journeys_router, prefix=settings.API_V1_STR)
app.include_router(admin_compute_router, prefix=settings.API_V1_STR)

# Frontend static directory
frontend_dir = Path(__file__).resolve().parent.parent.parent / "frontend"


@app.get("/api")
async def api_info():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "college": settings.COLLEGE_NAME,
        "version": "1.0.0",
        "endpoints": {
            "alumni": f"{settings.API_V1_STR}/alumni/",
            "opportunities": f"{settings.API_V1_STR}/opportunities/",
            "stories": f"{settings.API_V1_STR}/stories/",
            "matching": f"{settings.API_V1_STR}/matching/find-teammates",
            "mentorship": f"{settings.API_V1_STR}/mentorship/requests",
            "roadmap": f"{settings.API_V1_STR}/roadmap/generate",
            "analytics": f"{settings.API_V1_STR}/analytics/interview-prep/{{company}}",
            "search": f"{settings.API_V1_STR}/search/nl",
            "recommendations": f"{settings.API_V1_STR}/recommendations/personalize",
            "journeys": f"{settings.API_V1_STR}/journeys/",
            "admin_verify_email": f"{settings.API_V1_STR}/admin-compute/verify-email",
            "docs": "/docs",
        },
    }


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "san-backend-compute"}


# Serve frontend index and assets if directory exists
if frontend_dir.exists():
    @app.get("/logo.png")
    async def serve_logo():
        logo_file = frontend_dir / "logo.png"
        if not logo_file.exists():
            logo_file = frontend_dir.parent / "logo.png"
        if logo_file.exists():
            return FileResponse(logo_file, media_type="image/png")
        return {"error": "logo.png not found"}

    @app.get("/favicon.ico")
    async def serve_favicon():
        logo_file = frontend_dir / "logo.png"
        if not logo_file.exists():
            logo_file = frontend_dir.parent / "logo.png"
        if logo_file.exists():
            return FileResponse(logo_file, media_type="image/png")
        return {"error": "favicon not found"}

    @app.get("/")
    async def serve_frontend():
        index_file = frontend_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"message": "Frontend directory found, but index.html is missing"}

    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

