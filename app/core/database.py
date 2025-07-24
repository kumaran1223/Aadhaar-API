from supabase import create_client, Client
from app.core.config import settings
from app.core.local_database import get_local_database, LocalDatabase
import logging

logger = logging.getLogger(__name__)

class HybridDatabaseClient:
    def __init__(self):
        self.supabase_client: Client = None
        self.local_db: LocalDatabase = get_local_database()
        self.use_supabase = False
        self.connect()

    def connect(self):
        """Initialize database connections - try Supabase first, fallback to local"""
        # Try Supabase first
        if settings.supabase_url and settings.supabase_key:
            try:
                self.supabase_client = create_client(settings.supabase_url, settings.supabase_key)
                # Test connection
                result = self.supabase_client.table('aadhaar_forms').select("count", count="exact").execute()
                self.use_supabase = True
                logger.info("✅ Successfully connected to Supabase database")
                return
            except Exception as e:
                logger.warning(f"⚠️  Supabase connection failed: {str(e)}")
                logger.info("🔄 Falling back to local SQLite database")

        # Use local database as fallback
        self.use_supabase = False
        logger.info("✅ Using local SQLite database")

    def get_client(self):
        """Get the appropriate database client"""
        if self.use_supabase:
            return self.supabase_client
        return self.local_db

    def is_using_supabase(self) -> bool:
        """Check if currently using Supabase"""
        return self.use_supabase

# Global database client instance
db_client = HybridDatabaseClient()

def get_database():
    """Dependency to get database client"""
    return db_client.get_client()

def get_supabase() -> Client:
    """Dependency to get Supabase client (for backward compatibility)"""
    return db_client.get_client()
