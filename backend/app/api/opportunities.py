from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field
from app.services.demo_data import DEMO_OPPORTUNITIES
from app.core.supabase import get_supabase_client

router = APIRouter(prefix="/opportunities", tags=["Opportunities & Events"])


class OpportunityCreateRequest(BaseModel):
    title: str = Field(alias="t")
    type: str = Field(description="'Internship', 'Job', 'Hackathon', or 'Event'")
    organization: str = Field(alias="o")
    location: str = Field(alias="l")
    deadline: str = Field(alias="dl")
    skills: List[str] = Field(default_factory=list, alias="s")
    description: str = Field(alias="d")

    model_config = {"populate_by_name": True}


# In-memory storage for newly added demo opportunities
_dynamic_opportunities: List[Dict[str, Any]] = []


@router.get("/")
async def list_opportunities(
    q: Optional[str] = Query(None, description="Search keyword"),
    type: Optional[str] = Query(None, description="Filter by type (Internship, Job, Hackathon, Event)"),
    location: Optional[str] = Query(None, description="Filter by location keyword"),
):
    """
    Returns opportunities (internships, jobs, hackathons, and events)
    harmonized with the frontend OP schema.
    """
    all_opps = _dynamic_opportunities + DEMO_OPPORTUNITIES
    supabase = get_supabase_client()
    if supabase:
        try:
            res = supabase.table("opportunities").select("*").execute()
            if res.data:
                for row in res.data:
                    all_opps.append({
                        "id": str(row["id"]),
                        "t": row["title"],
                        "type": row["type"].capitalize(),
                        "o": row["company"],
                        "l": row.get("location", "Chennai"),
                        "s": row.get("skills_required", []),
                        "dl": row.get("deadline", "2026-12-31"),
                        "d": row.get("description", ""),
                    })
        except Exception:
            pass

    filtered = []
    q_lower = q.lower() if q else ""
    loc_lower = location.lower() if location else ""

    for o in all_opps:
        if type and type != "All" and o.get("type", "").lower() != type.lower():
            continue
        if loc_lower and loc_lower not in o.get("l", "").lower():
            continue
        if q_lower:
            text = (o.get("t", "") + " " + o.get("o", "") + " " + o.get("l", "") + " " + " ".join(o.get("s", []))).lower()
            if q_lower not in text:
                continue
        filtered.append(o)

    return filtered


@router.post("/", status_code=201)
async def create_opportunity(payload: OpportunityCreateRequest):
    """Publishes a new opportunity from alumni or college coordinator."""
    new_opp = {
        "id": f"p{len(_dynamic_opportunities) + len(DEMO_OPPORTUNITIES) + 1}",
        "t": payload.title,
        "type": payload.type,
        "o": payload.organization,
        "l": payload.location,
        "dl": payload.deadline,
        "s": payload.skills,
        "d": payload.description,
        "is_verified": True,
        "is_approved": True,
        "is_demo": True,
    }
    _dynamic_opportunities.insert(0, new_opp)
    return {"message": "Opportunity published successfully", "opportunity": new_opp}
