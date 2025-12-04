# 🚀 Start Here: Migrate SQLite to PostgreSQL

## ✅ Quick 3-Step Migration

Your SQLite database exists and PostgreSQL is configured. Here's the simplest way to migrate:

---

## Step 1: Export Data from SQLite (2 minutes)

### 1.1: Temporarily switch to SQLite

Open `medicine_ordering_system/settings.py` and change lines 108-121:

**FROM (current - PostgreSQL):**
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
        'CONN_MAX_AGE': 0,
    }
}
```

**TO (temporary - SQLite):**
```python
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'oncare_medicine_db',
#         'USER': 'postgres',
#         'PASSWORD': 'z3rr3Itug',
#         'HOST': 'localhost',
#         'PORT': '5433',
#         'OPTIONS': {
#             'connect_timeout': 10,
#         },
#         'CONN_MAX_AGE': 0,
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 1.2: Export data

```bash
python manage.py dumpdata --indent 2 --output data_export.json
```

Wait for it to complete. You'll see a file `data_export.json` created.

---

## Step 2: Switch Back to PostgreSQL (1 minute)

### 2.1: Change settings.py back to PostgreSQL

Open `medicine_ordering_system/settings.py` and change back:

**FROM (current - SQLite):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**TO (back to PostgreSQL):**
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
        'CONN_MAX_AGE': 0,
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
```

### 2.2: Create tables in PostgreSQL

```bash
python manage.py migrate
```

This creates all tables in PostgreSQL (empty for now).

---

## Step 3: Import Data into PostgreSQL (2 minutes)

```bash
python manage.py loaddata data_export.json
```

Done! All your data is now in PostgreSQL! 🎉

---

## ✅ Verify Migration

Check if data was migrated:

```bash
python manage.py shell
```

Then type:
```python
from accounts.models import User
from inventory.models import Medicine
from orders.models import Order

print(f"Users: {User.objects.count()}")
print(f"Medicines: {Medicine.objects.count()}")
print(f"Orders: {Order.objects.count()}")
```

Compare these numbers with what you had in SQLite.

---

## 📋 Summary

1. ✅ Switch settings.py to SQLite
2. ✅ Run: `python manage.py dumpdata --indent 2 --output data_export.json`
3. ✅ Switch settings.py back to PostgreSQL
4. ✅ Run: `python manage.py migrate`
5. ✅ Run: `python manage.py loaddata data_export.json`
6. ✅ Done!

---

## 🆘 Need Help?

- See `MIGRATION_STEPS.md` for detailed instructions
- See `QUICK_MIGRATION_GUIDE.md` for quick reference
- See `TROUBLESHOOTING_POSTGRESQL.md` if you have connection issues

---

## 💾 Backup Recommendation

After migration is complete:
1. Keep `db.sqlite3` as backup (don't delete it yet)
2. Keep `data_export.json` as backup
3. Test your application thoroughly
4. Once verified, you can delete `data_export.json` (keep SQLite for reference)

---

**Ready? Start with Step 1 above!** ⬆️

