import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.journey_analyzer import JourneyAnalyzerService


class TestJourneyAnalyzerService(unittest.TestCase):
    def test_list_all_journeys(self):
        journeys = JourneyAnalyzerService.list_all_journeys()
        self.assertGreater(len(journeys), 0)
        first = journeys[0]
        self.assertIn(first.current_company, ["Google", "Amazon"])
        self.assertGreater(len(first.stages), 3)
        self.assertIsNotNone(first.mistakes_made)
        self.assertIsNotNone(first.advice_for_juniors)

    def test_get_pattern_analysis(self):
        pattern = JourneyAnalyzerService.get_pattern_analysis("Cloud Engineer")
        self.assertEqual(pattern.target_role_category, "Cloud Engineer")
        self.assertGreater(len(pattern.common_starting_skills), 0)
        self.assertGreater(len(pattern.key_breakthrough_milestones), 0)
        self.assertGreater(len(pattern.frequent_mistakes_to_avoid), 0)


if __name__ == "__main__":
    unittest.main()
