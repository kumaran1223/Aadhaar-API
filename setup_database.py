#!/usr/bin/env python3
"""
Automated database setup script for Aadhaar OCR API
This script will automatically create the required table in Supabase
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    """Automatically set up the database table in Supabase"""
    try:
        from supabase import create_client
        
        # Get Supabase credentials
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            print("❌ Supabase credentials not found in .env file")
            print("Please ensure SUPABASE_URL and SUPABASE_KEY are set in your .env file")
            return False
        
        print("🔗 Connecting to Supabase...")
        supabase = create_client(supabase_url, supabase_key)
        
        # SQL to create the table
        create_table_sql = """
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
        
        print("📊 Creating database table and indexes...")
        
        # Execute the SQL using Supabase RPC
        try:
            # Use the SQL execution method
            result = supabase.rpc('exec_sql', {'sql': create_table_sql}).execute()
            print("✅ Database table created successfully!")
            return True
        except Exception as e:
            # If RPC doesn't work, try alternative method
            print(f"⚠️  RPC method failed: {e}")
            print("🔄 Trying alternative method...")
            
            # Try using direct SQL execution
            import requests
            
            headers = {
                'apikey': supabase_key,
                'Authorization': f'Bearer {supabase_key}',
                'Content-Type': 'application/json'
            }
            
            # Create table using REST API
            response = requests.post(
                f"{supabase_url}/rest/v1/rpc/exec_sql",
                headers=headers,
                json={'sql': create_table_sql}
            )
            
            if response.status_code in [200, 201]:
                print("✅ Database table created successfully!")
                return True
            else:
                print(f"❌ Failed to create table: {response.text}")
                return False
                
    except ImportError:
        print("❌ Supabase library not installed. Installing...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "supabase"], check=True)
        print("✅ Supabase library installed. Please run the script again.")
        return False
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

def test_database_connection():
    """Test if the database table exists and is accessible"""
    try:
        from supabase import create_client
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        supabase = create_client(supabase_url, supabase_key)
        
        # Try to query the table
        result = supabase.table('aadhaar_forms').select("count", count="exact").execute()
        print(f"✅ Database connection successful! Table exists with {len(result.data)} records.")
        return True
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Aadhaar OCR API - Automated Database Setup")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please create a .env file with your Supabase credentials:")
        print("SUPABASE_URL=https://your-project.supabase.co")
        print("SUPABASE_KEY=your-anon-or-service-role-key")
        return
    
    # Set up database
    if setup_database():
        print("\n🧪 Testing database connection...")
        if test_database_connection():
            print("\n🎉 Database setup completed successfully!")
            print("Your Aadhaar OCR API is now ready to use!")
            print("\nNext steps:")
            print("1. Run: python run.py dev")
            print("2. Visit: http://127.0.0.1:8000")
            print("3. Upload an Aadhaar document to test!")
        else:
            print("\n⚠️  Database setup completed but connection test failed.")
            print("The table should still work. Try running the application.")
    else:
        print("\n❌ Database setup failed.")
        print("Please check your Supabase credentials and try again.")

if __name__ == "__main__":
    main()
