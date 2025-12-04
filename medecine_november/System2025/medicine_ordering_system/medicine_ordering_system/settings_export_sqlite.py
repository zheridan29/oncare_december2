"""
Temporary settings file for exporting data from SQLite
Use this when exporting data from SQLite database

Usage: python manage.py dumpdata --settings=settings_export_sqlite ...
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Now import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
import django
django.setup()

from django.conf import settings

# Import all from base settings
from medicine_ordering_system.settings import *

# Override database to use SQLite for export
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

