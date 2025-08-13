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
- `BLOCKCHAIN_PROVIDER`: Your blockchain provider URL
- `CONTRACT_ADDRESS`: Your smart contract address
- `BACKEND_WALLET_ADDRESS`: Your backend wallet address
- `BACKEND_PRIVATE_KEY`: Your backend private key

## Deployment Steps

1. **Push your code to Git**:

   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

2. **Railway will automatically detect the changes and start building**

3. **Monitor the build logs** for any errors

4. **Check the deployment** once it's complete

## Common Issues and Solutions

### Build Failures

- **Virtual environment issues**: The `nixpacks.toml` file should handle this
- **Package conflicts**: Check `requirements.txt` for incompatible packages
- **Missing dependencies**: Ensure all required packages are in requirements.txt

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

### If app doesn't start:

1. Check Railway logs for runtime errors
2. Verify environment variables are set correctly
3. Ensure database is accessible
4. Check if all required services are running

## Support

If you continue to have issues, check:

- Railway documentation: https://docs.railway.app/
- Django deployment checklist: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
- Your application logs in Railway dashboard
