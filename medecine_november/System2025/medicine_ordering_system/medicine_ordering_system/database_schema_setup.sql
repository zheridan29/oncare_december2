-- Database Schema Setup Script for OnCare Medicine Ordering System
-- This script creates the database and user with proper permissions
-- Run this BEFORE running Django migrations

-- ============================================================
-- PostgreSQL Setup (Recommended)
-- ============================================================

-- Connect as postgres superuser:
-- sudo -u postgres psql

-- Create database
CREATE DATABASE oncare_medicine_db
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

-- Create user
CREATE USER oncare_user WITH ENCRYPTED PASSWORD 'your_secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE oncare_medicine_db TO oncare_user;

-- Connect to the database
\c oncare_medicine_db

-- Grant schema privileges (required for Django migrations)
GRANT ALL ON SCHEMA public TO oncare_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO oncare_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO oncare_user;

-- Set timezone
ALTER DATABASE oncare_medicine_db SET timezone = 'UTC';

-- Create extensions (if needed)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For similarity searches

-- Exit
\q

-- ============================================================
-- MySQL/MariaDB Setup (Alternative)
-- ============================================================

-- Connect as root:
-- sudo mysql -u root -p

-- Create database
CREATE DATABASE IF NOT EXISTS oncare_medicine_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Create user
CREATE USER IF NOT EXISTS 'oncare_user'@'localhost' 
    IDENTIFIED BY 'your_secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON oncare_medicine_db.* TO 'oncare_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

-- Exit
-- EXIT;

-- ============================================================
-- Post-Setup Verification
-- ============================================================

-- PostgreSQL: Test connection
-- psql -U oncare_user -d oncare_medicine_db -c "SELECT version();"

-- MySQL: Test connection
-- mysql -u oncare_user -p oncare_medicine_db -e "SELECT VERSION();"

-- ============================================================
-- Django Migration Notes
-- ============================================================

-- After running this script, execute Django migrations:
-- python manage.py migrate
--
-- This will create all tables according to your models:
-- - accounts (User, SalesRepProfile, PharmacistAdminProfile, etc.)
-- - inventory (Medicine, Category, Manufacturer, StockMovement, etc.)
-- - orders (Order, OrderItem, OrderStatusHistory, etc.)
-- - analytics (DemandForecast, ForecastMetrics, etc.)
-- - transactions (Transaction, Payment, etc.)
-- - audits (AuditLog, etc.)
-- - common (Address, BaseModel, etc.)
-- - oncare_admin (various admin models)
-- - Django system tables (auth, sessions, etc.)

