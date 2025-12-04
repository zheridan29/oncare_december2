# Quick Guide: Migrate SQLite to PostgreSQL

## Simple 3-Step Process

### Step 1: Export Data from SQLite

First, temporarily use SQLite settings to export all data:

```bash
# Export all data to JSON file
python manage.py dumpdata --settings=settings_export_sqlite --indent 2 --output=data_export.json

# This creates a file called data_export.json with all your data
```

**Note:** Make sure `db.sqlite3` exists in your project directory.

### Step 2: Ensure PostgreSQL is Ready

Make sure PostgreSQL has all tables created:

```bash
# Run migrations (this creates all tables in PostgreSQL)
python manage.py migrate
```

### Step 3: Import Data into PostgreSQL

Now import the exported data:

```bash
# Import all data from JSON file
python manage.py loaddata data_export.json
```

That's it! Your data is now in PostgreSQL.

---

## Verification

Check if data was migrated:

```bash
python manage.py shell
```

Then in Python shell:
```python
from accounts.models import User
from inventory.models import Medicine
from orders.models import Order

print(f"Users: {User.objects.count()}")
print(f"Medicines: {Medicine.objects.count()}")
print(f"Orders: {Order.objects.count()}")
```

---

## Automated Script (Easier!)

Or just run the automated script:

```bash
python migrate_sqlite_to_postgres.py
```

This script does everything automatically!

---

## Troubleshooting

### If export fails:
- Make sure `db.sqlite3` exists
- Check that you have read permissions

### If import fails due to foreign keys:
Export and import in dependency order:

```bash
# Export in order
python manage.py dumpdata contenttypes --settings=settings_export_sqlite --indent 2 > 01_contenttypes.json
python manage.py dumpdata auth --settings=settings_export_sqlite --indent 2 > 02_auth.json
python manage.py dumpdata accounts --settings=settings_export_sqlite --indent 2 > 03_accounts.json
python manage.py dumpdata common --settings=settings_export_sqlite --indent 2 > 04_common.json
python manage.py dumpdata inventory --settings=settings_export_sqlite --indent 2 > 05_inventory.json
python manage.py dumpdata orders --settings=settings_export_sqlite --indent 2 > 06_orders.json
python manage.py dumpdata transactions --settings=settings_export_sqlite --indent 2 > 07_transactions.json
python manage.py dumpdata analytics --settings=settings_export_sqlite --indent 2 > 08_analytics.json

# Import in same order
python manage.py loaddata 01_contenttypes.json
python manage.py loaddata 02_auth.json
python manage.py loaddata 03_accounts.json
python manage.py loaddata 04_common.json
python manage.py loaddata 05_inventory.json
python manage.py loaddata 06_orders.json
python manage.py loaddata 07_transactions.json
python manage.py loaddata 08_analytics.json
```

---

## What Gets Migrated?

- ✅ All users and profiles
- ✅ All medicines and inventory
- ✅ All orders and order items
- ✅ All transactions
- ✅ All analytics/forecasts
- ✅ All audit logs
- ✅ All settings and configurations

Everything in your SQLite database will be transferred to PostgreSQL!


