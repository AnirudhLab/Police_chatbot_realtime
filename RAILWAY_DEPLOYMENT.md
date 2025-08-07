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

### 1. Build Frontend Locally
1. Navigate to the project directory
2. Make sure the prepare script is executable: `chmod +x prepare_for_railway.sh`
3. Run the prepare script: `./prepare_for_railway.sh`
4. This will build the frontend and copy it to the Flask app's static folder

### 2. Deploy to Railway
1. After building the frontend, run `railway init` to initialize a new Railway project
2. Run `railway up` to deploy the application

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

2. **Frontend Build Failures**:
   - Make sure to run the `prepare_for_railway.sh` script locally before deploying
   - Verify that your local Node.js and npm versions are working properly
   - Check that the static files have been properly copied to `app/static` directory

3. **Runtime Errors**:
   - Check the health endpoint at `/api/health` to see if the server is running
   - Use Railway logs to diagnose specific errors in the application
   - If you get a "Not Found" error, make sure the static files are in the correct location

4. **Command Not Found (Exit Code 127)**:
   - This usually means Railway couldn't find a command in the build script
   - We're now building the frontend locally to avoid this issue

### 4. Final Deployment
After setting up environment variables, deploy again:
```
railway up
```

### 5. Access Your Application
Once deployed, you can access your application through the URL provided by Railway.

## Updating Your Application
To update your application after making changes:
1. Build the frontend if there are frontend changes: `./prepare_for_railway.sh`
2. Deploy the updated application: `railway up`

## Alternative Deployment Option: Separate Frontend and Backend

If you continue to have issues with the combined deployment approach, you can deploy the frontend and backend separately:

### Backend Only Deployment
1. Deploy only the Flask backend to Railway using the current setup
2. This will provide the API endpoints at your Railway URL

### Frontend Separate Deployment
1. Navigate to the frontend directory: `cd frontend`
2. Update the API URL in App.js to point to your Railway backend:
   ```javascript
   const apiUrl = 'https://your-railway-app-url.railway.app/api/chat';
   ```
3. Build the frontend: `npm run build`
4. Deploy the frontend to a static hosting service like:
   - Netlify
   - Vercel
   - GitHub Pages
   - Firebase Hosting
5. Configure CORS in your Railway environment variables to allow requests from your frontend domain:
   - ALLOWED_ORIGIN=https://your-frontend-domain.com
