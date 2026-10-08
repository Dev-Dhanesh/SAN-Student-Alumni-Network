from fastapi import APIRouter
from app.schemas.recommendations import (
    StudentProfileContext,
    PersonalizedRecommendationsResponse,
)
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["Personalized Recommendations"])


@router.post("/personalize", response_model=PersonalizedRecommendationsResponse)
async def get_personalized_recommendations(profile: StudentProfileContext):
    """
    Returns personalized recommendations across Events, Opportunities, and Alumni
    tailored to the student's profile with transparent percentage scores and explicit reasons.
    """
    return RecommendationService.get_recommendations_for_student(profile)
