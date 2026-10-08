from typing import Dict, Any, List
from pydantic import BaseModel, Field


class EmailVerificationRequest(BaseModel):
    email: str = Field(example="student.cse@saveetha.ac.in")


class EmailVerificationResponse(BaseModel):
    email: str
    is_valid_format: bool
    is_college_domain: bool
    domain: str
    suggested_role: str
    suggested_department: str
    verification_status: str


class PlatformHealthStats(BaseModel):
    total_students: int
    total_alumni: int
    total_opportunities: int
    total_events: int
    active_teams: int
    pending_verifications: int
    college_name: str
