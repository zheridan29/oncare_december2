"""
Simple Working Migration Script
Run: python do_migration.py
"""

import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

print("\n" + "="*60)
print("  SQLite to PostgreSQL Migration")
print("="*60)

# Step 1: Check SQLite exists
sqlite_file = BASE_DIR / 'db.sqlite3'
if not sqlite_file.exists():
    print(f"\n❌ Error: db.sqlite3 not found!")
    sys.exit(1)

print(f"\n✅ Found SQLite database: {sqlite_file.stat().st_size:,} bytes")

# Step 2: Instructions for manual migration
print("\n" + "="*60)
print("  MIGRATION INSTRUCTIONS")
print("="*60)

print("""
Since settings need to be switched, here's the easiest way:

STEP 1: Export from SQLite
---------------------------
1. Temporarily change settings.py to use SQLite:
   
   Comment PostgreSQL section and uncomment SQLite:
   
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }

2. Run this command:
   python manage.py dumpdata --indent 2 --output data_export.json

STEP 2: Switch to PostgreSQL
-----------------------------
1. Change settings.py back to PostgreSQL (current configuration)

2. Run migrations:
   python manage.py migrate

STEP 3: Import Data
--------------------
1. Run this command:
   python manage.py loaddata data_export.json

Done! Your data is now in PostgreSQL.
""")

print("\n" + "="*60)
print("  OR USE THE MANUAL STEPS BELOW")
print("="*60)

# Provide copy-paste commands
print("\n📋 Copy-Paste Commands:")
print("\n1️⃣  First, change settings.py to SQLite, then run:")
print("   python manage.py dumpdata --indent 2 --output data_export.json")
print("\n2️⃣  Change settings.py back to PostgreSQL, then run:")
print("   python manage.py migrate")
print("   python manage.py loaddata data_export.json")
print("\n✅ Done!")

# Offer to check current settings
response = input("\nDo you want me to check your current database settings? (y/n): ")
if response.lower() == 'y':
    try:
        sys.path.insert(0, str(BASE_DIR))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
        import django
        django.setup()
        from django.conf import settings
        
        db = settings.DATABASES['default']
        print(f"\nCurrent database: {db['ENGINE']}")
        if 'sqlite' in db['ENGINE']:
            print("✅ You're using SQLite - ready to export!")
        else:
            print(f"ℹ️  You're using {db['ENGINE']} - switch to SQLite first for export")
    except Exception as e:
        print(f"\n⚠️  Could not check settings: {e}")

print("\n" + "="*60)
print("  Need help? See MIGRATION_STEPS.md")
print("="*60 + "\n")


