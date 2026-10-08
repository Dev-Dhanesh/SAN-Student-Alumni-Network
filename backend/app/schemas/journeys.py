from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class JourneyStage(BaseModel):
    stage_name: str = Field(description="e.g. 'College & Academics', 'Skills Learned', 'Projects Built', 'First Internship', 'Campus & Off-Campus Applications', 'Interview Rounds', 'First Job', 'Current Role'")
    timeframe: str = Field(description="e.g. 'Year 2, Sem 4', '2023 - 2024'")
    details: str
    highlights: List[str] = Field(default_factory=list)


class CareerJourneyDetail(BaseModel):
    id: str
    alumni_id: str
    alumni_name: str
    current_company: str
    current_role: str
    department: str
    graduation_year: int
    stages: List[JourneyStage]
    mistakes_made: Optional[str] = None
    lessons_learned: Optional[str] = None
    advice_for_juniors: Optional[str] = None


class CareerPatternAnalysis(BaseModel):
    target_role_category: str
    sample_size: int
    common_starting_skills: List[str]
    typical_internship_timeline: str
    key_breakthrough_milestones: List[str]
    frequent_mistakes_to_avoid: List[str]
    top_recommended_resources: List[str]
