from fastapi import APIRouter
from app.schemas.nl_search import NLSearchRequest, NLSearchResponse
from app.services.ai_service import AIService

router = APIRouter(prefix="/search", tags=["Natural Language Search"])


@router.post("/nl", response_model=NLSearchResponse)
async def natural_language_search(request: NLSearchRequest):
    """
    Translates a conversational user query (e.g. 'Find AI hackathons for second-year students')
    into structured database filters and suggested categories.
    """
    return AIService.parse_natural_language_search(request)
