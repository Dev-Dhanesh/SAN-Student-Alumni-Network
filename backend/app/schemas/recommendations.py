from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class StudentProfileContext(BaseModel):
    user_id: str
    department: str
    current_year: int
    skills: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    career_goals: Optional[str] = None
    preferred_roles: List[str] = Field(default_factory=list)


class RecommendedItem(BaseModel):
    item_id: str
    title: str
    subtitle: str
    category: str
    match_percentage: int = Field(ge=0, le=100)
    match_reasons: List[str]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PersonalizedRecommendationsResponse(BaseModel):
    student_id: str
    events: List[RecommendedItem]
    opportunities: List[RecommendedItem]
    alumni: List[RecommendedItem]
    generated_at: str
