# This file loads the app.py directly to avoid conflict with the app package

import os
import sys
import importlib.util

def load_app_factory():
    """Load the create_app function from app.py"""
    spec = importlib.util.spec_from_file_location(
        "app_module", 
        os.path.join(os.path.dirname(__file__), "app.py")
    )
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    return app_module.create_app

# Export the create_app function
create_app = load_app_factory()
