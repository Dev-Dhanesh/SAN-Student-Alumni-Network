from typing import List, Dict, Any, Optional
from app.schemas.journeys import (
    CareerJourneyDetail,
    JourneyStage,
    CareerPatternAnalysis,
)
from app.services.demo_data import DEMO_JOURNEYS


class JourneyAnalyzerService:
    """
    Analyzes multi-stage alumni career journeys to extract common trajectories,
    breakthrough milestones, mistakes to avoid, and junior guidance.
    """

    @classmethod
    def list_all_journeys(cls) -> List[CareerJourneyDetail]:
        results: List[CareerJourneyDetail] = []
        for j in DEMO_JOURNEYS:
            stages = [
                JourneyStage(
                    stage_name=st["stage_name"],
                    timeframe=st["timeframe"],
                    details=st["details"],
                    highlights=st.get("highlights", []),
                )
                for st in j.get("stages", [])
            ]
            results.append(
                CareerJourneyDetail(
                    id=j["id"],
                    alumni_id=j["alumni_id"],
                    alumni_name=j["alumni_name"],
                    current_company=j["current_company"],
                    current_role=j["current_role"],
                    department=j["department"],
                    graduation_year=j["graduation_year"],
                    stages=stages,
                    mistakes_made=j.get("mistakes_made"),
                    lessons_learned=j.get("lessons_learned"),
                    advice_for_juniors=j.get("advice_for_juniors"),
                )
            )
        return results

    @classmethod
    def get_pattern_analysis(cls, target_role: Optional[str] = None) -> CareerPatternAnalysis:
        role_label = target_role or "Software Engineering & Cloud"
        return CareerPatternAnalysis(
            target_role_category=role_label,
            sample_size=12,
            common_starting_skills=[
                "C++ / Java Basics (Year 1)",
                "Data Structures & LeetCode (Year 2)",
                "Full-Stack Web Dev / Cloud (Year 3)",
                "System Design Basics (Year 4)",
            ],
            typical_internship_timeline="Year 3 Summer (Months 5 to 7)",
            key_breakthrough_milestones=[
                "Building at least 2 non-trivial full-stack projects beyond classroom syllabus",
                "Consistently solving 200+ LeetCode problems across core patterns",
                "Active participation in national or college hackathons (SIH / InnoHack)",
                "Securing an off-campus referral via Saveetha Alumni Network",
            ],
            frequent_mistakes_to_avoid=[
                "Focusing exclusively on CGPA while ignoring practical coding and GitHub projects",
                "Starting interview and DSA preparation only in final semester",
                "Submitting generic resumes without STAR-formatted accomplishment bullets",
                "Hesitating to reach out to senior alumni for mentorship and referrals",
            ],
            top_recommended_resources=[
                "Striver's SDE Sheet & A2Z DSA Course",
                "LeetCode Top Interview Questions",
                "Grokking Modern System Design",
                "Saveetha ACM Student Chapter Coding Workshops",
            ],
        )
