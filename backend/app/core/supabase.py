from typing import Optional
from supabase import create_client, Client
from app.core.config import settings


_supabase_client: Optional[Client] = None


def get_supabase_client() -> Optional[Client]:
    """
    Returns an initialized Supabase client with the service role key.
    Returns None if credentials are not configured yet, allowing graceful offline mode.
    """
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    if settings.SUPABASE_URL and settings.SUPABASE_SERVICE_ROLE_KEY:
        try:
            _supabase_client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_SERVICE_ROLE_KEY
            )
            return _supabase_client
        except Exception:
            return None
    return None
