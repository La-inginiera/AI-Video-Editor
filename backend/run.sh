#!/bin/bash

# Export Flask app environment variables
export FLASK_APP=main.py
export FLASK_ENV=development

# Optional: Create virtual environment and activate it
# If you are using a virtual environment, uncomment these lines
# source venv/bin/activate  # For Unix/MacOS
# source venv/Scripts/activate  # For Windows

# Run Flask
flask run
