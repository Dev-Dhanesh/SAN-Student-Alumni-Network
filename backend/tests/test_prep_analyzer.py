import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.prep_analyzer import PrepAnalyzerService


class TestPrepAnalyzerService(unittest.TestCase):
    def test_prep_analyzer_returns_topic_distribution(self):
        analytics = PrepAnalyzerService.analyze_company_experiences(
            company_name="Zoho Corporation", role="Software Developer"
        )

        self.assertEqual(analytics.company, "Zoho Corporation")
        self.assertGreaterEqual(analytics.total_experiences_analyzed, 1)
        self.assertGreater(len(analytics.topics), 0)
        
        for topic in analytics.topics:
            self.assertTrue(0.0 <= topic.frequency_percentage <= 100.0)
            self.assertIn(topic.focus_level, ["Crucial", "High", "Moderate"])
            
        self.assertGreater(len(analytics.common_rounds), 0)
        self.assertGreater(len(analytics.top_resources), 0)


if __name__ == "__main__":
    unittest.main()
