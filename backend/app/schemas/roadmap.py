from typing import List, Optional
from pydantic import BaseModel, Field


class RoadmapMilestone(BaseModel):
    step_number: int
    stage_title: str
    description: str
    key_skills: List[str]
    suggested_projects: List[str]
    preparation_tips: List[str]
    estimated_duration: str


class RoadmapRequest(BaseModel):
    career_goal: str = Field(example="Software Development Engineer")
    current_year: int = Field(default=2, ge=1, le=4)
    department: str = Field(default="Computer Science")
    current_skills: List[str] = Field(default_factory=list)


class RoadmapResponse(BaseModel):
    career_goal: str
    overview: str
    target_role: str
    milestones: List[RoadmapMilestone]
    alumni_insights_count: int = 0
    source_type: str = Field(description="'gemini_ai' or 'alumni_pattern_engine'")
