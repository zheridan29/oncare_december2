# Migrate Data from SQLite to PostgreSQL

This guide will help you transfer all your data from SQLite to PostgreSQL database.

## Prerequisites

- ✅ SQLite database exists (`db.sqlite3`)
- ✅ PostgreSQL database is set up and connected
- ✅ Both databases are accessible from Django

---

## Method 1: Using Django dumpdata/loaddata (Recommended)

This is the safest and most reliable method using Django's built-in tools.

### Step 1: Verify Your Current Setup

```bash
# Check if SQLite database exists
ls -la db.sqlite3  # Linux/Mac
dir db.sqlite3     # Windows

# Verify PostgreSQL connection
python manage.py dbshell
# Type \q to exit
```

### Step 2: Update Settings to Use SQLite (Temporary)

First, we need to export data from SQLite, so temporarily switch back:

**Option A: Create a temporary settings file for export**

Create `settings_export.py`:
```python
from .settings import *

# Override database to use SQLite for export
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Step 3: Export Data from SQLite

```bash
# Export all data to JSON file
python manage.py dumpdata --settings=medicine_ordering_system.settings_export --indent 2 > data_export.json

# Or export specific apps only:
python manage.py dumpdata accounts --settings=medicine_ordering_system.settings_export --indent 2 > accounts_data.json
python manage.py dumpdata inventory --settings=medicine_ordering_system.settings_export --indent 2 > inventory_data.json
python manage.py dumpdata orders --settings=medicine_ordering_system.settings_export --indent 2 > orders_data.json
python manage.py dumpdata analytics --settings=medicine_ordering_system.settings_export --indent 2 > analytics_data.json
python manage.py dumpdata transactions --settings=medicine_ordering_system.settings_export --indent 2 > transactions_data.json
python manage.py dumpdata audits --settings=medicine_ordering_system.settings_export --indent 2 > audits_data.json
python manage.py dumpdata common --settings=medicine_ordering_system.settings_export --indent 2 > common_data.json
python manage.py dumpdata oncare_admin --settings=medicine_ordering_system.settings_export --indent 2 > oncare_admin_data.json
```

### Step 4: Ensure PostgreSQL Schema is Ready

```bash
# Make sure PostgreSQL has all migrations applied
python manage.py migrate
```

### Step 5: Import Data into PostgreSQL

```bash
# Import all data
python manage.py loaddata data_export.json

# Or import app by app:
python manage.py loaddata accounts_data.json
python manage.py loaddata inventory_data.json
python manage.py loaddata orders_data.json
python manage.py loaddata analytics_data.json
python manage.py loaddata transactions_data.json
python manage.py loaddata audits_data.json
python manage.py loaddata common_data.json
python manage.py loaddata oncare_admin_data.json
```

---

## Method 2: Automated Migration Script

I'll create a script that automates this process for you.

---

## Method 3: Manual SQL Export/Import (Advanced)

If dumpdata/loaddata doesn't work, you can manually export and import.

### Step 1: Export from SQLite

```bash
# Using sqlite3 command line
sqlite3 db.sqlite3 .dump > sqlite_dump.sql
```

### Step 2: Convert SQL for PostgreSQL

SQLite and PostgreSQL have some syntax differences. You'll need to:
- Replace `INTEGER PRIMARY KEY AUTOINCREMENT` with `SERIAL PRIMARY KEY`
- Handle boolean values differently
- Adjust date/time formats

### Step 3: Import to PostgreSQL

```bash
psql -U postgres -d oncare_medicine_db -f converted_dump.sql
```

**Note:** This method is more complex and error-prone. Use Method 1 instead.

---

## Verification Steps

After migration, verify your data:

```bash
# Check data counts in PostgreSQL
python manage.py shell
```

```python
from accounts.models import User
from inventory.models import Medicine
from orders.models import Order

print(f"Users: {User.objects.count()}")
print(f"Medicines: {Medicine.objects.count()}")
print(f"Orders: {Order.objects.count()}")

# Compare with SQLite if needed
```

---

## Troubleshooting

### Issue: Foreign key constraints fail

**Solution:** Export data in the correct order (dependencies first):
```bash
# Export in dependency order
python manage.py dumpdata contenttypes --settings=... > 01_contenttypes.json
python manage.py dumpdata auth --settings=... > 02_auth.json
python manage.py dumpdata accounts --settings=... > 03_accounts.json
python manage.py dumpdata common --settings=... > 04_common.json
python manage.py dumpdata inventory --settings=... > 05_inventory.json
python manage.py dumpdata orders --settings=... > 06_orders.json
python manage.py dumpdata transactions --settings=... > 07_transactions.json
python manage.py dumpdata analytics --settings=... > 08_analytics.json
```

Then import in the same order.

### Issue: Data types don't match

**Solution:** Run migrations first to ensure schema matches:
```bash
python manage.py migrate
```

### Issue: Large files timeout

**Solution:** Use compression and split files:
```bash
python manage.py dumpdata --settings=... | gzip > data_export.json.gz
gunzip < data_export.json.gz | python manage.py loaddata --format=json -
```

---

## Quick Migration Script

See `migrate_sqlite_to_postgres.py` for an automated script.

---

## Post-Migration Checklist

- [ ] Verify all tables exist in PostgreSQL
- [ ] Check record counts match SQLite
- [ ] Test application functionality
- [ ] Backup PostgreSQL database
- [ ] Keep SQLite backup for reference
- [ ] Update settings to use PostgreSQL permanently


