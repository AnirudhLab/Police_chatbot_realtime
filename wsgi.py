import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Use the app_loader to avoid conflicts with the app package
from app_loader import create_app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    app.run()
