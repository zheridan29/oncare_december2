# Quick Start Deployment Guide

## Prerequisites Checklist

- [ ] Server with Ubuntu 20.04+ or similar Linux distribution
- [ ] Python 3.8+ installed
- [ ] PostgreSQL 12+ OR MySQL 8.0+ installed
- [ ] Redis installed
- [ ] Nginx installed
- [ ] Domain name configured (optional but recommended)

---

## Quick Deployment Steps

### Step 1: Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv python3-dev -y

# Install PostgreSQL (Recommended)
sudo apt install postgresql postgresql-contrib libpq-dev -y

# OR Install MySQL/MariaDB (Alternative)
# sudo apt install mysql-server mysql-client libmysqlclient-dev -y

# Install Redis
sudo apt install redis-server -y

# Install Nginx
sudo apt install nginx -y

# Install build tools
sudo apt install build-essential -y
```

### Step 2: Set Up Database

#### For PostgreSQL:
```bash
# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE oncare_medicine_db;
CREATE USER oncare_user WITH ENCRYPTED PASSWORD 'your_secure_password';
ALTER ROLE oncare_user SET client_encoding TO 'utf8';
ALTER ROLE oncare_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE oncare_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE oncare_medicine_db TO oncare_user;
\c oncare_medicine_db
GRANT ALL ON SCHEMA public TO oncare_user;
\q
EOF
```

#### For MySQL/MariaDB:
```bash
sudo mysql << EOF
CREATE DATABASE oncare_medicine_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'oncare_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON oncare_medicine_db.* TO 'oncare_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
EOF
```

### Step 3: Clone/Upload Your Project

```bash
# Create project directory
sudo mkdir -p /var/www/oncare
sudo chown $USER:$USER /var/www/oncare

# Upload your project files to /var/www/oncare
# Or clone from git:
# git clone <your-repo-url> /var/www/oncare
cd /var/www/oncare
```

### Step 4: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# For PostgreSQL, ensure psycopg2-binary is installed:
pip install psycopg2-binary

# For MySQL, ensure mysqlclient is installed:
# pip install mysqlclient
```

### Step 5: Configure Environment Variables

Create `.env` file:
```bash
cat > .env << EOF
DEBUG=False
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,127.0.0.1,localhost
DB_NAME=oncare_medicine_db
DB_USER=oncare_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password
EOF
```

### Step 6: Run Migrations

```bash
# Export settings
export DJANGO_SETTINGS_MODULE=medicine_ordering_system.settings_production

# Load environment variables (if using python-dotenv)
export $(cat .env | xargs)

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### Step 7: Configure Gunicorn

Update paths in `gunicorn.conf.py` and test:
```bash
# Test Gunicorn
gunicorn --config gunicorn.conf.py medicine_ordering_system.wsgi:application
```

### Step 8: Set Up Systemd Service

```bash
# Copy service file
sudo cp oncare.service /etc/systemd/system/

# Edit paths in the service file
sudo nano /etc/systemd/system/oncare.service

# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl enable oncare.service
sudo systemctl start oncare.service

# Check status
sudo systemctl status oncare.service
```

### Step 9: Configure Nginx

```bash
# Update nginx.conf with your domain and paths
sudo nano /etc/nginx/sites-available/oncare

# Copy content from nginx.conf and update paths
# Then enable site:
sudo ln -s /etc/nginx/sites-available/oncare /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

### Step 10: Configure Firewall

```bash
# Allow HTTP and HTTPS
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw enable
```

---

## Database Schema Creation

Django automatically creates the schema when you run migrations. No manual SQL needed!

The migration command creates all tables:
```bash
python manage.py migrate
```

This will create:
- All Django system tables (auth, sessions, admin, etc.)
- All application tables (accounts, inventory, orders, analytics, etc.)
- All indexes and constraints

---

## Verify Deployment

1. **Check Django**: `python manage.py check --deploy`
2. **Check Gunicorn**: `curl http://localhost:8000`
3. **Check Nginx**: Visit your domain in a browser
4. **Check Database**: `python manage.py dbshell` (test connection)

---

## Troubleshooting

### Database Connection Issues
```bash
# PostgreSQL
psql -U oncare_user -d oncare_medicine_db -h localhost

# MySQL
mysql -u oncare_user -p oncare_medicine_db
```

### Check Logs
```bash
# Django logs
tail -f logs/django.log

# Gunicorn logs
sudo journalctl -u oncare.service -f

# Nginx logs
sudo tail -f /var/log/nginx/oncare_error.log
```

### Permissions Issues
```bash
sudo chown -R oncare:www-data /var/www/oncare
sudo chmod -R 755 /var/www/oncare
sudo chmod -R 775 /var/www/oncare/media
sudo chmod -R 775 /var/www/oncare/logs
```

---

## Next Steps

1. Set up SSL certificate (Let's Encrypt)
2. Configure automated backups
3. Set up monitoring (Sentry, etc.)
4. Configure email notifications
5. Set up Redis for caching
6. Configure Celery for background tasks

---

## Support

For detailed information, see:
- `DEPLOYMENT_COMPLETE_GUIDE.md` - Full deployment guide
- `database_schema_setup.sql` - Database setup script
- `settings_production.py` - Production settings

