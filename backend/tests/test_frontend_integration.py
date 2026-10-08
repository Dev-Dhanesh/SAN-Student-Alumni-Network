import unittest
import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app


class TestFrontendIntegration(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_serve_frontend_index(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("SAN – Student Alumni Network", res.text)
        self.assertIn("Team Matchmaker", res.text)

    def test_list_alumni_endpoint(self):
        res = self.client.get("/api/alumni/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreater(len(data), 0)
        first = data[0]
        self.assertIn("n", first)
        self.assertIn("c", first)
        self.assertIn("s", first)

    def test_list_and_create_opportunities(self):
        res = self.client.get("/api/opportunities/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreater(len(data), 0)

        # Create new opportunity
        payload = {
            "t": "Campus Full-Stack Intern",
            "type": "Internship",
            "o": "Saveetha Labs",
            "l": "Chennai",
            "dl": "2026-12-15",
            "s": ["React", "FastAPI"],
            "d": "Hands-on engineering internship.",
        }
        create_res = self.client.post("/api/opportunities/", json=payload)
        self.assertEqual(create_res.status_code, 201)

    def test_list_and_create_stories(self):
        res = self.client.get("/api/stories/")
        self.assertEqual(res.status_code, 200)
        stories = res.json()
        self.assertGreater(len(stories), 0)

        payload = {
            "t": "How our squad won InnoHack",
            "cat": "Hackathon Update",
            "n": "Dhanesh R.",
            "y": "Computer Science",
            "c": "",
            "b": "We designed an automated hospital triage assistant in 24 hours.",
            "role": "student",
            "g": "m",
        }
        create_res = self.client.post("/api/stories/", json=payload)
        self.assertEqual(create_res.status_code, 201)

    def test_find_teammates_matchmaker(self):
        payload = {
            "user_skills": ["Python", "UI Design"],
            "user_interests": ["AI", "Hackathons"],
            "user_dept": "Computer Science",
            "needed_skills": ["React", "Backend"],
            "needed_interests": ["Web", "Startups"],
        }
        res = self.client.post("/api/matching/find-teammates", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("matches", data)
        self.assertGreater(len(data["matches"]), 0)
        top = data["matches"][0]
        self.assertTrue(0 <= top["p"] <= 100)
        self.assertIn("reasons", top)

    def test_mentorship_request_flow(self):
        payload = {
            "to": "a1",
            "toN": "Priya Nair",
            "from": "Kavya S.",
            "fromE": "kavya.it@saveetha.ac.in",
            "msg": "Would love advice on preparing for cloud developer roles.",
        }
        res = self.client.post("/api/mentorship/request", json=payload)
        self.assertEqual(res.status_code, 201)
        req_id = res.json()["request"]["id"]

        # Respond
        resp_res = self.client.post("/api/mentorship/respond", json={"request_id": req_id, "action": "Accepted"})
        self.assertEqual(resp_res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
