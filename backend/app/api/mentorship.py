from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/mentorship", tags=["Mentorship Requests"])


class MentorshipSubmitRequest(BaseModel):
    to_id: str = Field(alias="to")
    to_name: str = Field(alias="toN")
    from_name: str = Field(alias="from")
    from_email: str = Field(alias="fromE")
    message: str = Field(alias="msg")

    model_config = {"populate_by_name": True}


class MentorshipRespondRequest(BaseModel):
    request_id: str
    action: str = Field(description="'Accepted' or 'Declined'")


_dynamic_requests: List[Dict[str, Any]] = [
    {
        "id": "r101",
        "to": "a1",
        "toN": "Priya Nair",
        "from": "Aarav Shah",
        "fromE": "aarav.cse@saveetha.ac.in",
        "msg": "Hi Priya! I would love guidance on preparing for SDE-1 cloud systems interviews.",
        "st": "Pending",
    },
    {
        "id": "r102",
        "to": "a3",
        "toN": "Sneha Iyer",
        "from": "Ananya Rao",
        "fromE": "ananya.cse@saveetha.ac.in",
        "msg": "Could you review my resume and portfolio for Associate Product Manager roles?",
        "st": "Pending",
    },
]


@router.get("/requests")
async def list_mentorship_requests(user_email: Optional[str] = None):
    """Returns mentorship requests involving the user."""
    if not user_email:
        return _dynamic_requests
    return [
        r for r in _dynamic_requests
        if r.get("fromE", "").lower() == user_email.lower() or r.get("to", "").lower() == user_email.lower()
    ]


@router.post("/request", status_code=201)
async def submit_mentorship_request(payload: MentorshipSubmitRequest):
    """Submits a new mentorship inquiry from student to alumnus."""
    req_item = {
        "id": f"r{len(_dynamic_requests) + 1}",
        "to": payload.to_id,
        "toN": payload.to_name,
        "from": payload.from_name,
        "fromE": payload.from_email,
        "msg": payload.message,
        "st": "Pending",
    }
    _dynamic_requests.append(req_item)
    return {"message": "Mentorship request submitted", "request": req_item}


@router.post("/respond")
async def respond_to_mentorship(payload: MentorshipRespondRequest):
    """Alumni accepts or declines a student mentorship request."""
    for req in _dynamic_requests:
        if req["id"] == payload.request_id:
            req["st"] = payload.action
            return {"message": f"Request marked as {payload.action}", "request": req}
    raise HTTPException(status_code=404, detail="Mentorship request not found")
