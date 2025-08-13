# Debugging Guide for Internal Server Error

## Current Status

- ✅ Project deployed successfully on Railway
- ✅ Redirect loop fixed (HTTPS redirect disabled)
- ❌ Internal Server Error occurring

## Debugging Steps

### 1. **Check Railway Logs**

Go to your Railway dashboard and check the logs for the specific error message.

### 2. **Test Simple Endpoint**

Try accessing: `https://lifechain.up.railway.app/test/`
This should show "Django is working! This is a test view."

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

### 5. **Temporary Debug Settings Applied**

I've temporarily enabled:

- `DEBUG = True` to show detailed error messages
- Added logging configuration
- Added error handling to the index view
- Added a test view for debugging

### 6. **Next Steps**

1. **Deploy the current changes**:

   ```bash
   git add .
   git commit -m "Add debugging and fix internal server error"
   git push origin main
   ```

2. **Check Railway logs** for the specific error

3. **Test the test endpoint**: `/test/`

4. **If still getting errors**, check the logs for the specific error message

### 7. **Expected Behavior After Fix**

- `/` should work (index page)
- `/test/` should show "Django is working!"
- `/admin/` should show Django admin
- Other pages should work normally

### 8. **If Issues Persist**

Check these specific areas:

1. **Database**: Ensure PostgreSQL is running and accessible
2. **Static Files**: Verify `collectstatic` ran successfully
3. **Templates**: Check if all template files are present
4. **Dependencies**: Ensure all packages are installed correctly

## Support

- Check Railway logs first
- Look for specific error messages
- Test the `/test/` endpoint
- Verify environment variables are set correctly
