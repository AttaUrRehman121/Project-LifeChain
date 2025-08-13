# Debugging Guide for Internal Server Error

## Current Status

- ✅ Project deployed successfully on Railway
- ✅ Redirect loop fixed (HTTPS redirect disabled)
- ✅ Whitenoise removed (was causing static file issues)
- ❌ Internal Server Error occurring

## Debugging Steps

### 1. **Check Railway Logs**

Go to your Railway dashboard and check the logs for the specific error message.

### 2. **Test Simple Endpoints (in order of complexity)**

1. **Health Check**: `https://lifechain.up.railway.app/health/`
   - Should show "OK" (no dependencies)
2. **Test View**: `https://lifechain.up.railway.app/test/`
   - Should show "Django is working! This is a test view."
3. **Main Page**: `https://lifechain.up.railway.app/`
   - Should show the index page

### 3. **Check Environment Variables**

Ensure these are set in Railway:

- `SECRET_KEY`: A valid Django secret key
- `DATABASE_URL`: Railway should provide this automatically
- `DEBUG`: Set to `True` temporarily for debugging

### 4. **Common Causes of Internal Server Error**

#### A. **Database Connection Issues**

- Check if `DATABASE_URL` is set correctly
- Verify database is accessible
- Check if migrations ran successfully

#### B. **Template Rendering Issues**

- Check if all template files exist
- Verify static files are collected
- Check for template syntax errors

#### C. **Import Errors**

- Check if all required packages are installed
- Verify model imports are working
- Check for circular import issues

#### D. **Environment Variable Issues**

- Ensure all required environment variables are set
- Check for typos in variable names
- Verify variable values are correct

### 5. **Recent Changes Made**

#### **Whitenoise Removed**

- Removed from `INSTALLED_APPS`
- Removed from `MIDDLEWARE`
- Removed from `requirements.txt`
- Using Django's default static file handling

#### **Enhanced Debugging**

- `DEBUG = True` to show detailed error messages
- Added comprehensive logging configuration
- Added error handling to all views
- Added health check endpoint (`/health/`)
- Added test endpoint (`/test/`)

### 6. **Next Steps**

1. **Deploy the current changes**:

   ```bash
   git add .
   git commit -m "Remove Whitenoise and add comprehensive debugging"
   git push origin main
   ```

2. **Test endpoints in order**:

   - `/health/` (should work)
   - `/test/` (should work)
   - `/` (main page)

3. **Check Railway logs** for specific error messages

4. **If still getting errors**, the logs will now show exactly what's failing

### 7. **Expected Behavior After Fix**

- `/health/` → "OK"
- `/test/` → "Django is working!"
- `/` → Index page (should work now)
- `/admin/` → Django admin
- Other pages should work normally

### 8. **If Issues Persist**

Check these specific areas:

1. **Database**: Ensure PostgreSQL is running and accessible
2. **Static Files**: Verify `collectstatic` ran successfully
3. **Templates**: Check if all template files are present
4. **Dependencies**: Ensure all packages are installed correctly
5. **Models**: Check for any model import issues

### 9. **Static Files Handling**

Since Whitenoise is removed:

- Django will handle static files through its default mechanism
- Railway will serve static files through its proxy
- No additional middleware needed for static files

## Support

- Check Railway logs first
- Test endpoints in order: `/health/` → `/test/` → `/`
- Look for specific error messages
- Verify environment variables are set correctly
