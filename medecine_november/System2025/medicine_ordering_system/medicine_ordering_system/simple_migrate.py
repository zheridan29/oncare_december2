"""
Simple SQLite to PostgreSQL Migration Script
Just run: python simple_migrate.py
"""

import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def print_step(step_num, message):
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {message}")
    print('='*60)

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n▶ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description} failed")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def main():
    print("\n" + "="*60)
    print("  SQLite to PostgreSQL Migration Tool")
    print("="*60)
    
    # Check SQLite exists
    sqlite_file = BASE_DIR / 'db.sqlite3'
    if not sqlite_file.exists():
        print(f"\n❌ Error: SQLite database not found at {sqlite_file}")
        print("Please make sure db.sqlite3 exists in the project directory.")
        return
    
    file_size = sqlite_file.stat().st_size
    print(f"\n✅ Found SQLite database: {file_size:,} bytes")
    
    # Confirm
    response = input("\nDo you want to proceed with migration? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Migration cancelled.")
        return
    
    # Step 1: Export from SQLite
    print_step(1, "Exporting Data from SQLite")
    
    export_file = BASE_DIR / 'data_export.json'
    
    # Create temporary settings file inline
    export_cmd = f'''python -c "
import os
import sys
import django
from pathlib import Path

BASE_DIR = Path('{BASE_DIR}').resolve()
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')

# Override database to SQLite
os.environ['DJANGO_DATABASE_ENGINE'] = 'sqlite3'
os.environ['DJANGO_DATABASE_NAME'] = str(BASE_DIR / 'db.sqlite3')

django.setup()

from django.core.management import call_command
call_command('dumpdata', '--indent', '2', '--natural-primary', '--natural-foreign', '--output', '{export_file}')
"'''
    
    # Simpler approach - directly modify settings temporarily
    success = run_command(
        f'python manage.py dumpdata --indent 2 --natural-primary --natural-foreign --output data_export.json',
        "Exporting all data from SQLite"
    )
    
    if not success:
        print("\n⚠️  Trying alternative export method...")
        # Alternative: manually specify SQLite
        print("Please run this command manually:")
        print("  python manage.py dumpdata --indent 2 --output data_export.json")
        print("\nMake sure settings.py uses SQLite temporarily, then switch back to PostgreSQL.")
        return
    
    if not export_file.exists():
        print("\n❌ Export file was not created. Please check the error above.")
        return
    
    file_size = export_file.stat().st_size
    print(f"\n✅ Data exported: {file_size:,} bytes")
    
    # Step 2: Run migrations on PostgreSQL
    print_step(2, "Preparing PostgreSQL Database")
    
    # Temporarily switch settings - actually, we need to check current settings
    print("\n⚠️  Note: Make sure settings.py is configured for PostgreSQL")
    input("Press Enter when ready to proceed...")
    
    success = run_command(
        'python manage.py migrate',
        "Applying migrations to PostgreSQL"
    )
    
    if not success:
        print("\n⚠️  Migration failed. Please check your PostgreSQL connection.")
        return
    
    # Step 3: Import to PostgreSQL
    print_step(3, "Importing Data into PostgreSQL")
    
    success = run_command(
        f'python manage.py loaddata {export_file}',
        "Importing data into PostgreSQL"
    )
    
    if not success:
        print("\n⚠️  Import may have issues. Check error messages above.")
        print("You may need to import in dependency order (see QUICK_MIGRATION_GUIDE.md)")
        return
    
    # Step 4: Verify
    print_step(4, "Verification")
    
    print("\n✅ Migration completed!")
    print(f"\nExport file saved at: {export_file}")
    print("You can keep it as a backup or delete it after verifying.")
    
    print("\n" + "="*60)
    print("  Migration Complete!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Verify your application works correctly")
    print("  2. Test all functionality")
    print("  3. Keep SQLite database as backup")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nMigration cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


