"""Utility module to manage application version."""
import os

def get_version():
    """Read and return the current version from VERSION file."""
    try:
        version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
        with open(version_file, 'r') as f:
            return f.read().strip()
    except Exception:
        return "unknown"

__version__ = get_version()
