#!/usr/bin/env python
"""
Database Connection Test Script
Run this to diagnose PostgreSQL connection issues
"""

import sys
import os

# Add project to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

print("=" * 60)
print("OnCare PostgreSQL Connection Diagnostic Tool")
print("=" * 60)
print()

# Test 1: Check if psycopg2 is installed
print("Test 1: Checking psycopg2 package...")
try:
    import psycopg2
    print(f"✅ psycopg2 is installed (version: {psycopg2.__version__})")
except ImportError:
    print("❌ psycopg2 is NOT installed")
    print("   Solution: pip install psycopg2-binary")
    sys.exit(1)

print()

# Test 2: Read Django settings
print("Test 2: Reading database configuration from settings...")
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
    import django
    django.setup()
    
    from django.conf import settings
    db_config = settings.DATABASES['default']
    
    print(f"✅ Settings loaded successfully")
    print(f"   Engine: {db_config['ENGINE']}")
    print(f"   Database: {db_config['NAME']}")
    print(f"   User: {db_config['USER']}")
    print(f"   Host: {db_config['HOST']}")
    print(f"   Port: {db_config['PORT']}")
    print(f"   Password: {'*' * len(str(db_config.get('PASSWORD', '')))}")
except Exception as e:
    print(f"❌ Failed to load settings: {e}")
    sys.exit(1)

print()

# Test 3: Test direct psycopg2 connection
print("Test 3: Testing direct psycopg2 connection...")
try:
    conn = psycopg2.connect(
        host=db_config['HOST'],
        port=db_config['PORT'],
        user=db_config['USER'],
        password=db_config.get('PASSWORD', ''),
        database='postgres'  # Try connecting to default postgres DB first
    )
    print("✅ Successfully connected to PostgreSQL server!")
    
    # Get PostgreSQL version
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    print(f"   PostgreSQL version: {version.split(',')[0]}")
    
    # Check if target database exists
    cursor.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s;",
        (db_config['NAME'],)
    )
    db_exists = cursor.fetchone()
    
    if db_exists:
        print(f"✅ Database '{db_config['NAME']}' exists")
    else:
        print(f"⚠️  Database '{db_config['NAME']}' does NOT exist")
        print(f"   Solution: Create database first")
        response = input("   Do you want to create it now? (y/n): ")
        if response.lower() == 'y':
            conn.autocommit = True
            cursor.execute(f'CREATE DATABASE {db_config["NAME"]};')
            print(f"   ✅ Database '{db_config['NAME']}' created successfully!")
    
    cursor.close()
    conn.close()
    
except psycopg2.OperationalError as e:
    print(f"❌ Connection failed: {e}")
    print()
    print("Common issues:")
    print("  - PostgreSQL service is not running")
    print("  - Wrong host/port number")
    print("  - Wrong username/password")
    print("  - Firewall blocking connection")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 4: Test connection to target database
print(f"Test 4: Testing connection to '{db_config['NAME']}' database...")
try:
    conn = psycopg2.connect(
        host=db_config['HOST'],
        port=db_config['PORT'],
        user=db_config['USER'],
        password=db_config.get('PASSWORD', ''),
        database=db_config['NAME']
    )
    print(f"✅ Successfully connected to database '{db_config['NAME']}'!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT current_database(), current_user, version();")
    db_name, user, version = cursor.fetchone()
    print(f"   Current database: {db_name}")
    print(f"   Current user: {user}")
    
    cursor.close()
    conn.close()
    
except psycopg2.OperationalError as e:
    print(f"❌ Failed to connect to database: {e}")
    print("   Make sure the database exists and user has permissions")
    sys.exit(1)

print()

# Test 5: Test Django database connection
print("Test 5: Testing Django database connection...")
try:
    from django.db import connection
    
    # Test connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        
    if result:
        print("✅ Django database connection works!")
        
        # Check if tables exist
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public';
            """)
            table_count = cursor.fetchone()[0]
            print(f"   Existing tables in database: {table_count}")
            
            if table_count == 0:
                print("   ⚠️  Database is empty - you need to run migrations")
                print("      Run: python manage.py migrate")
    
except Exception as e:
    print(f"❌ Django connection failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 60)
print("✅ All tests passed! Your database connection is working.")
print("=" * 60)
print()
print("Next steps:")
print("1. Run migrations: python manage.py migrate")
print("2. Create superuser: python manage.py createsuperuser")
print("3. Start server: python manage.py runserver")


