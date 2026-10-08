from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class TopicFrequency(BaseModel):
    topic: str
    frequency_percentage: float = Field(description="Percentage (0 - 100%)")
    count: int
    focus_level: str = Field(description="'Crucial', 'High', 'Moderate'")


class InterviewRoundSummary(BaseModel):
    round_name: str
    typical_duration: str
    focus_areas: List[str]
    common_questions: List[str]


class CompanyInterviewAnalytics(BaseModel):
    company: str
    role: Optional[str] = "All Roles"
    total_experiences_analyzed: int
    difficulty_breakdown: Dict[str, int]
    topics: List[TopicFrequency]
    common_rounds: List[InterviewRoundSummary]
    top_resources: List[str]
    alumni_advice_highlights: List[str]
