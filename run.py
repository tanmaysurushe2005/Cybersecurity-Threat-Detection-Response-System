#!/usr/bin/env python
"""
Launcher script for the Cybersecurity Threat Detection System
Properly configures Python path and runs Streamlit
"""
import sys
import os
import subprocess

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Add project directory to Python path
sys.path.insert(0, script_dir)

# Change to project directory
os.chdir(script_dir)

# Run streamlit with proper environment
if __name__ == "__main__":
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        os.path.join(script_dir, "project", "app.py"),
        "--logger.level=error"
    ])

