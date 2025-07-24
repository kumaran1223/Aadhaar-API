"""
Database initialization script for Supabase.
This script contains the SQL commands to create the required tables.
Run these commands in your Supabase SQL editor.
"""

CREATE_AADHAAR_FORMS_TABLE = """
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

-- Enable Row Level Security (RLS) if needed
-- ALTER TABLE aadhaar_forms ENABLE ROW LEVEL SECURITY;

-- Create a policy for authenticated users (optional)
-- CREATE POLICY "Enable all operations for authenticated users" ON aadhaar_forms
--     FOR ALL USING (auth.role() = 'authenticated');
"""

def print_sql_commands():
    """Print the SQL commands to create the database schema"""
    print("=== Supabase Database Initialization ===")
    print("Copy and paste the following SQL commands into your Supabase SQL editor:")
    print("\n" + "="*60 + "\n")
    print(CREATE_AADHAAR_FORMS_TABLE)
    print("\n" + "="*60 + "\n")
    print("After running these commands, your database will be ready to use with the API.")

if __name__ == "__main__":
    print_sql_commands()
