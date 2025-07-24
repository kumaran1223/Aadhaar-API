#!/usr/bin/env python3
"""
Test Supabase database connection and migrate local data
"""

import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

def test_supabase_connection():
    """Test if Supabase database is working"""
    try:
        from supabase import create_client
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        print("🔗 Testing Supabase connection...")
        supabase = create_client(supabase_url, supabase_key)
        
        # Test table access
        result = supabase.table('aadhaar_forms').select("count", count="exact").execute()
        print("✅ Supabase database connection successful!")
        print(f"📊 Current records in Supabase: {len(result.data)}")
        
        return supabase
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return None

def migrate_local_to_supabase():
    """Migrate local SQLite data to Supabase"""
    try:
        # Test Supabase connection first
        supabase = test_supabase_connection()
        if not supabase:
            return False
        
        # Check if local database exists
        if not os.path.exists('aadhaar_data.db'):
            print("📭 No local database found to migrate.")
            return True
        
        print("\n🔄 Migrating local data to Supabase...")
        
        # Connect to local database
        conn = sqlite3.connect('aadhaar_data.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all records
        cursor.execute("SELECT * FROM aadhaar_forms")
        records = cursor.fetchall()
        
        if not records:
            print("📭 No local data to migrate.")
            conn.close()
            return True
        
        print(f"📊 Found {len(records)} records to migrate...")
        
        migrated = 0
        skipped = 0
        
        for record in records:
            try:
                # Convert to dict and remove local ID
                data = dict(record)
                data.pop('id', None)  # Let Supabase auto-generate ID
                
                # Insert into Supabase
                result = supabase.table('aadhaar_forms').insert(data).execute()
                
                if result.data:
                    migrated += 1
                    print(f"✅ Migrated: {data.get('name', 'Unknown')} ({data.get('aadhaar_number', 'N/A')})")
                else:
                    skipped += 1
                    print(f"⚠️  Skipped: {data.get('name', 'Unknown')} (may already exist)")
                    
            except Exception as e:
                skipped += 1
                name = dict(record).get('name', 'Unknown')
                print(f"⚠️  Skipped: {name} - {str(e)}")
        
        conn.close()
        
        print(f"\n📊 Migration Summary:")
        print(f"✅ Successfully migrated: {migrated} records")
        print(f"⚠️  Skipped: {skipped} records")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def main():
    """Main function"""
    print("🧪 Supabase Database Test & Migration")
    print("=" * 50)
    
    # Test connection
    supabase = test_supabase_connection()
    
    if supabase:
        print("\n🎉 Supabase database is ready!")
        
        # Ask about migration
        if os.path.exists('aadhaar_data.db'):
            print("\n📊 Local database found.")
            migrate = input("Do you want to migrate local data to Supabase? (y/N): ").strip().lower()
            
            if migrate == 'y':
                if migrate_local_to_supabase():
                    print("\n🎉 Migration completed successfully!")
                    print("\n📋 Next steps:")
                    print("1. Restart your application: python run.py dev")
                    print("2. Your app will now use Supabase for storage")
                    print("3. All new uploads will go to Supabase")
                    print("4. Your data is now in the cloud! ☁️")
                else:
                    print("\n❌ Migration failed. Check the errors above.")
            else:
                print("\n✅ Supabase is ready. Your app will use it for new data.")
        else:
            print("\n✅ Supabase is ready for your application!")
            print("All new uploads will be stored in Supabase.")
    
    else:
        print("\n❌ Supabase database is not ready.")
        print("Please make sure you've created the table using the SQL commands.")
        print("Run: python create_supabase_database.py for instructions.")

if __name__ == "__main__":
    main()
