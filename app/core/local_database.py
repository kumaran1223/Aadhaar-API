"""
Local SQLite database implementation as fallback
This allows the application to work immediately without Supabase setup
"""

import sqlite3
import os
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class LocalDatabase:
    def __init__(self, db_path: str = "aadhaar_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the local SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create the aadhaar_forms table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS aadhaar_forms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vid TEXT,
                    aadhaar_number TEXT NOT NULL UNIQUE,
                    name_tamil TEXT,
                    name TEXT NOT NULL,
                    guardian_name TEXT,
                    dob TEXT,
                    gender TEXT,
                    address TEXT,
                    vtc TEXT,
                    po TEXT,
                    sub_district TEXT,
                    district TEXT,
                    state TEXT,
                    pincode TEXT,
                    phone TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_aadhaar_number ON aadhaar_forms(aadhaar_number)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_vid ON aadhaar_forms(vid)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON aadhaar_forms(created_at)")
            
            conn.commit()
            conn.close()
            logger.info("Local SQLite database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing local database: {e}")
            raise
    
    def create_record(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record in the local database"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            cursor = conn.cursor()
            
            # Prepare the data
            fields = [
                'vid', 'aadhaar_number', 'name_tamil', 'name', 'guardian_name',
                'dob', 'gender', 'address', 'vtc', 'po', 'sub_district',
                'district', 'state', 'pincode', 'phone'
            ]
            
            values = [data.get(field) for field in fields]
            placeholders = ', '.join(['?' for _ in fields])
            field_names = ', '.join(fields)
            
            # Insert the record
            cursor.execute(f"""
                INSERT INTO aadhaar_forms ({field_names}, created_at, updated_at)
                VALUES ({placeholders}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """, values)
            
            # Get the inserted record
            record_id = cursor.lastrowid
            cursor.execute("SELECT * FROM aadhaar_forms WHERE id = ?", (record_id,))
            record = dict(cursor.fetchone())
            
            conn.commit()
            conn.close()
            
            logger.info(f"Created local record for Aadhaar: {data.get('aadhaar_number')}")
            return record
            
        except sqlite3.IntegrityError as e:
            logger.error(f"Integrity error creating record: {e}")
            raise ValueError("Aadhaar number already exists")
        except Exception as e:
            logger.error(f"Error creating local record: {e}")
            raise
    
    def get_by_aadhaar_number(self, aadhaar_number: str) -> Optional[Dict[str, Any]]:
        """Get a record by Aadhaar number"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM aadhaar_forms WHERE aadhaar_number = ?", (aadhaar_number,))
            record = cursor.fetchone()
            
            conn.close()
            
            if record:
                return dict(record)
            return None
            
        except Exception as e:
            logger.error(f"Error retrieving record: {e}")
            raise
    
    def update_record(self, aadhaar_number: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing record"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Build update query
            fields = [f"{key} = ?" for key in data.keys() if key != 'aadhaar_number']
            values = [value for key, value in data.items() if key != 'aadhaar_number']
            values.append(aadhaar_number)
            
            if not fields:
                return None
            
            query = f"""
                UPDATE aadhaar_forms 
                SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP
                WHERE aadhaar_number = ?
            """
            
            cursor.execute(query, values)
            
            if cursor.rowcount > 0:
                # Get the updated record
                cursor.execute("SELECT * FROM aadhaar_forms WHERE aadhaar_number = ?", (aadhaar_number,))
                record = dict(cursor.fetchone())
                conn.commit()
                conn.close()
                return record
            
            conn.close()
            return None
            
        except Exception as e:
            logger.error(f"Error updating record: {e}")
            raise
    
    def list_records(self, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """List all records with pagination"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM aadhaar_forms 
                ORDER BY created_at DESC 
                LIMIT ? OFFSET ?
            """, (limit, offset))
            
            records = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return records
            
        except Exception as e:
            logger.error(f"Error listing records: {e}")
            raise
    
    def delete_record(self, aadhaar_number: str) -> bool:
        """Delete a record by Aadhaar number"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM aadhaar_forms WHERE aadhaar_number = ?", (aadhaar_number,))
            deleted = cursor.rowcount > 0
            
            conn.commit()
            conn.close()
            
            return deleted
            
        except Exception as e:
            logger.error(f"Error deleting record: {e}")
            raise

# Global instance
local_db = LocalDatabase()

def get_local_database() -> LocalDatabase:
    """Get the local database instance"""
    return local_db
