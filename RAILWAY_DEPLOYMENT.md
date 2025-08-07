# Simplified Railway Deployment Instructions

## Prerequisites
1. Create a Railway account: https://railway.app/
2. Install Railway CLI: `npm install -g @railway/cli`
3. Login to Railway: `railway login`

## Simplified Deployment Approach
For more reliable deployment, we'll use a simplified approach:

1. Deploy only the backend API to Railway
2. Deploy the frontend separately to a static hosting service (Netlify, Vercel, etc.)

This separation makes troubleshooting easier and reduces complexity.

## Backend Deployment Steps

### 1. Prepare Backend for Deployment
1. Create a minimal `railway.json` file:
   ```bash
   cat > railway.json << 'EOF'
   {
     "$schema": "https://railway.app/railway.schema.json",
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "gunicorn app:create_app() --bind=0.0.0.0:$PORT",
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10
     }
   }
   EOF
   ```

### 2. Deploy Backend to Railway
1. Run `railway login` to authenticate (if not already logged in)
2. Run `railway init` to create a new project
3. Run `railway up` to deploy the backend API

### 3. Backend Environment Variables
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

### 4. Test the Backend API
1. After deployment, Railway will provide a URL for your application
2. Test the API endpoint with cURL:
   ```bash
   curl -X POST https://your-railway-url.railway.app/api/chat \
     -H "Content-Type: application/json" \
     -d '{"query":"What is IPC?", "language":"en"}'
   ```

### 5. Frontend Deployment Steps
1. Navigate to the frontend directory: `cd frontend`
2. Update the API URL in App.js to point to your Railway backend:
   ```javascript
   const apiUrl = process.env.NODE_ENV === 'production' 
     ? 'https://your-railway-url.railway.app/api/chat' 
     : 'http://localhost:5000/api/chat';
   ```
3. Build the frontend: `npm run build`
4. Deploy to a static hosting service:
   - **Netlify**: Use the Netlify CLI or connect your GitHub repo
   - **Vercel**: Use the Vercel CLI or connect your GitHub repo
   - **GitHub Pages**: Configure GitHub Pages in your repository settings
   - **Firebase Hosting**: Use the Firebase CLI to deploy

### 6. Configure CORS for Frontend
After deploying your frontend, update the ALLOWED_ORIGIN environment variable in Railway:
- ALLOWED_ORIGIN=https://your-frontend-domain.com

### Troubleshooting Backend Deployment
If you encounter issues:

1. **Simplify the API Endpoint**:
   - Create a simple test endpoint in app.py to verify the server works
   
2. **Check Logs**:
   - Use `railway logs` to view error messages

3. **Verify Data Files**:
   - Upload your data files to the server using Railway variables or add a placeholder

4. **Remove Complex Dependencies**:
   - If a specific package is causing issues, try removing it temporarily

## Updating Your Application

### Backend Updates
1. Make changes to your backend code
2. Deploy changes with: `railway up`

### Frontend Updates
1. Make changes to your frontend code
2. Rebuild the frontend: `cd frontend && npm run build`
3. Redeploy to your static hosting service

## Extremely Simplified Approach (If Still Having Issues)

If you're still having issues with Railway, here's an even simpler approach:

### Deploy a Minimal API First
1. Create a new directory: `mkdir minimal-api`
2. Create a basic Flask app:
   ```python
   # app.py
   from flask import Flask, jsonify
   
   app = Flask(__name__)
   
   @app.route('/api/test', methods=['GET'])
   def test():
       return jsonify({"message": "API is working!"})
   
   if __name__ == '__main__':
       app.run()
   ```
3. Create a minimal railway.json:
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "gunicorn app:app --bind=0.0.0.0:$PORT",
       "restartPolicyType": "ON_FAILURE"
     }
   }
   ```
4. Create a minimal requirements.txt:
   ```
   flask
   gunicorn
   ```
5. Deploy this minimal API first to ensure Railway is working properly
6. Then gradually add your actual API functionality
