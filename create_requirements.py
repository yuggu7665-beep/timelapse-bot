#!/usr/bin/env python3
"""
Script to create requirements.txt file on PythonAnywhere
Run this in your timelapse-bot directory on PythonAnywhere
"""

import os

requirements_content = """Flask==3.0.3
python-telegram-bot==21.7
openai==1.52.0
requests==2.32.3
python-dotenv==1.0.1
redis==5.0.7  # optional for future
psycopg2-binary==2.9.10  # optional for future"""

def main():
    # Check if we're in the right directory
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    # Write requirements.txt
    with open('requirements.txt', 'w') as f:
        f.write(requirements_content)
    
    print("✓ Created requirements.txt")
    print("\nNow you can install dependencies:")
    print("  pip install -r requirements.txt")
    
    # Also show what's in the file
    print("\nContents of requirements.txt:")
    print("-" * 40)
    print(requirements_content)
    print("-" * 40)

if __name__ == "__main__":
    main()