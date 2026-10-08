from fastapi import APIRouter
from app.schemas.roadmap import RoadmapRequest, RoadmapResponse
from app.services.ai_service import AIService

router = APIRouter(prefix="/roadmap", tags=["Career Roadmap"])


@router.post("/generate", response_model=RoadmapResponse)
async def generate_career_roadmap(request: RoadmapRequest):
    """
    Synthesizes a personalized career roadmap for a selected career goal
    grounded in alumni trajectory patterns.
    """
    return AIService.generate_career_roadmap(request)
