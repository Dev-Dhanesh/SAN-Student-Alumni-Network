import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.schemas.recommendations import StudentProfileContext
from app.services.recommendation_service import RecommendationService


class TestRecommendationService(unittest.TestCase):
    def test_get_recommendations_for_student(self):
        profile = StudentProfileContext(
            user_id="std_999",
            department="Computer Science & Engineering",
            current_year=3,
            skills=["React", "TypeScript", "Python"],
            interests=["Healthcare Tech", "Hackathons"],
            career_goals="Software Engineer at AWS",
            preferred_roles=["Frontend Developer"],
        )

        response = RecommendationService.get_recommendations_for_student(profile)

        self.assertEqual(response.student_id, "std_999")
        self.assertGreater(len(response.events), 0)
        self.assertGreater(len(response.opportunities), 0)
        self.assertGreater(len(response.alumni), 0)

        # Verify items have match scores between 0 and 100 and clear reasons
        for evt in response.events:
            self.assertTrue(0 <= evt.match_percentage <= 100)
            self.assertGreater(len(evt.match_reasons), 0)

        for opp in response.opportunities:
            self.assertTrue(0 <= opp.match_percentage <= 100)
            self.assertGreater(len(opp.match_reasons), 0)

        for alm in response.alumni:
            self.assertTrue(0 <= alm.match_percentage <= 100)
            self.assertGreater(len(alm.match_reasons), 0)


if __name__ == "__main__":
    unittest.main()
