#!/usr/bin/env python3
"""
Run script for Aadhaar OCR API
This script provides easy commands to run the application in different modes.
"""

import os
import sys
import subprocess
import argparse

def run_development():
    """Run the application in development mode"""
    print("🚀 Starting Aadhaar OCR API in development mode...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")

def run_production():
    """Run the application in production mode"""
    print("🚀 Starting Aadhaar OCR API in production mode...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--workers", "4"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start application: {e}")

def run_docker():
    """Run the application using Docker"""
    print("🐳 Starting Aadhaar OCR API with Docker...")
    try:
        subprocess.run(["docker-compose", "up", "--build"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Docker containers stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Docker containers: {e}")

def show_database_setup():
    """Show database setup instructions"""
    try:
        from app.core.init_db import print_sql_commands
        print_sql_commands()
    except ImportError:
        print("❌ Could not import database setup module")
        print("Make sure you have installed the dependencies: pip install -r requirements.txt")

def check_health():
    """Check if the application is running"""
    import requests
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Application is running: {data}")
        else:
            print(f"⚠️  Application responded with status {response.status_code}")
    except requests.exceptions.RequestException:
        print("❌ Application is not running or not accessible")

def main():
    parser = argparse.ArgumentParser(description="Aadhaar OCR API Runner")
    parser.add_argument(
        "command", 
        choices=["dev", "prod", "docker", "db-setup", "health"],
        help="Command to run"
    )
    
    args = parser.parse_args()
    
    if args.command == "dev":
        run_development()
    elif args.command == "prod":
        run_production()
    elif args.command == "docker":
        run_docker()
    elif args.command == "db-setup":
        show_database_setup()
    elif args.command == "health":
        check_health()

if __name__ == "__main__":
    main()
