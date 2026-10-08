import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.schemas.admin_compute import EmailVerificationRequest
from app.api.admin_compute import check_email_domain, get_platform_health_metrics
import asyncio


class TestAdminCompute(unittest.TestCase):
    def test_verify_saveetha_college_email(self):
        req = EmailVerificationRequest(email="dhanesh.cse@saveetha.ac.in")
        res = asyncio.run(check_email_domain(req))
        self.assertTrue(res.is_valid_format)
        self.assertTrue(res.is_college_domain)
        self.assertEqual(res.verification_status, "auto_eligible_for_badge")

    def test_verify_external_email(self):
        req = EmailVerificationRequest(email="candidate@gmail.com")
        res = asyncio.run(check_email_domain(req))
        self.assertTrue(res.is_valid_format)
        self.assertFalse(res.is_college_domain)
        self.assertEqual(res.verification_status, "manual_approval_required")

    def test_platform_health_metrics(self):
        stats = asyncio.run(get_platform_health_metrics())
        self.assertGreater(stats.total_students, 0)
        self.assertGreater(stats.total_alumni, 0)
        self.assertGreater(stats.total_opportunities, 0)
        self.assertEqual(stats.college_name, "Saveetha Engineering College")


if __name__ == "__main__":
    unittest.main()
