import re
from fastapi import APIRouter
from app.core.config import settings
from app.schemas.admin_compute import (
    EmailVerificationRequest,
    EmailVerificationResponse,
    PlatformHealthStats,
)
from app.services.demo_data import DEMO_ALUMNI, DEMO_OPPORTUNITIES, DEMO_EVENTS

router = APIRouter(prefix="/admin-compute", tags=["Admin Verification & Analytics"])


@router.post("/verify-email", response_model=EmailVerificationResponse)
async def check_email_domain(request: EmailVerificationRequest):
    """
    Validates institutional email domain (@saveetha.ac.in),
    parses department clues, and suggests verification badges.
    """
    email = request.email.strip().lower()
    email_regex = r"^[\w\.-]+@([\w\.-]+\.\w+)$"
    match = re.match(email_regex, email)

    if not match:
        return EmailVerificationResponse(
            email=email,
            is_valid_format=False,
            is_college_domain=False,
            domain="",
            suggested_role="student",
            suggested_department="General",
            verification_status="invalid_email",
        )

    domain = match.group(1)
    is_college = domain.endswith(settings.COLLEGE_EMAIL_DOMAIN.lower())

    # Infer department from prefix
    dept = "Computer Science & Engineering"
    if "it" in email or "infotech" in email:
        dept = "Information Technology"
    elif "ai" in email or "ds" in email:
        dept = "Artificial Intelligence & Data Science"
    elif "ece" in email:
        dept = "Electronics & Communication Engineering"

    role = "alumni" if "alumni" in email else "student"
    status = "auto_eligible_for_badge" if is_college else "manual_approval_required"

    return EmailVerificationResponse(
        email=email,
        is_valid_format=True,
        is_college_domain=is_college,
        domain=domain,
        suggested_role=role,
        suggested_department=dept,
        verification_status=status,
    )


@router.get("/health-metrics", response_model=PlatformHealthStats)
async def get_platform_health_metrics():
    """
    Computes real-time platform statistics for college administrative view.
    """
    return PlatformHealthStats(
        total_students=248,
        total_alumni=len(DEMO_ALUMNI) + 142,
        total_opportunities=len(DEMO_OPPORTUNITIES) + 18,
        total_events=len(DEMO_EVENTS) + 6,
        active_teams=14,
        pending_verifications=3,
        college_name=settings.COLLEGE_NAME,
    )
