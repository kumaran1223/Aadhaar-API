#!/usr/bin/env python3
"""
Automated Supabase Database Setup Script
This script will create the required table structure in your Supabase database
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_supabase_credentials():
    """Get Supabase credentials from environment"""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ Supabase credentials not found!")
        print("\nPlease update your .env file with:")
        print("SUPABASE_URL=https://your-project.supabase.co")
        print("SUPABASE_KEY=your-anon-or-service-role-key")
        print("\nYou can find these in your Supabase project settings:")
        print("1. Go to https://supabase.com/dashboard")
        print("2. Select your project")
        print("3. Go to Settings > API")
        print("4. Copy the URL and anon/public key")
        return None, None
    
    return supabase_url, supabase_key

def create_database_table(supabase_url, supabase_key):
    """Create the aadhaar_forms table in Supabase using SQL"""
    
    # SQL to create the table and related objects
    sql_commands = """
-- Create the aadhaar_forms table
CREATE TABLE IF NOT EXISTS aadhaar_forms (
    id SERIAL PRIMARY KEY,
    vid VARCHAR(20),
    aadhaar_number VARCHAR(15) NOT NULL UNIQUE,
    name_tamil TEXT,
    name VARCHAR(255) NOT NULL,
    guardian_name VARCHAR(255),
    dob VARCHAR(20),
    gender VARCHAR(20),
    address TEXT,
    vtc VARCHAR(255),
    po VARCHAR(255),
    sub_district VARCHAR(255),
    district VARCHAR(255),
    state VARCHAR(255),
    pincode VARCHAR(10),
    phone VARCHAR(15),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_aadhaar_forms_aadhaar_number ON aadhaar_forms(aadhaar_number);
CREATE INDEX IF NOT EXISTS idx_aadhaar_forms_vid ON aadhaar_forms(vid);
CREATE INDEX IF NOT EXISTS idx_aadhaar_forms_created_at ON aadhaar_forms(created_at);

-- Create a function to automatically update the updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create a trigger to automatically update the updated_at column
DROP TRIGGER IF EXISTS update_aadhaar_forms_updated_at ON aadhaar_forms;
CREATE TRIGGER update_aadhaar_forms_updated_at
    BEFORE UPDATE ON aadhaar_forms
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
"""
    
    print("🔄 Creating database table in Supabase...")
    
    # Method 1: Try using the SQL endpoint
    try:
        headers = {
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}',
            'Content-Type': 'application/json'
        }
        
        # Use the REST API to execute SQL
        sql_url = f"{supabase_url}/rest/v1/rpc/exec_sql"
        
        response = requests.post(
            sql_url,
            headers=headers,
            json={'sql': sql_commands},
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            print("✅ Database table created successfully using REST API!")
            return True
        else:
            print(f"⚠️  REST API method failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"⚠️  REST API method failed: {e}")
    
    # Method 2: Try using Supabase client
    try:
        from supabase import create_client
        
        print("🔄 Trying Supabase client method...")
        supabase = create_client(supabase_url, supabase_key)
        
        # Execute SQL using RPC
        result = supabase.rpc('exec_sql', {'sql': sql_commands}).execute()
        print("✅ Database table created successfully using Supabase client!")
        return True
        
    except Exception as e:
        print(f"⚠️  Supabase client method failed: {e}")
    
    # Method 3: Manual instructions
    print("\n📋 Manual Setup Required")
    print("=" * 50)
    print("Please copy and paste the following SQL commands into your Supabase SQL editor:")
    print("\n1. Go to https://supabase.com/dashboard")
    print("2. Select your project")
    print("3. Go to 'SQL Editor' in the left sidebar")
    print("4. Create a new query and paste this SQL:")
    print("\n" + "="*60)
    print(sql_commands)
    print("="*60)
    print("\n5. Click 'Run' to execute the SQL")
    print("\nAfter running the SQL, your database will be ready!")
    
    return False

def test_database_connection(supabase_url, supabase_key):
    """Test if the database table was created successfully"""
    try:
        from supabase import create_client
        
        print("🧪 Testing database connection...")
        supabase = create_client(supabase_url, supabase_key)
        
        # Try to query the table
        result = supabase.table('aadhaar_forms').select("count", count="exact").execute()
        print(f"✅ Database connection successful! Table exists and is accessible.")
        print(f"📊 Current record count: {len(result.data)}")
        return True
        
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def migrate_local_data_to_supabase(supabase_url, supabase_key):
    """Migrate existing local data to Supabase"""
    try:
        print("\n🔄 Migrating local data to Supabase...")
        
        # Import local database
        import sqlite3
        from supabase import create_client
        
        # Connect to local database
        local_conn = sqlite3.connect('aadhaar_data.db')
        local_conn.row_factory = sqlite3.Row
        local_cursor = local_conn.cursor()
        
        # Get all records from local database
        local_cursor.execute("SELECT * FROM aadhaar_forms")
        local_records = local_cursor.fetchall()
        
        if not local_records:
            print("📭 No local data to migrate.")
            local_conn.close()
            return True
        
        # Connect to Supabase
        supabase = create_client(supabase_url, supabase_key)
        
        migrated_count = 0
        skipped_count = 0
        
        for record in local_records:
            try:
                # Convert record to dict and remove id (let Supabase auto-generate)
                data = dict(record)
                data.pop('id', None)  # Remove local ID
                
                # Insert into Supabase
                result = supabase.table('aadhaar_forms').insert(data).execute()
                
                if result.data:
                    migrated_count += 1
                    print(f"✅ Migrated: {data.get('aadhaar_number', 'Unknown')}")
                else:
                    skipped_count += 1
                    print(f"⚠️  Skipped: {data.get('aadhaar_number', 'Unknown')} (may already exist)")
                    
            except Exception as e:
                skipped_count += 1
                aadhaar_num = dict(record).get('aadhaar_number', 'Unknown')
                print(f"⚠️  Skipped: {aadhaar_num} - {str(e)}")
        
        local_conn.close()
        
        print(f"\n📊 Migration Summary:")
        print(f"✅ Migrated: {migrated_count} records")
        print(f"⚠️  Skipped: {skipped_count} records")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Supabase Database Setup for Aadhaar OCR API")
    print("=" * 60)
    
    # Get credentials
    supabase_url, supabase_key = get_supabase_credentials()
    if not supabase_url or not supabase_key:
        return
    
    print(f"🔗 Connecting to: {supabase_url}")
    
    # Create database table
    table_created = create_database_table(supabase_url, supabase_key)
    
    if table_created:
        # Test connection
        if test_database_connection(supabase_url, supabase_key):
            
            # Ask about data migration
            if os.path.exists('aadhaar_data.db'):
                print("\n📊 Local database found with existing data.")
                migrate = input("Do you want to migrate local data to Supabase? (y/N): ").strip().lower()
                
                if migrate == 'y':
                    migrate_local_data_to_supabase(supabase_url, supabase_key)
            
            print("\n🎉 Supabase database setup completed successfully!")
            print("\n📋 Next steps:")
            print("1. Restart your application: python run.py dev")
            print("2. Your app will now use Supabase for data storage")
            print("3. Test by uploading a new Aadhaar document")
            print("4. Data will be stored in the cloud!")
            
        else:
            print("\n⚠️  Table created but connection test failed.")
            print("Please check your Supabase project settings.")
    
    else:
        print("\n⚠️  Automatic setup failed. Please use the manual SQL method shown above.")

if __name__ == "__main__":
    main()
