from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from app.services.demo_data import DEMO_STORIES

router = APIRouter(prefix="/stories", tags=["Stories & Updates"])


class StoryCreateRequest(BaseModel):
    title: str = Field(alias="t")
    category: str = Field(alias="cat")
    author_name: str = Field(alias="n")
    year_or_dept: str = Field(alias="y")
    company: Optional[str] = Field(default="", alias="c")
    body: str = Field(alias="b")
    role: str = Field(default="alumni")
    gender: str = Field(default="m", alias="g")

    model_config = {"populate_by_name": True}


_dynamic_stories: List[Dict[str, Any]] = []


@router.get("/")
async def list_stories(
    category: Optional[str] = Query(None, description="Category filter (e.g. Office Life, Tech Update)")
):
    """Returns stories and updates shared by alumni and students."""
    all_stories = _dynamic_stories + DEMO_STORIES
    if category and category != "All":
        return [s for s in all_stories if s.get("cat", "").lower() == category.lower()]
    return all_stories


@router.post("/", status_code=201)
async def create_story(payload: StoryCreateRequest):
    """Publishes a new blog, office update, hackathon report, or career story."""
    new_story = {
        "id": f"s{len(_dynamic_stories) + len(DEMO_STORIES) + 1}",
        "t": payload.title,
        "cat": payload.category,
        "n": payload.author_name,
        "y": payload.year_or_dept,
        "c": payload.company or "",
        "b": payload.body,
        "role": payload.role,
        "g": payload.gender,
        "date": "Just now",
    }
    _dynamic_stories.insert(0, new_story)
    return {"message": "Story published successfully", "story": new_story}
