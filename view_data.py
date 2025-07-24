#!/usr/bin/env python3
"""
Script to view all stored Aadhaar data from the local database
"""

import sqlite3
import json
from datetime import datetime

def view_all_data():
    """View all stored Aadhaar data"""
    try:
        # Connect to the database
        conn = sqlite3.connect('aadhaar_data.db')
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        cursor = conn.cursor()
        
        # Get all records
        cursor.execute("SELECT * FROM aadhaar_forms ORDER BY created_at DESC")
        records = cursor.fetchall()
        
        if not records:
            print("📭 No data found in the database.")
            return
        
        print(f"📊 Found {len(records)} record(s) in the database:")
        print("=" * 80)
        
        for i, record in enumerate(records, 1):
            print(f"\n🔍 Record #{i}")
            print("-" * 40)
            
            # Convert to dict for easier handling
            data = dict(record)
            
            # Display key information
            print(f"📋 Aadhaar Number: {data.get('aadhaar_number', 'N/A')}")
            print(f"👤 Name: {data.get('name', 'N/A')}")
            print(f"👨‍👩‍👧‍👦 Guardian: {data.get('guardian_name', 'N/A')}")
            print(f"🎂 DOB: {data.get('dob', 'N/A')}")
            print(f"⚧ Gender: {data.get('gender', 'N/A')}")
            print(f"🏠 Address: {data.get('address', 'N/A')}")
            print(f"🏘️ District: {data.get('district', 'N/A')}")
            print(f"🗺️ State: {data.get('state', 'N/A')}")
            print(f"📮 PIN Code: {data.get('pincode', 'N/A')}")
            print(f"📞 Phone: {data.get('phone', 'N/A')}")
            print(f"🆔 VID: {data.get('vid', 'N/A')}")
            print(f"📅 Created: {data.get('created_at', 'N/A')}")
            print(f"🔄 Updated: {data.get('updated_at', 'N/A')}")
            
            if i < len(records):
                print("\n" + "=" * 80)
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def export_to_json():
    """Export all data to JSON file"""
    try:
        conn = sqlite3.connect('aadhaar_data.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM aadhaar_forms ORDER BY created_at DESC")
        records = cursor.fetchall()
        
        # Convert to list of dictionaries
        data = [dict(record) for record in records]
        
        # Export to JSON file
        filename = f"aadhaar_data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Data exported to: {filename}")
        conn.close()
        
    except Exception as e:
        print(f"❌ Export error: {e}")

def get_database_info():
    """Get database schema and statistics"""
    try:
        conn = sqlite3.connect('aadhaar_data.db')
        cursor = conn.cursor()
        
        # Get table info
        cursor.execute("PRAGMA table_info(aadhaar_forms)")
        columns = cursor.fetchall()
        
        # Get record count
        cursor.execute("SELECT COUNT(*) FROM aadhaar_forms")
        count = cursor.fetchone()[0]
        
        print("🗄️ Database Information:")
        print("-" * 40)
        print(f"📊 Total Records: {count}")
        print(f"📁 Database File: aadhaar_data.db")
        print(f"🏗️ Table: aadhaar_forms")
        print(f"📋 Columns: {len(columns)}")
        
        print("\n📋 Table Schema:")
        for col in columns:
            print(f"  • {col[1]} ({col[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error getting database info: {e}")

def main():
    """Main function"""
    print("🔍 Aadhaar Data Viewer")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. View all stored data")
        print("2. Export data to JSON")
        print("3. Database information")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            view_all_data()
        elif choice == '2':
            export_to_json()
        elif choice == '3':
            get_database_info()
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
