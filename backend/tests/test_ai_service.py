import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.schemas.roadmap import RoadmapRequest
from app.schemas.nl_search import NLSearchRequest
from app.services.ai_service import AIService


class TestAIService(unittest.TestCase):
    def test_ai_service_generates_roadmap_with_pattern_fallback(self):
        request = RoadmapRequest(
            career_goal="Full-Stack Web Developer",
            current_year=2,
            department="Computer Science",
            current_skills=["HTML", "CSS", "Basic JavaScript"],
        )

        response = AIService.generate_career_roadmap(request)

        self.assertEqual(response.career_goal, "Full-Stack Web Developer")
        self.assertGreaterEqual(len(response.milestones), 3)
        self.assertEqual(response.milestones[0].step_number, 1)
        self.assertGreater(len(response.milestones[0].key_skills), 0)

    def test_ai_service_parses_natural_language_search(self):
        request = NLSearchRequest(
            query="Find AI hackathons suitable for second-year students"
        )

        response = AIService.parse_natural_language_search(request)

        self.assertEqual(response.filters.entity_type, "event")
        self.assertEqual(response.filters.target_year, 2)
        self.assertIn("AI", response.filters.skills)


if __name__ == "__main__":
    unittest.main()
