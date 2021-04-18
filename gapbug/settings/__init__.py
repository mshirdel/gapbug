import sys

try:
    print("Trying import development.py settings...", file=sys.stderr)
    from .development import *
except ImportError:
    print("Trying import production.py settings...", file=sys.stderr)
    from .production import *
