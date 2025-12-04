# PostgreSQL Connection Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: Missing psycopg2 Package
**Error:** `ModuleNotFoundError: No module named 'psycopg2'`

**Solution:**
```bash
pip install psycopg2-binary
```

### Issue 2: Database Doesn't Exist
**Error:** `django.db.utils.OperationalError: FATAL: database "oncare_medicine_db" does not exist`

**Solution:**
```bash
# Connect to PostgreSQL
psql -U postgres -p 5433

# Create the database
CREATE DATABASE oncare_medicine_db;

# Grant privileges (if using a different user)
GRANT ALL PRIVILEGES ON DATABASE oncare_medicine_db TO postgres;

# Exit
\q
```

### Issue 3: Connection Refused
**Error:** `could not connect to server: Connection refused`

**Solutions:**

**a) Check if PostgreSQL is running:**
```bash
# Windows
# Check services: Services.msc and look for PostgreSQL

# Linux
sudo systemctl status postgresql
# If not running:
sudo systemctl start postgresql
```

**b) Check the correct port:**
```bash
# Check what port PostgreSQL is actually using
# Windows: Check postgresql.conf or use netstat
netstat -an | findstr 5432
netstat -an | findstr 5433

# Linux
sudo netstat -tlnp | grep postgres
# OR
sudo ss -tlnp | grep postgres
```

### Issue 4: Authentication Failed
**Error:** `FATAL: password authentication failed for user "postgres"`

**Solutions:**

**a) Reset PostgreSQL password:**
```bash
# Windows - Edit pg_hba.conf and change authentication method temporarily
# File location: C:\Program Files\PostgreSQL\14\data\pg_hba.conf
# Change: md5 to trust (then restart and change password, then change back)

# Or use pgAdmin to reset password

# Linux - Reset password
sudo -u postgres psql
ALTER USER postgres WITH PASSWORD 'z3rr3Itug';
\q
```

**b) Check pg_hba.conf authentication method:**
```bash
# Find pg_hba.conf location
# Windows: Usually in data directory
# Linux: /etc/postgresql/14/main/pg_hba.conf

# Make sure it has:
host    all             all             127.0.0.1/32            md5
```

### Issue 5: Wrong Port Number
**Error:** Connection timeouts or connection refused

Your settings show port `5433`, but PostgreSQL default is `5432`.

**Solutions:**

**a) Verify actual port:**
```sql
-- Connect to PostgreSQL (any way you can)
SELECT setting FROM pg_settings WHERE name = 'port';
```

**b) Check if multiple PostgreSQL instances are running:**
```bash
# Windows: Check services
# Look for multiple PostgreSQL services

# Linux
sudo systemctl list-units | grep postgres
```

### Issue 6: Permission Denied
**Error:** `permission denied for database`

**Solution:**
```sql
-- Connect as postgres superuser
psql -U postgres -p 5433

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE oncare_medicine_db TO postgres;
ALTER DATABASE oncare_medicine_db OWNER TO postgres;
\q
```

---

## Step-by-Step Connection Test

### Step 1: Test PostgreSQL Connection
```bash
# Test connection manually
psql -U postgres -h localhost -p 5433 -d postgres

# If that works, test your specific database:
psql -U postgres -h localhost -p 5433 -d oncare_medicine_db
```

### Step 2: Check Database Exists
```sql
-- List all databases
\l

-- If oncare_medicine_db doesn't exist, create it:
CREATE DATABASE oncare_medicine_db;
```

### Step 3: Test Django Connection
```bash
# In your Django project directory
python manage.py dbshell

# If successful, you'll see PostgreSQL prompt
# Type \q to exit
```

### Step 4: Check Django Settings
Run this Python script to test connection:
```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        row = cursor.fetchone()
        print(f"✅ Connected successfully!")
        print(f"PostgreSQL version: {row[0]}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

---

## Quick Fixes

### Fix 1: Update Settings with OPTIONS
Add connection options to your settings.py:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'oncare_medicine_db',
        'USER': 'postgres',
        'PASSWORD': 'z3rr3Itug',
        'HOST': 'localhost',
        'PORT': '5433',
        'OPTIONS': {
            'connect_timeout': 10,
        },
        'CONN_MAX_AGE': 0,  # Disable persistent connections for debugging
    }
}
```

### Fix 2: Create Database If Missing
```bash
# Create database script
python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='localhost',
        port=5433,
        user='postgres',
        password='z3rr3Itug',
        database='postgres'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE oncare_medicine_db;')
    print('✅ Database created successfully!')
    cursor.close()
    conn.close()
except psycopg2.errors.DuplicateDatabase:
    print('⚠️ Database already exists')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

---

## Windows-Specific Issues

### Issue: PostgreSQL Service Not Running
```powershell
# Check service status
Get-Service -Name postgresql*

# Start service
Start-Service postgresql-x64-14  # Adjust version number

# Or use Services.msc GUI
```

### Issue: Multiple PostgreSQL Installations
Check for multiple PostgreSQL installations and ensure you're connecting to the correct one.

```powershell
# List all PostgreSQL services
Get-Service | Where-Object {$_.Name -like "*postgres*"}

# Check which ports are in use
netstat -ano | findstr :5432
netstat -ano | findstr :5433
```

---

## Verification Checklist

- [ ] PostgreSQL service is running
- [ ] psycopg2-binary is installed: `pip list | grep psycopg2`
- [ ] Database exists: `psql -U postgres -p 5433 -l | grep oncare_medicine_db`
- [ ] Can connect manually: `psql -U postgres -p 5433 -d oncare_medicine_db`
- [ ] Password is correct
- [ ] Port number matches (5433 or 5432)
- [ ] HOST is correct (localhost or 127.0.0.1)
- [ ] User has proper permissions

---

## Still Having Issues?

Run the diagnostic script below to get detailed error information.

