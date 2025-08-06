# Railway Deployment Instructions

## Prerequisites
1. Create a Railway account: https://railway.app/
2. Install Railway CLI: `npm install -g @railway/cli`
3. Login to Railway: `railway login`

## Important Note on App Structure
This project uses a special import system to handle conflicts between the `app/` directory and `app.py` file:

1. The `app_loader.py` file dynamically imports from `app.py` to avoid conflicts
2. The `wsgi.py` file imports from `app_loader.py` instead of directly importing from `app.py` or `app/`
3. Do not modify these files unless you fully understand the import structure

## Deployment Steps

### 1. Backend Deployment
1. Navigate to the project directory
2. Run `railway init` to initialize a new Railway project
3. Run `railway up` to deploy the backend service

### 2. Frontend Integration
1. Run the build script: `./build_frontend.sh`
2. The frontend will be built and copied to the Flask app's static folder

### 3. Railway Environment Variables
Set these environment variables in the Railway dashboard:
- ENVIRONMENT=production
- FLASK_ENV=production
- ALLOWED_ORIGIN=https://your-railway-app-url.railway.app (replace with your actual URL)
- PORT=8080 (Railway will override this, but it's good to have it set)

To set environment variables in Railway:
1. Go to your Railway project dashboard
2. Click on your deployed service
3. Navigate to "Variables" in the left sidebar
4. Click "New Variable" to add each key-value pair
5. Enter the variable name and value, then click "Add"
6. After adding all variables, Railway will automatically redeploy your application

### Troubleshooting Deployment Issues
If you encounter issues during deployment:

1. **Import Errors**:
   - We've added mock implementations of functions in `app/utils.py` to maintain compatibility
   - Check Railway logs to identify any additional missing imports

2. **Build Failures**:
   - Make sure Node.js and npm are available for frontend building
   - The `railway.json` file includes a build command to handle frontend setup

3. **Runtime Errors**:
   - Check the health endpoint at `/api/health` to see if the server is running
   - Use Railway logs to diagnose specific errors in the application

### 4. Final Deployment
After setting up environment variables, deploy again:
```
railway up
```

### 5. Access Your Application
Once deployed, you can access your application through the URL provided by Railway.

## Updating Your Application
To update your application after making changes:
1. Build the frontend if there are frontend changes: `./build_frontend.sh`
2. Deploy the updated application: `railway up`
