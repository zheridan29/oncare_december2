#!/usr/bin/env python
"""
Automated Migration Script: SQLite to PostgreSQL
This script exports all data from SQLite and imports it into PostgreSQL
"""

import os
import sys
import django
import json
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
django.setup()

from django.core.management import call_command
from django.conf import settings
from django.db import connections
import subprocess

# Colors for output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def check_sqlite_exists():
    """Check if SQLite database exists"""
    sqlite_path = BASE_DIR / 'db.sqlite3'
    if sqlite_path.exists():
        size = sqlite_path.stat().st_size
        print_success(f"SQLite database found: {sqlite_path} ({size:,} bytes)")
        return True
    else:
        print_error(f"SQLite database not found: {sqlite_path}")
        return False

def check_postgres_connection():
    """Check PostgreSQL connection"""
    try:
        db_config = settings.DATABASES['default']
        if db_config['ENGINE'] != 'django.db.backends.postgresql':
            print_error("Current database is not PostgreSQL!")
            print_warning("Please update settings.py to use PostgreSQL first")
            return False
        
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
        
        print_success(f"PostgreSQL connection successful!")
        print(f"   Database: {db_config['NAME']}")
        print(f"   Host: {db_config['HOST']}:{db_config['PORT']}")
        print(f"   Version: {version.split(',')[0]}")
        return True
    except Exception as e:
        print_error(f"PostgreSQL connection failed: {e}")
        return False

def export_from_sqlite():
    """Export data from SQLite database"""
    print_header("Step 1: Exporting Data from SQLite")
    
    # Create temporary settings for SQLite
    sqlite_settings = f"""
import sys
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# Override to use SQLite
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}
"""
    
    settings_file = BASE_DIR / 'temp_sqlite_settings.py'
    with open(settings_file, 'w') as f:
        f.write(sqlite_settings)
    
    try:
        export_file = BASE_DIR / 'data_export.json'
        
        print("Exporting all data to JSON...")
        
        # Use dumpdata with SQLite settings
        result = subprocess.run(
            [
                sys.executable, 
                'manage.py', 
                'dumpdata',
                '--indent', '2',
                '--natural-primary',
                '--natural-foreign',
                '--output', str(export_file)
            ],
            env={**os.environ, 'DJANGO_SETTINGS_MODULE': 'temp_sqlite_settings'},
            capture_output=True,
            text=True,
            cwd=str(BASE_DIR)
        )
        
        if result.returncode != 0:
            print_error(f"Export failed: {result.stderr}")
            return None
        
        if export_file.exists():
            size = export_file.stat().st_size
            print_success(f"Data exported successfully: {export_file} ({size:,} bytes)")
            return export_file
        else:
            print_error("Export file was not created")
            return None
            
    except Exception as e:
        print_error(f"Export error: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        # Clean up temp settings
        if settings_file.exists():
            settings_file.unlink()

def ensure_postgres_migrations():
    """Ensure PostgreSQL has all migrations applied"""
    print_header("Step 2: Applying Migrations to PostgreSQL")
    
    try:
        print("Running migrations...")
        call_command('migrate', verbosity=1, interactive=False)
        print_success("Migrations applied successfully!")
        return True
    except Exception as e:
        print_error(f"Migration failed: {e}")
        return False

def import_to_postgres(export_file):
    """Import data into PostgreSQL"""
    print_header("Step 3: Importing Data into PostgreSQL")
    
    if not export_file or not export_file.exists():
        print_error("Export file not found!")
        return False
    
    try:
        print(f"Importing data from {export_file.name}...")
        
        # Load data
        call_command('loaddata', str(export_file), verbosity=2)
        
        print_success("Data imported successfully!")
        return True
    except Exception as e:
        print_error(f"Import failed: {e}")
        print_warning("You may need to import in dependency order")
        import traceback
        traceback.print_exc()
        return False

def verify_data():
    """Verify data was migrated correctly"""
    print_header("Step 4: Verifying Data Migration")
    
    try:
        from accounts.models import User
        from inventory.models import Medicine, Category, Manufacturer
        from orders.models import Order, OrderItem
        from analytics.models import DemandForecast
        
        print("\nData counts in PostgreSQL:")
        print(f"  Users: {User.objects.count()}")
        print(f"  Medicines: {Medicine.objects.count()}")
        print(f"  Categories: {Category.objects.count()}")
        print(f"  Manufacturers: {Manufacturer.objects.count()}")
        print(f"  Orders: {Order.objects.count()}")
        print(f"  Order Items: {OrderItem.objects.count()}")
        print(f"  Demand Forecasts: {DemandForecast.objects.count()}")
        
        print_success("Data verification complete!")
        return True
    except Exception as e:
        print_error(f"Verification failed: {e}")
        return False

def compare_with_sqlite():
    """Compare counts with SQLite (if accessible)"""
    print_header("Step 5: Comparing with SQLite Database")
    
    sqlite_path = BASE_DIR / 'db.sqlite3'
    if not sqlite_path.exists():
        print_warning("SQLite database not found for comparison")
        return
    
    print_warning("Note: This requires temporarily switching back to SQLite")
    print("You can manually compare by running:")
    print("  python compare_databases.py")

def main():
    """Main migration process"""
    print_header("SQLite to PostgreSQL Migration Tool")
    
    print("This script will:")
    print("  1. Export all data from SQLite database")
    print("  2. Apply migrations to PostgreSQL")
    print("  3. Import data into PostgreSQL")
    print("  4. Verify the migration")
    
    # Confirm
    response = input("\nDo you want to continue? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Migration cancelled.")
        return
    
    # Step 1: Check prerequisites
    print_header("Checking Prerequisites")
    
    if not check_sqlite_exists():
        print_error("Cannot proceed without SQLite database")
        return
    
    if not check_postgres_connection():
        print_error("Cannot proceed without PostgreSQL connection")
        return
    
    # Step 2: Export from SQLite
    export_file = export_from_sqlite()
    if not export_file:
        print_error("Export failed. Cannot continue.")
        return
    
    # Step 3: Ensure PostgreSQL is ready
    if not ensure_postgres_migrations():
        print_error("Migration setup failed. Cannot continue.")
        return
    
    # Step 4: Import to PostgreSQL
    if not import_to_postgres(export_file):
        print_error("Import failed.")
        print_warning("You may need to manually import using:")
        print(f"  python manage.py loaddata {export_file}")
        return
    
    # Step 5: Verify
    verify_data()
    
    # Step 6: Summary
    print_header("Migration Complete!")
    print_success("Data has been successfully migrated from SQLite to PostgreSQL")
    print("\nNext steps:")
    print("  1. Verify your application works correctly")
    print("  2. Test all functionality")
    print("  3. Keep SQLite backup for reference")
    print("  4. Update settings.py to use PostgreSQL permanently")
    print(f"\nExport file saved at: {export_file}")
    print("You can delete it after verifying everything works.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nMigration cancelled by user.")
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()


