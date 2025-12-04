#!/bin/bash
# Deployment script for OnCare Medicine Ordering System
# Usage: ./deploy.sh [production|staging]

set -e  # Exit on error

ENVIRONMENT=${1:-production}
PROJECT_DIR="/path/to/your/project"  # Update this path
VENV_DIR="$PROJECT_DIR/venv"
SETTINGS_MODULE="medicine_ordering_system.settings_production"

echo "========================================="
echo "OnCare Medicine Ordering System"
echo "Deployment Script - $ENVIRONMENT"
echo "========================================="

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# Activate virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Set environment variables
export DJANGO_SETTINGS_MODULE=$SETTINGS_MODULE

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser (interactive)
echo "Do you want to create a superuser? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser
fi

# Test configuration
echo "Testing Django configuration..."
python manage.py check --deploy

echo "========================================="
echo "Deployment completed successfully!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Start Gunicorn: gunicorn -c gunicorn.conf.py medicine_ordering_system.wsgi:application"
echo "2. Or use systemd service: sudo systemctl start oncare.service"
echo "3. Configure Nginx and start it: sudo systemctl start nginx"
echo "4. Test your deployment"

