import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Direct import from the main app.py file
from app import create_app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    app.run()
