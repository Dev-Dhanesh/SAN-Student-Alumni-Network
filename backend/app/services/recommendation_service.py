from datetime import datetime, timezone
from typing import List, Dict, Any, Set
from app.schemas.recommendations import (
    StudentProfileContext,
    RecommendedItem,
    PersonalizedRecommendationsResponse,
)
from app.services.demo_data import DEMO_EVENTS, DEMO_OPPORTUNITIES, DEMO_ALUMNI


class RecommendationService:
    """
    Computes personalized recommendations across Events, Opportunities, and Alumni
    based on student profile (skills, interests, department, year, career goals).
    Outputs transparent explanation bullets for each recommendation.
    """

    @classmethod
    def get_recommendations_for_student(
        cls, profile: StudentProfileContext
    ) -> PersonalizedRecommendationsResponse:
        student_skills = {s.lower().strip() for s in profile.skills}
        student_interests = {i.lower().strip() for i in profile.interests}
        goal_text = (profile.career_goals or "").lower()

        # 1. Rank Events
        recommended_events: List[RecommendedItem] = []
        for evt in DEMO_EVENTS:
            evt_skills = {s.lower().strip() for s in evt.get("skills_focus", [])}
            matched_skills = student_skills.intersection(evt_skills)
            
            # Category and interest overlap
            evt_tokens = {w for w in (evt["title"] + " " + evt["description"]).lower().split() if len(w) > 3}
            matched_interests = student_interests.intersection(evt_tokens)

            # Score computation
            score = 50  # Baseline college event relevance
            reasons = []

            if matched_skills:
                skill_boost = min(30, len(matched_skills) * 15)
                score += skill_boost
                reasons.append(f"Requires your core skills: {', '.join([s.capitalize() for s in matched_skills])}.")
            
            if matched_interests:
                score += 15
                reasons.append(f"Matches your stated interests in {', '.join(list(matched_interests)[:2])}.")

            cat_str = evt.get("category", evt.get("type", "hackathon")).lower()
            if profile.current_year >= 2 and cat_str == "hackathon":
                score += 10
                reasons.append(f"Ideal competitive hackathon for Year {profile.current_year} students.")

            score = min(98, max(45, score))
            if not reasons:
                reasons.append("High campus participation and peer alignment.")

            recommended_events.append(
                RecommendedItem(
                    item_id=evt["id"],
                    title=evt.get("title", evt.get("t", "")),
                    subtitle=evt.get("organizer", evt.get("o", "College")),
                    category=cat_str.capitalize(),
                    match_percentage=score,
                    match_reasons=reasons,
                    metadata={"mode": evt.get("mode", "offline"), "venue": evt.get("venue", evt.get("l"))},
                )
            )

        recommended_events.sort(key=lambda x: x.match_percentage, reverse=True)

        # 2. Rank Opportunities
        recommended_opps: List[RecommendedItem] = []
        for opp in DEMO_OPPORTUNITIES:
            opp_skills = {s.lower().strip() for s in opp.get("skills_required", [])}
            matched_skills = student_skills.intersection(opp_skills)
            
            score = 50
            reasons = []

            if matched_skills:
                score += min(35, len(matched_skills) * 12)
                reasons.append(f"Your skills ({', '.join([s.capitalize() for s in matched_skills])}) match job requirements.")

            opp_title = opp.get("title", opp.get("t", ""))
            opp_company = opp.get("company", opp.get("o", ""))
            opp_type = opp.get("type", "Internship")

            if goal_text and any(word in goal_text for word in opp_title.lower().split()):
                score += 15
                reasons.append(f"Directly advances your target career goal: '{profile.career_goals}'.")

            if opp.get("is_verified"):
                score += 5
                reasons.append("Verified opening with active Saveetha alumni referrals.")

            score = min(96, max(40, score))
            if not reasons:
                reasons.append("Relevant opening for upcoming placement cycles.")

            recommended_opps.append(
                RecommendedItem(
                    item_id=opp["id"],
                    title=opp_title,
                    subtitle=f"{opp_company} • {opp_type.capitalize()}",
                    category=opp_type.capitalize(),
                    match_percentage=score,
                    match_reasons=reasons,
                    metadata={"stipend_salary": opp.get("stipend_salary"), "location": opp.get("location", opp.get("l"))},
                )
            )

        recommended_opps.sort(key=lambda x: x.match_percentage, reverse=True)

        # 3. Rank Alumni
        recommended_alumni: List[RecommendedItem] = []
        for alm in DEMO_ALUMNI:
            alm_skills = {s.lower().strip() for s in alm.get("skills", [])}
            matched_skills = student_skills.intersection(alm_skills)

            score = 45
            reasons = []

            alm_dept = alm.get("department", alm.get("d", ""))
            alm_role = alm.get("current_role", alm.get("r", "Alumnus"))
            alm_name = alm.get("full_name", alm.get("n", "Alumni"))
            alm_company = alm.get("current_company", alm.get("c", "Tech"))
            alm_year = alm.get("graduation_year", alm.get("y", 2020))

            if alm_dept.lower() == profile.department.lower():
                score += 20
                reasons.append(f"Fellow senior from your department ({alm_dept}).")

            if matched_skills:
                score += min(20, len(matched_skills) * 10)
                reasons.append(f"Experienced in technologies you practice ({', '.join([s.capitalize() for s in matched_skills])}).")

            if alm.get("is_available_for_mentorship"):
                score += 10
                reasons.append("Actively offering 1-on-1 mentorship and resume reviews.")

            if goal_text and any(w in alm_role.lower() for w in goal_text.split() if len(w) > 3):
                score += 15
                reasons.append(f"Currently working as {alm_role}, your target career path.")

            score = min(98, max(50, score))
            if not reasons:
                reasons.append("Valuable alumni contact with industry expertise.")

            recommended_alumni.append(
                RecommendedItem(
                    item_id=alm.get("id", alm.get("user_id", "")),
                    title=alm_name,
                    subtitle=f"{alm_role} at {alm_company}",
                    category="Alumni",
                    match_percentage=score,
                    match_reasons=reasons,
                    metadata={
                        "graduation_year": alm_year,
                        "company": alm_company,
                        "mentorship": alm.get("is_available_for_mentorship", True),
                    },
                )
            )

        recommended_alumni.sort(key=lambda x: x.match_percentage, reverse=True)

        return PersonalizedRecommendationsResponse(
            student_id=profile.user_id,
            events=recommended_events[:5],
            opportunities=recommended_opps[:5],
            alumni=recommended_alumni[:5],
            generated_at=datetime.now(timezone.utc).isoformat(),
        )
