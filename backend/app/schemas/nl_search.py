from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class NLSearchRequest(BaseModel):
    query: str = Field(example="Find AI hackathons suitable for second-year students")
    college_id: Optional[str] = None


class ParsedFilters(BaseModel):
    entity_type: str = Field(description="'event', 'opportunity', 'alumni', 'teammate', or 'all'")
    skills: List[str] = Field(default_factory=list)
    roles: List[str] = Field(default_factory=list)
    target_year: Optional[int] = None
    category: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)


class NLSearchResponse(BaseModel):
    original_query: str
    parsed_intent: str
    filters: ParsedFilters
    explanation: str
    suggested_actions: List[str]
