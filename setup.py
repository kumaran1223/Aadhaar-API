#!/usr/bin/env python3
"""
Setup script for Aadhaar OCR API
This script helps set up the development environment and run the application.
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_tesseract():
    """Check if Tesseract OCR is installed"""
    try:
        result = subprocess.run(['tesseract', '--version'], capture_output=True, text=True)
        print("✅ Tesseract OCR is installed")
        return True
    except FileNotFoundError:
        print("❌ Tesseract OCR is not installed")
        print("Please install Tesseract OCR:")
        if platform.system() == "Windows":
            print("  - Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        elif platform.system() == "Darwin":  # macOS
            print("  - Run: brew install tesseract")
        else:  # Linux
            print("  - Run: sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-tam")
        return False

def install_dependencies():
    """Install Python dependencies"""
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    )

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("\n📝 Creating .env file...")
        try:
            with open('.env.example', 'r') as example:
                content = example.read()
            with open('.env', 'w') as env_file:
                env_file.write(content)
            print("✅ .env file created from .env.example")
            print("⚠️  Please update .env with your Supabase credentials")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
        return True

def setup_database():
    """Display database setup instructions"""
    print("\n🗄️  Database Setup Instructions:")
    print("1. Create a Supabase account at https://supabase.com")
    print("2. Create a new project")
    print("3. Go to Settings > API to get your URL and anon key")
    print("4. Update the .env file with your credentials")
    print("5. Run the SQL commands from app/core/init_db.py in your Supabase SQL editor")
    print("   You can run: python -c \"from app.core.init_db import print_sql_commands; print_sql_commands()\"")

def main():
    """Main setup function"""
    print("🚀 Aadhaar OCR API Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_tesseract():
        print("\n⚠️  Tesseract OCR is required for the application to work properly")
        response = input("Continue setup anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create environment file
    if not create_env_file():
        print("❌ Failed to create environment file")
        sys.exit(1)
    
    # Database setup instructions
    setup_database()
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Update .env with your Supabase credentials")
    print("2. Set up the database using the SQL commands")
    print("3. Run the application: python -m uvicorn app.main:app --reload")
    print("4. Visit http://127.0.0.1:8000 to test the application")
    print("5. API documentation: http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    main()
