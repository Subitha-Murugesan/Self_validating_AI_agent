import subprocess
import sys
import os

# Function to install dependencies from requirements.txt
def install_requirements():
    try:
        # Check if requirements.txt exists
        if os.path.exists(r'requirements.txt'):
            print("Installing dependencies from requirements.txt...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        else:
            print("requirements.txt not found. Please make sure it exists.")
    except Exception as error:
        print(f"Error during initialization: {error}")
        raise