# Step-by-Step Migration: SQLite to PostgreSQL

## ✅ Your SQLite Database Exists!

Your `db.sqlite3` file is found and ready to migrate.

---

## Option 1: Manual Step-by-Step (Recommended)

### Step 1: Export Data from SQLite

**Temporarily switch to SQLite in settings.py:**
```python
# In settings.py, comment PostgreSQL and uncomment SQLite:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Export all data:**
```bash
python manage.py dumpdata --indent 2 --output data_export.json
```

This creates `data_export.json` with all your data.

### Step 2: Switch Back to PostgreSQL

**Update settings.py to use PostgreSQL again:**
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
    }
}
```

### Step 3: Run Migrations on PostgreSQL

```bash
python manage.py migrate
```

This creates all tables in PostgreSQL.

### Step 4: Import Data

```bash
python manage.py loaddata data_export.json
```

Done! Your data is now in PostgreSQL.

---

## Option 2: Automated Script

Run the automated script:

```bash
python migrate_sqlite_to_postgres.py
```

Or the simpler version:

```bash
python simple_migrate.py
```

---

## Option 3: Using Export Settings File

### Step 1: Export using special settings

```bash
python manage.py dumpdata --settings=settings_export_sqlite --indent 2 --output data_export.json
```

This uses SQLite without changing your main settings.py.

### Step 2: Ensure PostgreSQL is ready

```bash
python manage.py migrate
```

### Step 3: Import data

```bash
python manage.py loaddata data_export.json
```

---

## What Gets Migrated?

All your data will be transferred:
- ✅ Users and profiles
- ✅ Medicines and inventory
- ✅ Categories and manufacturers
- ✅ Orders and order items
- ✅ Transactions and payments
- ✅ Analytics and forecasts
- ✅ Audit logs
- ✅ All other data

---

## Verification After Migration

Check data counts:

```bash
python manage.py shell
```

```python
from accounts.models import User
from inventory.models import Medicine
from orders.models import Order

print(f"Users: {User.objects.count()}")
print(f"Medicines: {Medicine.objects.count()}")
print(f"Orders: {Order.objects.count()}")
```

Compare these counts with your SQLite database to verify everything migrated.

---

## Troubleshooting

### If export fails:
- Make sure settings.py is using SQLite
- Check that db.sqlite3 exists

### If import fails with foreign key errors:
Export and import in dependency order (see QUICK_MIGRATION_GUIDE.md)

### If you get connection errors:
- Verify PostgreSQL is running
- Check database credentials in settings.py
- Run: `python test_db_connection.py`

---

## Files Created for You

1. **QUICK_MIGRATION_GUIDE.md** - Quick reference
2. **MIGRATE_SQLITE_TO_POSTGRESQL.md** - Detailed guide
3. **migrate_sqlite_to_postgres.py** - Automated script
4. **simple_migrate.py** - Simpler automated script
5. **settings_export_sqlite.py** - Settings for exporting from SQLite

---

**Ready to migrate?** Start with Option 1 for the most control, or use Option 2 for automation!


