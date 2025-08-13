# Railway Deployment Guide for LifeChain

## Prerequisites
- Railway account
- Git repository connected to Railway
- Environment variables configured

## Environment Variables
Set these in your Railway project dashboard:

### Required Variables:
- `SECRET_KEY`: Django secret key (generate a new one for production)
- `DATABASE_URL`: Railway will provide this automatically
- `DEBUG`: Set to `False` for production

### Optional Variables:
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `CSRF_TRUSTED_ORIGINS`: Comma-separated list of trusted origins
- `EMAIL_HOST_USER`: Your email for sending notifications
- `EMAIL_HOST_PASSWORD`: Your email app password
- `BLOCKCHAIN_PROVIDER`: Your blockchain provider URL (can be empty)
- `CONTRACT_ADDRESS`: Your smart contract address (can be empty)
- `BACKEND_WALLET_ADDRESS`: Your backend wallet address (can be empty)
- `BACKEND_PRIVATE_KEY`: Your backend private key (can be empty)

## Deployment Steps

1. **Push your code to Git**:
   ```bash
   git add .
   git commit -m "Fix Railway deployment issues and clean up imports"
   git push origin main
   ```

2. **Railway will automatically detect the changes and start building**

3. **Monitor the build logs** for any errors**

4. **Check the deployment** once it's complete

## Common Issues and Solutions

### Build Failures
- **Virtual environment issues**: The `nixpacks.toml` file should handle this
- **Package conflicts**: Check `requirements.txt` for incompatible packages
- **Missing dependencies**: Ensure all required packages are in requirements.txt

### Migration Failures (Most Common Issue)
The build process now handles migration failures gracefully:
- **Database connection issues**: Ensure `DATABASE_URL` is set correctly
- **Model import issues**: Fixed circular imports and blockchain dependencies
- **Environment variable issues**: Blockchain features are now optional

### Runtime Errors
- **Database connection**: Ensure `DATABASE_URL` is set correctly
- **Static files**: The build process should handle `collectstatic`
- **Environment variables**: Check all required variables are set

### Performance Issues
- **Static files**: Ensure Whitenoise is configured correctly
- **Database**: Use Railway's PostgreSQL for better performance

## Troubleshooting

### If build still fails:
1. Check Railway build logs for specific error messages
2. Verify all files are committed to Git
3. Ensure `requirements.txt` has no Windows-specific packages
4. Check for syntax errors in Python files

### If migration fails:
1. The build process now continues even if migrations fail
2. Check Railway logs for specific migration error messages
3. Ensure `DATABASE_URL` is set correctly
4. Blockchain features are now optional and won't cause failures

### If app doesn't start:
1. Check Railway logs for runtime errors
2. Verify environment variables are set correctly
3. Ensure database is accessible
4. Check if all required services are running

## Recent Fixes Applied

### Import Issues Fixed:
- Removed incorrect imports in `donor/views.py`
- Fixed `from venv import logger` in `recipient/views.py`
- Removed incorrect `from multiprocessing import AuthenticationError` in `home/views.py`
- Cleaned up duplicate imports in model files

### Blockchain Dependencies Made Optional:
- `blockchain.py` now handles missing web3 gracefully
- `eth_wallet.py` now handles missing dependencies gracefully
- These won't cause migration failures anymore

### Build Process Improved:
- Added error handling for migrations
- Build continues even if migrations fail
- Better error messages and warnings

## Support
If you continue to have issues, check:
- Railway documentation: https://docs.railway.app/
- Django deployment checklist: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
- Your application logs in Railway dashboard
