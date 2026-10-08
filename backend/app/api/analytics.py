from typing import Optional
from fastapi import APIRouter, Query
from app.schemas.analytics import CompanyInterviewAnalytics
from app.services.prep_analyzer import PrepAnalyzerService
from app.core.supabase import get_supabase_client

router = APIRouter(prefix="/analytics", tags=["Interview Analytics"])


@router.get("/interview-prep/{company}", response_model=CompanyInterviewAnalytics)
async def get_company_interview_prep(
    company: str,
    role: Optional[str] = Query(None, description="Optional role filter"),
):
    """
    Returns aggregated interview statistics for a given company:
    topic frequency percentages (DSA, OOP, DBMS, etc.), common rounds,
    difficulty distribution, and verified alumni advice.
    """
    experiences = None
    supabase = get_supabase_client()
    if supabase:
        try:
            query = supabase.table("interview_experiences").select("*").ilike("company", f"%{company}%")
            if role:
                query = query.ilike("role", f"%{role}%")
            res = query.execute()
            if res.data:
                experiences = res.data
        except Exception:
            experiences = None

    return PrepAnalyzerService.analyze_company_experiences(
        company_name=company, role=role, experiences=experiences
    )
