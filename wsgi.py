"""
WSGI entry point for PythonAnywhere.
PythonAnywhere looks for a variable called `application` in this file.
"""
import sys
import os

# Add your project directory to the sys.path
# PythonAnywhere: replace 'yourusername' with your actual username
project_home = '/home/yourusername/timelapse'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import the Flask app — PythonAnywhere needs it named `application`
from app import app as application  # noqa
