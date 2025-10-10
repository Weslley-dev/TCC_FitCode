"""
WSGI config for TCC_FitCode project.

This file redirects to the correct WSGI module in the app directory.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Import the actual WSGI application
from app.wsgi import application

# This makes the application available at the module level
__all__ = ['application']
