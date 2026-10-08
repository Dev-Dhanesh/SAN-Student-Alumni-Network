import unittest
import sys
import os

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.schemas.matching import CandidateProfile, TeamContext
from app.services.matching_service import DeterministicMatchingEngine


class TestDeterministicMatchingEngine(unittest.TestCase):
    def test_matching_engine_evaluates_candidate_within_bounds(self):
        candidate = CandidateProfile(
            user_id="test_cand_1",
            full_name="Test Student",
            department="Computer Science",
            current_year=3,
            skills=["React", "TypeScript", "Tailwind CSS"],
            interests=["Healthcare Hackathons", "Web Development"],
            preferred_roles=["Frontend Developer"],
            registered_event_ids=["evt_hack_101"],
            is_looking_for_team=True,
        )

        team = TeamContext(
            team_id="team_01",
            event_id="evt_hack_101",
            event_title="Smart Healthcare Hackathon",
            event_category="hackathon",
            needed_roles=["Frontend Developer", "UI/UX Designer"],
            needed_skills=["React", "Tailwind CSS"],
            current_member_skills=["Python", "FastAPI"],
            target_year_level=3,
        )

        result = DeterministicMatchingEngine.evaluate_candidate(candidate, team)

        self.assertTrue(0 <= result.total_score <= 100)
        self.assertGreaterEqual(result.total_score, 80)
        self.assertLessEqual(result.breakdown.skill_complementarity, 30.0)
        self.assertLessEqual(result.breakdown.interest_compatibility, 25.0)
        self.assertLessEqual(result.breakdown.event_compatibility, 20.0)
        self.assertLessEqual(result.breakdown.experience, 15.0)
        self.assertLessEqual(result.breakdown.availability, 10.0)
        self.assertGreaterEqual(len(result.reasons), 2)
        
        reason_text = " ".join(result.reasons).lower()
        self.assertTrue("event" in reason_text or "skill" in reason_text)

    def test_matching_engine_ranks_candidates_descending(self):
        team = TeamContext(
            team_id="team_01",
            event_id="evt_hack_101",
            needed_skills=["React"],
            needed_roles=["Frontend Developer"],
            target_year_level=3,
        )

        strong_candidate = CandidateProfile(
            user_id="c_strong",
            full_name="High Match",
            department="CSE",
            current_year=3,
            skills=["React"],
            registered_event_ids=["evt_hack_101"],
            is_looking_for_team=True,
        )

        weak_candidate = CandidateProfile(
            user_id="c_weak",
            full_name="Low Match",
            department="Mechanical",
            current_year=1,
            skills=["CAD"],
            registered_event_ids=[],
            is_looking_for_team=False,
        )

        ranked = DeterministicMatchingEngine.rank_candidates(team, [weak_candidate, strong_candidate])

        self.assertEqual(len(ranked.recommendations), 2)
        self.assertEqual(ranked.recommendations[0].user_id, "c_strong")
        self.assertGreater(ranked.recommendations[0].total_score, ranked.recommendations[1].total_score)


if __name__ == "__main__":
    unittest.main()
