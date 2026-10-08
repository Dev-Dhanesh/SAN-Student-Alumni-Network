from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from app.schemas.matching import (
    TeamRecommendationRequest,
    TeamRecommendationResponse,
    TeamMatchmakerRequest,
    TeamMatchmakerResponse,
    CandidateProfile,
)
from app.services.matching_service import DeterministicMatchingEngine
from app.services.demo_data import DEMO_STUDENTS
from app.core.supabase import get_supabase_client

router = APIRouter(prefix="/matching", tags=["Team Matching"])


@router.get("/members")
async def get_team_members_pool():
    """Returns the pool of students available for team formation."""
    supabase = get_supabase_client()
    if supabase:
        try:
            res = supabase.table("student_profiles").select("*").execute()
            if res.data:
                return [
                    {
                        "id": r["user_id"],
                        "n": r.get("full_name", "Student"),
                        "g": r.get("gender", "m"),
                        "d": r.get("department", "CSE"),
                        "s": r.get("skills", []),
                        "i": r.get("interests", []),
                    }
                    for r in res.data
                ]
        except Exception:
            pass
    return DEMO_STUDENTS


@router.post("/find-teammates", response_model=TeamMatchmakerResponse)
async def find_teammates(request: TeamMatchmakerRequest):
    """
    Evaluates students against user talents and needed teammate requirements.
    Directly powers the interactive frontend Matchmaker view with % scores and top match glows.
    """
    candidates = DEMO_STUDENTS
    supabase = get_supabase_client()
    if supabase:
        try:
            res = supabase.table("student_profiles").select("*").execute()
            if res.data:
                candidates = [
                    {
                        "id": r["user_id"],
                        "n": r.get("full_name", "Student"),
                        "g": r.get("gender", "m"),
                        "d": r.get("department", "CSE"),
                        "s": r.get("skills", []),
                        "i": r.get("interests", []),
                    }
                    for r in res.data
                ]
        except Exception:
            pass

    ranked = DeterministicMatchingEngine.matchmaker_rank(
        user_skills=request.user_skills,
        user_interests=request.user_interests,
        user_dept=request.user_dept,
        needed_skills=request.needed_skills,
        needed_interests=request.needed_interests,
        candidates=candidates,
    )

    return TeamMatchmakerResponse(
        matches=ranked,
        total_evaluated=len(candidates),
    )


@router.post("/team-recommendations", response_model=TeamRecommendationResponse)
async def get_team_recommendations(request: TeamRecommendationRequest):
    """
    Evaluates available student candidates using the 5-factor deterministic matching engine.
    """
    candidates = request.candidates
    if not candidates:
        candidates = [
            CandidateProfile(
                user_id=s["id"],
                full_name=s["n"],
                department=s["d"],
                current_year=3,
                skills=s["s"],
                interests=s["i"],
                preferred_roles=[],
                is_looking_for_team=True,
            )
            for s in DEMO_STUDENTS
        ]

    return DeterministicMatchingEngine.rank_candidates(
        team=request.team, candidates=candidates, top_k=request.top_k
    )
