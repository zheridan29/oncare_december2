# OnCare Medicine Ordering System - Complete Deployment Guide

## Table of Contents
1. [Database Recommendation](#database-recommendation)
2. [Production Deployment Options](#production-deployment-options)
3. [Database Setup](#database-setup)
4. [Environment Configuration](#environment-configuration)
5. [Deployment Steps](#deployment-steps)
6. [Database Schema Creation](#database-schema-creation)

---

## Database Recommendation

### **PostgreSQL (Recommended)**
PostgreSQL is the **recommended database** for production deployment because:
- Excellent Django ORM support with advanced features
- Better performance for complex queries and analytics
- Superior data integrity and ACID compliance
- Advanced indexing capabilities for ARIMA forecasting queries
- Better handling of concurrent connections
- Robust full-text search capabilities
- Active community and excellent documentation

### **MySQL/MariaDB (Alternative)**
MySQL/MariaDB is a viable alternative if you:
- Already have MySQL infrastructure
- Need compatibility with existing systems
- Prefer familiar MySQL tooling

---

## Production Deployment Options

### Option 1: Cloud Platform (Recommended)
- **Heroku**: Easy deployment, managed PostgreSQL
- **AWS**: EC2 + RDS PostgreSQL, scalable
- **DigitalOcean**: App Platform or Droplets with managed databases
- **Railway**: Simple deployment with PostgreSQL
- **Render**: Free tier available with PostgreSQL

### Option 2: VPS/Server
- **Ubuntu Server 20.04+** (recommended)
- **CentOS/RHEL 8+**
- Self-managed database and server

---

## Database Setup

### PostgreSQL Setup

#### Step 1: Install PostgreSQL
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib python3-psycopg2

# CentOS/RHEL
sudo yum install postgresql postgresql-server postgresql-devel python3-psycopg2
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Step 2: Create Database and User
```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE oncare_medicine_db;
CREATE USER oncare_user WITH ENCRYPTED PASSWORD 'your_secure_password_here';
ALTER ROLE oncare_user SET client_encoding TO 'utf8';
ALTER ROLE oncare_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE oncare_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE oncare_medicine_db TO oncare_user;

# Exit PostgreSQL
\q
```

#### Step 3: Configure PostgreSQL Authentication
Edit `/etc/postgresql/14/main/pg_hba.conf` (or your version):
```conf
# Add this line for local connections
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
```

Restart PostgreSQL:
```bash
sudo systemctl restart postgresql
```

### MySQL/MariaDB Setup (Alternative)

#### Step 1: Install MySQL/MariaDB
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server mysql-client libmysqlclient-dev

# CentOS/RHEL
sudo yum install mariadb-server mariadb-devel
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

#### Step 2: Secure MySQL Installation
```bash
sudo mysql_secure_installation
```

#### Step 3: Create Database and User
```bash
sudo mysql -u root -p
```

```sql
CREATE DATABASE oncare_medicine_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'oncare_user'@'localhost' IDENTIFIED BY 'your_secure_password_here';
GRANT ALL PRIVILEGES ON oncare_medicine_db.* TO 'oncare_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

---

## Environment Configuration

### Step 1: Install Python Dependencies
```bash
# Update requirements.txt first (add psycopg2 for PostgreSQL or mysqlclient for MySQL)
pip install -r requirements.txt
```

**For PostgreSQL**, add to `requirements.txt`:
```
psycopg2-binary==2.9.9
```

**For MySQL/MariaDB**, `mysqlclient==2.2.0` is already in requirements.txt.

### Step 2: Create Production Settings

Create `medicine_ordering_system/settings_production.py` (see below)

### Step 3: Set Environment Variables
Create `.env` file:
```env
DEBUG=False
SECRET_KEY=your-super-secret-key-generate-with-python-secrets-token-hex-32
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://oncare_user:your_secure_password_here@localhost:5432/oncare_medicine_db
# OR for MySQL:
# DATABASE_URL=mysql://oncare_user:your_secure_password_here@localhost:3306/oncare_medicine_db
REDIS_URL=redis://localhost:6379
EMAIL_HOST=smtp.yourprovider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password
```

Generate a secure SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Deployment Steps

### Step 1: Prepare Codebase
```bash
# Clone or copy your project
cd /path/to/your/project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 2: Configure Production Settings
Use the `settings_production.py` file provided below.

### Step 3: Run Migrations
```bash
# Set environment variable
export DJANGO_SETTINGS_MODULE=medicine_ordering_system.settings_production

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### Step 4: Set Up Web Server

#### Using Gunicorn
```bash
pip install gunicorn

# Test run
gunicorn --bind 0.0.0.0:8000 medicine_ordering_system.wsgi:application
```

#### Using uWSGI
```bash
pip install uwsgi

# Create uwsgi.ini (see configuration below)
```

### Step 5: Configure Nginx
Create Nginx configuration (see `nginx.conf` below)

---

## Database Schema Creation

Django will automatically create the database schema when you run migrations. However, you can also:

### Option 1: Use Django Migrations (Recommended)
```bash
python manage.py migrate
```

This creates all tables based on your models.

### Option 2: Generate SQL Schema
```bash
# Generate SQL without executing
python manage.py sqlmigrate accounts 0001 > accounts_schema.sql
python manage.py sqlmigrate inventory 0001 > inventory_schema.sql
python manage.py sqlmigrate orders 0001 > orders_schema.sql
python manage.py sqlmigrate analytics 0001 > analytics_schema.sql
# ... repeat for all apps
```

### Option 3: Use Database Dump
```bash
# Export schema from development
pg_dump -U oncare_user -d oncare_medicine_db --schema-only > schema.sql

# Import to production
psql -U oncare_user -d oncare_medicine_db < schema.sql
```

---

## Additional Configuration Files

See the following files:
- `settings_production.py` - Production settings
- `nginx.conf` - Nginx configuration
- `gunicorn.conf.py` - Gunicorn configuration
- `uwsgi.ini` - uWSGI configuration (alternative)
- `database_schema.sql` - Database schema reference

---

## Security Checklist

- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Set up regular backups
- [ ] Enable database SSL connections (if remote)
- [ ] Configure proper file permissions
- [ ] Set up monitoring and logging

---

## Post-Deployment

### Initial Setup
1. Create superuser account
2. Set up initial data (categories, manufacturers)
3. Configure email settings
4. Set up Redis for caching
5. Configure Celery (if using background tasks)

### Monitoring
1. Set up error logging (Sentry, Loggly, etc.)
2. Configure performance monitoring
3. Set up database backups
4. Monitor server resources

### Maintenance
1. Schedule regular database backups
2. Keep dependencies updated
3. Monitor logs for errors
4. Update security patches regularly

