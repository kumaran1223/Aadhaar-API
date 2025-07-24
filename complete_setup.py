#!/usr/bin/env python3
"""
Complete automated setup script for Aadhaar OCR API
This script will set up everything needed to run the application
"""

import os
import sys
import subprocess
import time
from dotenv import load_dotenv

def run_command(command, description, check=True):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"⚠️  {description} completed with warnings")
            if result.stderr:
                print(f"Warning: {result.stderr}")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
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

def install_dependencies():
    """Install Python dependencies"""
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    )

def setup_environment():
    """Set up environment file"""
    if not os.path.exists('.env'):
        print("\n📝 Creating .env file...")
        try:
            with open('.env.example', 'r') as example:
                content = example.read()
            with open('.env', 'w') as env_file:
                env_file.write(content)
            print("✅ .env file created from .env.example")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
    return True

def test_application():
    """Test if the application starts correctly"""
    print("\n🧪 Testing application startup...")
    
    # Start the application in the background
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a few seconds for startup
        time.sleep(5)
        
        # Test health endpoint
        import requests
        try:
            response = requests.get("http://127.0.0.1:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Application started successfully!")
                print("✅ Health check passed!")
                
                # Test main page
                response = requests.get("http://127.0.0.1:8000/", timeout=5)
                if response.status_code == 200:
                    print("✅ Web interface is accessible!")
                
                # Stop the test server
                process.terminate()
                process.wait()
                return True
            else:
                print(f"⚠️  Health check returned status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Could not connect to application: {e}")
        
        # Stop the test server
        process.terminate()
        process.wait()
        return False
        
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        return False

def create_sample_data():
    """Create some sample data for testing"""
    print("\n📊 Setting up sample data...")
    try:
        # Import after dependencies are installed
        from app.core.local_database import get_local_database
        
        db = get_local_database()
        
        # Create a sample record
        sample_data = {
            "aadhaar_number": "1234 5678 9012",
            "name": "Sample User",
            "guardian_name": "Sample Guardian",
            "dob": "01/01/1990",
            "gender": "Male",
            "address": "Sample Address, Sample City",
            "district": "Sample District",
            "state": "Sample State",
            "pincode": "123456",
            "phone": "9876543210"
        }
        
        try:
            db.create_record(sample_data)
            print("✅ Sample data created successfully!")
        except ValueError:
            print("✅ Sample data already exists!")
        
        return True
    except Exception as e:
        print(f"⚠️  Could not create sample data: {e}")
        return True  # Not critical

def main():
    """Main setup function"""
    print("🚀 Aadhaar OCR API - Complete Automated Setup")
    print("=" * 60)
    print("This script will set up everything needed to run the application.")
    print("The application will work with a local SQLite database by default.")
    print("You can optionally configure Supabase later for cloud storage.")
    print("=" * 60)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Set up environment
    if not setup_environment():
        print("❌ Failed to set up environment")
        sys.exit(1)
    
    # Create sample data
    create_sample_data()
    
    # Test application
    if test_application():
        print("\n🎉 Setup completed successfully!")
        print("\n" + "=" * 60)
        print("🎯 Your Aadhaar OCR API is ready to use!")
        print("=" * 60)
        print("\n📋 What's been set up:")
        print("✅ All Python dependencies installed")
        print("✅ Environment configuration created")
        print("✅ Local SQLite database initialized")
        print("✅ Sample data created for testing")
        print("✅ Application tested and working")
        
        print("\n🚀 How to run the application:")
        print("1. Start the server:")
        print("   python run.py dev")
        print("\n2. Open your browser and visit:")
        print("   http://127.0.0.1:8000")
        print("\n3. Test the API documentation:")
        print("   http://127.0.0.1:8000/docs")
        
        print("\n🔍 Test the application:")
        print("• Upload an Aadhaar PDF or image file")
        print("• Search for the sample record: 1234 5678 9012")
        print("• View all records in the list endpoint")
        
        print("\n🌐 Optional: Configure Supabase")
        print("• Update .env with your Supabase credentials")
        print("• Run: python setup_database.py")
        print("• Restart the application")
        
        print("\n" + "=" * 60)
        print("🎉 Enjoy your Aadhaar OCR API!")
        print("=" * 60)
        
    else:
        print("\n⚠️  Setup completed but application test failed.")
        print("You can still try running the application manually:")
        print("python run.py dev")

if __name__ == "__main__":
    main()
