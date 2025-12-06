# Render Deployment Guide

This guide explains the changes made to prepare your Django application for deployment on Render.

## Changes Made

### 1. Settings Configuration (`medicine_ordering_system/settings.py`)

✅ **Security Settings:**
- `SECRET_KEY` now uses environment variable (Render will auto-generate)
- `DEBUG` automatically set to `False` when running on Render (checks for `RENDER` environment variable)
- `ALLOWED_HOSTS` automatically configured from `RENDER_EXTERNAL_HOSTNAME`

✅ **Database Configuration:**
- Updated to use `dj_database_url` for PostgreSQL connection
- Automatically uses `DATABASE_URL` environment variable from Render
- Falls back to local PostgreSQL for development

✅ **Static Files:**
- Configured WhiteNoise middleware (already added)
- Static files will be served via WhiteNoise in production
- Development mode continues to use `STATICFILES_DIRS`

### 2. Requirements (`requirements.txt`)

✅ **Added:**
- `uvicorn==0.38.0` - Required for ASGI server with Gunicorn on Render

✅ **Already Present:**
- `whitenoise==6.11.0` - For static file serving
- `dj-database-url==3.0.1` - For database URL parsing
- `psycopg2-binary==2.9.11` - PostgreSQL adapter
- `gunicorn==23.0.0` - Production WSGI/ASGI server

### 3. Build Script (`build.sh`)

✅ Already configured correctly:
- Installs dependencies
- Collects static files
- Runs database migrations

### 4. Render Configuration (`render.yaml`)

✅ Created configuration file that defines:
- PostgreSQL database service (free tier)
- Web service configuration
- Environment variables
- Build and start commands

## Deployment Steps

### Option 1: Using Blueprint (Recommended)

1. **Push your code to GitHub/GitLab/Bitbucket**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push
   ```

2. **Deploy via Render Dashboard:**
   - Go to [Render Blueprints](https://dashboard.render.com/blueprints)
   - Click **New Blueprint Instance**
   - Connect your repository
   - Render will automatically detect `render.yaml` and create the services

### Option 2: Manual Setup

1. **Create PostgreSQL Database:**
   - Go to Render Dashboard → New → PostgreSQL
   - Choose Free plan
   - Copy the Internal Database URL

2. **Create Web Service:**
   - Go to Render Dashboard → New → Web Service
   - Connect your repository
   - Use these settings:
     - **Build Command:** `./build.sh`
     - **Start Command:** `python -m gunicorn medicine_ordering_system.asgi:application -k uvicorn.workers.UvicornWorker`
     - **Environment Variables:**
       - `DATABASE_URL`: (from your PostgreSQL service)
       - `SECRET_KEY`: (click "Generate" or use a secure random string)
       - `WEB_CONCURRENCY`: `4`

3. **Update ALLOWED_HOSTS (if needed):**
   - After deployment, Render will provide your app URL (e.g., `your-app.onrender.com`)
   - If using a custom domain, add it to `ALLOWED_HOSTS` in settings.py

## Important Notes

### ⚠️ Celery/Redis Configuration

Your application currently uses Celery with Redis. **The free tier on Render does not include Redis.**

**Options:**
1. **Disable Celery tasks** (if not critical for initial deployment)
2. **Use Upstash Redis** (free tier available) and update `CELERY_BROKER_URL`
3. **Upgrade to paid Render plan** with Redis addon

To disable Celery temporarily, comment out Celery-related code or handle tasks synchronously.

### 📝 Environment Variables to Set in Render Dashboard

If not using `render.yaml`, manually set these:

- `DATABASE_URL` - Auto-provided by Render when linking database
- `SECRET_KEY` - Generate a secure random string (Render can auto-generate)
- `RENDER_EXTERNAL_HOSTNAME` - Auto-set by Render
- `RENDER` - Auto-set by Render (used to detect Render environment)

### 🔒 Security Checklist

- ✅ SECRET_KEY uses environment variable
- ✅ DEBUG automatically disabled in production
- ✅ ALLOWED_HOSTS configured
- ✅ Static files served via WhiteNoise
- ⚠️ Review other security settings in [Django deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)

### 📦 Media Files Storage

Currently, media files are stored locally. For production:

1. **Recommended:** Use AWS S3 or similar cloud storage
   - Install `django-storages` (already in requirements.txt)
   - Configure `DEFAULT_FILE_STORAGE` in settings

2. **Alternative:** Use Render's disk storage (limited, not persistent)
   - Files will be lost on redeploy

### 🔍 Post-Deployment Steps

1. **Run migrations:**
   - Migrations run automatically via `build.sh`
   - But verify in Render logs that they completed successfully

2. **Create superuser:**
   - Use Render's shell: `render.com → Your Service → Shell`
   - Run: `python manage.py createsuperuser`

3. **Verify deployment:**
   - Check logs in Render dashboard
   - Test your application URL
   - Verify static files are loading

4. **Set up custom domain (optional):**
   - In Render dashboard → Your Service → Settings
   - Add custom domain
   - Update `ALLOWED_HOSTS` if needed

## Local Development

Your local development environment remains unchanged:
- Continue using `python manage.py runserver` locally
- Local database settings work as before
- DEBUG=True for local development

## Troubleshooting

### Static files not loading
- Check that `collectstatic` ran successfully (check build logs)
- Verify WhiteNoise middleware is in `MIDDLEWARE` list
- Check `STATIC_ROOT` and `STATICFILES_STORAGE` settings

### Database connection errors
- Verify `DATABASE_URL` environment variable is set correctly
- Check database service is running in Render dashboard
- Review connection string format

### Application not starting
- Check build logs for errors
- Verify all dependencies in `requirements.txt`
- Check start command is correct
- Review application logs in Render dashboard

## References

- [Render Django Deployment Guide](https://render.com/docs/deploy-django)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [WhiteNoise Documentation](https://whitenoise.evans.io/en/stable/django.html)

