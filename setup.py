#!/usr/bin/env python3
"""
Setup script for Disease Detection System
"""

import os
import sys
import subprocess
import platform

def create_directory_structure():
    """Create the required directory structure"""
    directories = [
        'uploads',
        'static/css',
        'static/js',
        'static/images',
        'templates',
        'models',
        'output/reports',
        'output/processed_images',
        'evaluation/test_images',
        'docs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
        
        # Create .gitkeep file in empty directories
        if not os.listdir(directory):
            with open(os.path.join(directory, '.gitkeep'), 'w') as f:
                f.write('')

def install_dependencies():
    """Install Python dependencies"""
    print("\nInstalling Python dependencies...")
    
    if platform.system() == 'Windows':
        python_cmd = 'python'
    else:
        python_cmd = 'python3'
    
    try:
        subprocess.check_call([python_cmd, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.check_call([python_cmd, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        sys.exit(1)

def create_env_file():
    """Create .env file with default configuration"""
    env_content = """# Disease Detection System Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=output/processed_images
REPORT_FOLDER=output/reports
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✓ Created .env file")

def main():
    """Main setup function"""
    print("=" * 50)
    print("Disease Detection System Setup")
    print("=" * 50)
    
    # Create directory structure
    print("\n1. Creating directory structure...")
    create_directory_structure()
    
    # Install dependencies
    print("\n2. Installing dependencies...")
    install_dependencies()
    
    # Create .env file
    print("\n3. Creating configuration file...")
    create_env_file()
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nTo start the application:")
    print("  python app.py")
    print("\nOr with Docker:")
    print("  cd docker")
    print("  docker-compose up")
    print("\nAccess the dashboard at:")
    print("  http://localhost:5000")
    print("=" * 50)

if __name__ == '__main__':
    main()