from typing import List, Optional
from fastapi import APIRouter, Query
from app.schemas.journeys import (
    CareerJourneyDetail,
    CareerPatternAnalysis,
)
from app.services.journey_analyzer import JourneyAnalyzerService

router = APIRouter(prefix="/journeys", tags=["Career Journeys"])


@router.get("/", response_model=List[CareerJourneyDetail])
async def list_career_journeys():
    """
    Returns structured career journeys shared by verified college alumni,
    detailing timeline stages from college to current roles.
    """
    return JourneyAnalyzerService.list_all_journeys()


@router.get("/patterns", response_model=CareerPatternAnalysis)
async def get_career_pattern_analysis(
    target_role: Optional[str] = Query(None, description="Optional target role filter")
):
    """
    Returns aggregated career pattern analysis extracted from alumni journeys,
    highlighting typical timelines, milestone breakthroughs, and mistakes to avoid.
    """
    return JourneyAnalyzerService.get_pattern_analysis(target_role)
