from typing import List, Set, Tuple, Dict, Any, Optional
from app.schemas.matching import (
    CandidateProfile,
    TeamContext,
    ScoreBreakdown,
    TeammateRecommendation,
    TeamRecommendationResponse,
    TeamMatchmakerMember,
    TeamMatchmakerResponse,
)


class DeterministicMatchingEngine:
    """
    Deterministic 5-Factor Team Matching Engine.
    Implements explainable multi-factor scoring:
      - Skill Complementarity (30%)
      - Interest Compatibility (25%)
      - Event Compatibility (20%)
      - Experience Level (15%)
      - Availability (10%)
    """

    WEIGHT_SKILL = 30.0
    WEIGHT_INTEREST = 25.0
    WEIGHT_EVENT = 20.0
    WEIGHT_EXPERIENCE = 15.0
    WEIGHT_AVAILABILITY = 10.0

    @classmethod
    def evaluate_candidate(
        cls, candidate: CandidateProfile, team: TeamContext
    ) -> TeammateRecommendation:
        reasons: List[str] = []

        # 1. Skill Complementarity (30%)
        cand_skills_lower = {s.lower().strip() for s in candidate.skills}
        team_needed_lower = {s.lower().strip() for s in team.needed_skills}
        current_skills_lower = {s.lower().strip() for s in team.current_member_skills}

        unfilled_skills = team_needed_lower - current_skills_lower
        target_skills = unfilled_skills if unfilled_skills else team_needed_lower

        matched_skills_set = cand_skills_lower.intersection(target_skills)
        cand_roles_lower = {r.lower().strip() for r in candidate.preferred_roles}
        needed_roles_lower = {r.lower().strip() for r in team.needed_roles}
        matched_roles = cand_roles_lower.intersection(needed_roles_lower)

        if target_skills:
            skill_ratio = len(matched_skills_set) / len(target_skills)
            if matched_roles:
                skill_ratio = min(1.0, skill_ratio + 0.2)
        elif team_needed_lower:
            skill_ratio = len(cand_skills_lower.intersection(team_needed_lower)) / len(team_needed_lower)
        else:
            skill_ratio = 0.5

        skill_score = round(min(cls.WEIGHT_SKILL, skill_ratio * cls.WEIGHT_SKILL), 1)

        matched_skills_display = [
            s for s in candidate.skills if s.lower().strip() in (matched_skills_set or cand_skills_lower)
        ]

        if matched_skills_set:
            skills_str = ", ".join(list(matched_skills_set)[:3])
            reasons.append(f"Provides critical needed skills ({skills_str}) that complement your team.")
        if matched_roles:
            roles_str = ", ".join(list(matched_roles)[:2])
            reasons.append(f"Matches desired team role: {roles_str}.")

        # 2. Interest Compatibility (25%)
        cand_interest_tokens = {w for i in candidate.interests for w in i.lower().split() if len(w) > 2}
        team_domain_tokens = set()
        if team.event_title:
            team_domain_tokens.update([w for w in team.event_title.lower().split() if len(w) > 2])
        if team.event_category:
            team_domain_tokens.add(team.event_category.lower())

        domain_set = team_domain_tokens if team_domain_tokens else {w for s in team_needed_lower for w in s.split() if len(w) > 2}

        if domain_set and cand_interest_tokens:
            intersection = cand_interest_tokens.intersection(domain_set)
            ratio = len(intersection) / max(1, len(domain_set))
            interest_ratio = min(1.0, ratio * 1.5)
            interest_tokens_matched = list(intersection)
        else:
            interest_ratio = 0.5 if candidate.interests else 0.2
            interest_tokens_matched = []

        interest_score = round(min(cls.WEIGHT_INTEREST, interest_ratio * cls.WEIGHT_INTEREST), 1)

        if interest_tokens_matched:
            reasons.append(
                f"Shares common interests ({', '.join(interest_tokens_matched[:2])}) aligned with the event."
            )

        # 3. Event Compatibility (20%)
        if team.event_id and team.event_id in candidate.registered_event_ids:
            event_score = cls.WEIGHT_EVENT
            reasons.append("Already registered for the same event and actively seeking a squad.")
        elif candidate.registered_event_ids:
            event_score = round(cls.WEIGHT_EVENT * 0.5, 1)
        else:
            event_score = round(cls.WEIGHT_EVENT * 0.25, 1)

        # 4. Experience Level Compatibility (15%)
        target_year = team.target_year_level or 3
        year_diff = abs(candidate.current_year - target_year)
        if year_diff == 0:
            exp_ratio = 1.0
        elif year_diff == 1:
            exp_ratio = 0.75
        elif year_diff == 2:
            exp_ratio = 0.5
        else:
            exp_ratio = 0.25

        exp_score = round(exp_ratio * cls.WEIGHT_EXPERIENCE, 1)
        if year_diff <= 1:
            reasons.append(f"Ideal academic experience fit (Year {candidate.current_year}).")

        # 5. Availability (10%)
        if candidate.is_looking_for_team:
            avail_score = cls.WEIGHT_AVAILABILITY
            reasons.append("Profile is currently marked as 'Looking for Team'.")
        else:
            avail_score = round(cls.WEIGHT_AVAILABILITY * 0.3, 1)

        total_score = int(round(skill_score + interest_score + event_score + exp_score + avail_score))
        total_score = max(0, min(100, total_score))

        if len(reasons) < 2:
            reasons.append("High profile alignment with target team criteria.")

        return TeammateRecommendation(
            user_id=candidate.user_id,
            full_name=candidate.full_name,
            department=candidate.department,
            current_year=candidate.current_year,
            matched_skills=matched_skills_display[:5],
            preferred_roles=candidate.preferred_roles,
            total_score=total_score,
            breakdown=ScoreBreakdown(
                skill_complementarity=skill_score,
                interest_compatibility=interest_score,
                event_compatibility=event_score,
                experience=exp_score,
                availability=avail_score,
            ),
            reasons=reasons,
        )

    @classmethod
    def rank_candidates(
        cls, team: TeamContext, candidates: List[CandidateProfile], top_k: int = 10
    ) -> TeamRecommendationResponse:
        evaluated: List[TeammateRecommendation] = []
        for cand in candidates:
            evaluated.append(cls.evaluate_candidate(cand, team))

        evaluated.sort(key=lambda r: r.total_score, reverse=True)

        return TeamRecommendationResponse(
            team_id=team.team_id,
            recommendations=evaluated[:top_k],
            total_evaluated=len(candidates),
        )

    @classmethod
    def matchmaker_rank(
        cls,
        user_skills: List[str],
        user_interests: List[str],
        user_dept: Optional[str],
        needed_skills: List[str],
        needed_interests: List[str],
        candidates: List[Dict[str, Any]],
    ) -> List[TeamMatchmakerMember]:
        """
        Rank candidates directly for the frontend Matchmaker view.
        Calculates exact match score, top-match glow, and reasons.
        """
        W = [w.lower().strip() for w in needed_skills + needed_interests if w.strip()]
        M = [m.lower().strip() for m in user_skills + user_interests if m.strip()]
        dp = (user_dept or "").lower().strip()

        def match_tokens(target_tokens: List[str], cand_tokens: List[str]) -> List[str]:
            matched = []
            for t in target_tokens:
                for c in cand_tokens:
                    if t == c or (len(t) > 2 and t in c) or (len(c) > 2 and c in t):
                        matched.append(t)
                        break
            return matched

        results: List[TeamMatchmakerMember] = []

        for cand in candidates:
            c_skills = cand.get("s", cand.get("skills", []))
            c_interests = cand.get("i", cand.get("interests", []))
            cand_tokens = [tok.lower().strip() for tok in (c_skills + c_interests)]
            
            matched_needed = match_tokens(W, cand_tokens)
            matched_shared = match_tokens(M, cand_tokens)

            cov = len(matched_needed) / max(1, len(W)) if W else 0
            sim = len(matched_shared) / max(1, min(len(M), len(cand_tokens))) if M else 0
            
            dept_bonus = 10 if dp and cand.get("d", "").lower().strip() == dp else 0

            if W:
                score = round(70 * cov + 20 * sim + dept_bonus)
            else:
                score = round(90 * sim + dept_bonus)

            score = max(0, min(99, score))

            reasons: List[str] = []
            if matched_needed:
                reasons.append(f"Possesses desired skills/interests: {', '.join([m.capitalize() for m in matched_needed[:3]])}")
            if matched_shared:
                reasons.append(f"Shares your background in {', '.join([m.capitalize() for m in matched_shared[:2]])}")
            if dept_bonus:
                reasons.append(f"From the same department: {cand.get('d')}")
            if not reasons:
                reasons.append("Compatible talent profile for collaborative projects.")

            results.append(
                TeamMatchmakerMember(
                    id=cand.get("id", cand.get("user_id", "")),
                    n=cand.get("n", cand.get("full_name", "")),
                    g=cand.get("g", cand.get("gender", "m")),
                    d=cand.get("d", cand.get("department", "")),
                    s=c_skills,
                    i=c_interests,
                    p=score,
                    is_top_match=(score >= 70),
                    reasons=reasons,
                )
            )

        # Sort descending by score
        results.sort(key=lambda x: x.p, reverse=True)
        return results
