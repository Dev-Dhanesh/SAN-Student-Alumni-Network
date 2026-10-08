from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class CandidateProfile(BaseModel):
    user_id: str
    full_name: str
    department: str
    current_year: int = Field(default=3, ge=1, le=4)
    skills: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    preferred_roles: List[str] = Field(default_factory=list)
    registered_event_ids: List[str] = Field(default_factory=list)
    is_looking_for_team: bool = True
    bio: Optional[str] = None
    gender: Optional[str] = "m"


class TeamContext(BaseModel):
    team_id: Optional[str] = None
    event_id: Optional[str] = None
    event_title: Optional[str] = None
    event_category: Optional[str] = None
    needed_roles: List[str] = Field(default_factory=list)
    needed_skills: List[str] = Field(default_factory=list)
    current_member_skills: List[str] = Field(default_factory=list)
    target_year_level: Optional[int] = None


class ScoreBreakdown(BaseModel):
    skill_complementarity: float = Field(description="Max 30%")
    interest_compatibility: float = Field(description="Max 25%")
    event_compatibility: float = Field(description="Max 20%")
    experience: float = Field(description="Max 15%")
    availability: float = Field(description="Max 10%")


class TeammateRecommendation(BaseModel):
    user_id: str
    full_name: str
    department: str
    current_year: int
    matched_skills: List[str]
    preferred_roles: List[str]
    total_score: int = Field(description="Overall percentage from 0 to 100")
    breakdown: ScoreBreakdown
    reasons: List[str] = Field(description="Transparent bullet points explaining why this person is a match")


class TeamRecommendationRequest(BaseModel):
    team: TeamContext
    candidates: Optional[List[CandidateProfile]] = None
    top_k: int = 10


class TeamRecommendationResponse(BaseModel):
    team_id: Optional[str] = None
    recommendations: List[TeammateRecommendation]
    total_evaluated: int


# Frontend Team Matchmaker Integration Schemas
class TeamMatchmakerRequest(BaseModel):
    user_skills: List[str] = Field(default_factory=list)
    user_interests: List[str] = Field(default_factory=list)
    user_dept: Optional[str] = None
    needed_skills: List[str] = Field(default_factory=list)
    needed_interests: List[str] = Field(default_factory=list)


class TeamMatchmakerMember(BaseModel):
    id: str
    n: str
    g: str
    d: str
    s: List[str]
    i: List[str]
    p: int
    is_top_match: bool
    reasons: List[str]


class TeamMatchmakerResponse(BaseModel):
    matches: List[TeamMatchmakerMember]
    total_evaluated: int
