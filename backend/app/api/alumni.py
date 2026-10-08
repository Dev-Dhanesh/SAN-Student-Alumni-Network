from typing import List, Optional
from fastapi import APIRouter, Query
from app.services.demo_data import DEMO_ALUMNI
from app.core.supabase import get_supabase_client

router = APIRouter(prefix="/alumni", tags=["Alumni Directory"])


@router.get("/")
async def list_alumni(
    q: Optional[str] = Query(None, description="Search query"),
    department: Optional[str] = Query(None, description="Filter by department"),
    year: Optional[int] = Query(None, description="Filter by graduation year"),
    industry: Optional[str] = Query(None, description="Filter by industry"),
):
    """
    Returns verified alumni matching the frontend AL structure,
    supporting filters by department, graduation year, and industry.
    """
    alumni_list = list(DEMO_ALUMNI)
    supabase = get_supabase_client()
    if supabase:
        try:
            res = supabase.table("alumni_profiles").select("*").execute()
            if res.data:
                for row in res.data:
                    alumni_list.append({
                        "id": row["user_id"],
                        "n": row.get("full_name", "Alumni"),
                        "g": row.get("gender", "m"),
                        "y": row.get("graduation_year", 2020),
                        "d": row.get("department", "CSE"),
                        "c": row.get("current_company", "Company"),
                        "r": row.get("current_role", "Engineer"),
                        "s": row.get("skills", []),
                        "i": row.get("industry", "Technology"),
                        "x": f"{row.get('years_of_experience', 2)} years",
                        "g_guidance": row.get("mentorship_categories", ["Career guidance"]),
                    })
        except Exception:
            pass

    # Filtering
    filtered = []
    q_lower = q.lower() if q else ""
    for a in alumni_list:
        if department and a.get("d") != department:
            continue
        if year and int(a.get("y", 0)) != year:
            continue
        if industry and a.get("i") != industry:
            continue
        if q_lower:
            text = (a.get("n", "") + " " + a.get("c", "") + " " + a.get("r", "") + " " + " ".join(a.get("s", []))).lower()
            if q_lower not in text:
                continue
        filtered.append(a)

    return filtered
