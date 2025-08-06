# Railway Deployment Instructions

## Prerequisites
1. Create a Railway account: https://railway.app/
2. Install Railway CLI: `npm install -g @railway/cli`
3. Login to Railway: `railway login`

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
