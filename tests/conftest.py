"""Pytest configuration.

This file ensures the project root is on sys.path so tests can import
application modules (like logic_utils) even when pytest changes the cwd.
"""

import sys
from pathlib import Path

# Add project root to sys.path when running tests.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
