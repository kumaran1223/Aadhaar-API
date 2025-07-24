from typing import Optional, Dict, Any, Union
from supabase import Client
from app.schemas.aadhaar import AadhaarDataCreate, AadhaarDataUpdate
from app.core.local_database import LocalDatabase
import logging

logger = logging.getLogger(__name__)

class HybridAadhaarCRUD:
    def __init__(self, database_client: Union[Client, LocalDatabase]):
        self.db_client = database_client
        self.table_name = "aadhaar_forms"
        self.is_supabase = isinstance(database_client, Client)
    
    async def create_aadhaar_record(self, aadhaar_data: AadhaarDataCreate) -> Dict[str, Any]:
        """Create a new Aadhaar record"""
        try:
            # Convert Pydantic model to dict
            data_dict = aadhaar_data.model_dump(exclude_unset=True)

            if self.is_supabase:
                # Insert data into Supabase
                result = self.db_client.table(self.table_name).insert(data_dict).execute()

                if result.data:
                    logger.info(f"Successfully created Aadhaar record in Supabase for: {aadhaar_data.aadhaar_number}")
                    return result.data[0]
                else:
                    logger.error(f"Failed to create Aadhaar record: {result}")
                    raise Exception("Failed to insert data into Supabase")
            else:
                # Insert data into local database
                record = self.db_client.create_record(data_dict)
                logger.info(f"Successfully created Aadhaar record in local DB for: {aadhaar_data.aadhaar_number}")
                return record

        except Exception as e:
            logger.error(f"Error creating Aadhaar record: {str(e)}")
            raise
    
    async def get_aadhaar_by_number(self, aadhaar_number: str) -> Optional[Dict[str, Any]]:
        """Retrieve Aadhaar record by Aadhaar number"""
        try:
            if self.is_supabase:
                result = self.db_client.table(self.table_name).select("*").eq("aadhaar_number", aadhaar_number).execute()

                if result.data:
                    logger.info(f"Successfully retrieved Aadhaar record from Supabase for: {aadhaar_number}")
                    return result.data[0]
                else:
                    logger.info(f"No Aadhaar record found in Supabase for: {aadhaar_number}")
                    return None
            else:
                record = self.db_client.get_by_aadhaar_number(aadhaar_number)
                if record:
                    logger.info(f"Successfully retrieved Aadhaar record from local DB for: {aadhaar_number}")
                else:
                    logger.info(f"No Aadhaar record found in local DB for: {aadhaar_number}")
                return record

        except Exception as e:
            logger.error(f"Error retrieving Aadhaar record: {str(e)}")
            raise
    
    async def update_aadhaar_record(self, aadhaar_number: str, aadhaar_data: AadhaarDataUpdate) -> Optional[Dict[str, Any]]:
        """Update an existing Aadhaar record"""
        try:
            # Convert Pydantic model to dict, excluding unset values
            update_data = aadhaar_data.model_dump(exclude_unset=True)

            if not update_data:
                logger.warning("No data provided for update")
                return None

            if self.is_supabase:
                result = self.db_client.table(self.table_name).update(update_data).eq("aadhaar_number", aadhaar_number).execute()

                if result.data:
                    logger.info(f"Successfully updated Aadhaar record in Supabase for: {aadhaar_number}")
                    return result.data[0]
                else:
                    logger.warning(f"No Aadhaar record found to update in Supabase for: {aadhaar_number}")
                    return None
            else:
                record = self.db_client.update_record(aadhaar_number, update_data)
                if record:
                    logger.info(f"Successfully updated Aadhaar record in local DB for: {aadhaar_number}")
                else:
                    logger.warning(f"No Aadhaar record found to update in local DB for: {aadhaar_number}")
                return record

        except Exception as e:
            logger.error(f"Error updating Aadhaar record: {str(e)}")
            raise
    
    async def delete_aadhaar_record(self, aadhaar_number: str) -> bool:
        """Delete an Aadhaar record by Aadhaar number"""
        try:
            if self.is_supabase:
                result = self.db_client.table(self.table_name).delete().eq("aadhaar_number", aadhaar_number).execute()

                if result.data:
                    logger.info(f"Successfully deleted Aadhaar record from Supabase for: {aadhaar_number}")
                    return True
                else:
                    logger.warning(f"No Aadhaar record found to delete in Supabase for: {aadhaar_number}")
                    return False
            else:
                deleted = self.db_client.delete_record(aadhaar_number)
                if deleted:
                    logger.info(f"Successfully deleted Aadhaar record from local DB for: {aadhaar_number}")
                else:
                    logger.warning(f"No Aadhaar record found to delete in local DB for: {aadhaar_number}")
                return deleted

        except Exception as e:
            logger.error(f"Error deleting Aadhaar record: {str(e)}")
            raise

    async def check_aadhaar_exists(self, aadhaar_number: str) -> bool:
        """Check if an Aadhaar record exists"""
        try:
            if self.is_supabase:
                result = self.db_client.table(self.table_name).select("aadhaar_number").eq("aadhaar_number", aadhaar_number).execute()
                return len(result.data) > 0
            else:
                record = self.db_client.get_by_aadhaar_number(aadhaar_number)
                return record is not None
        except Exception as e:
            logger.error(f"Error checking Aadhaar existence: {str(e)}")
            raise

    async def list_all_records(self, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """List all Aadhaar records with pagination"""
        try:
            if self.is_supabase:
                result = self.db_client.table(self.table_name).select("*").range(offset, offset + limit - 1).execute()
                return {
                    "success": True,
                    "data": result.data,
                    "total_count": len(result.data)
                }
            else:
                records = self.db_client.list_records(limit, offset)
                return {
                    "success": True,
                    "data": records,
                    "total_count": len(records)
                }
        except Exception as e:
            logger.error(f"Error listing Aadhaar records: {str(e)}")
            raise

def get_aadhaar_crud(database_client) -> HybridAadhaarCRUD:
    """Factory function to create HybridAadhaarCRUD instance"""
    return HybridAadhaarCRUD(database_client)
