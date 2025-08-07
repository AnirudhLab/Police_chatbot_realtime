# Railway Deployment Instructions for Police Chatbot

## Overview
The Police Chatbot application consists of two parts:
1. Backend API (Flask) - Already deployed at `policechatbotrealtime-production.up.railway.app`
2. Frontend (React) - To be deployed separately

## Backend (Already Deployed)
The backend API is already deployed at:
- URL: `https://policechatbotrealtime-production.up.railway.app`
- API endpoint: `https://policechatbotrealtime-production.up.railway.app/api/chat`

### Testing the Backend API
You can test the backend API using cURL:
```bash
curl -X POST https://policechatbotrealtime-production.up.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"What is IPC?", "language":"en"}'
```

## Frontend Deployment to Railway

### Prerequisites
1. Railway account: https://railway.app/
2. Railway CLI: `npm install -g @railway/cli`
3. Login to Railway: `railway login`

### Option 1: Automated Deployment

We've created a script to automate the frontend deployment process:

1. Run the deployment script:
   ```bash
   ./deploy_frontend.sh
   ```

2. Follow the instructions displayed after running the script:
   ```bash
   cd frontend
   railway init  # Creates a new project
   railway up    # Deploys the frontend
   ```

3. After deployment, Railway will provide a URL for your frontend application

### Option 2: Manual Deployment

If you prefer to deploy manually:

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Create a Dockerfile:
   ```dockerfile
   FROM node:16-alpine as build
   
   WORKDIR /app
   COPY package*.json ./
   RUN npm install
   COPY . .
   RUN npm run build
   
   FROM nginx:alpine
   COPY --from=build /app/build /usr/share/nginx/html
   COPY nginx.conf /etc/nginx/conf.d/default.conf
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

3. Create an nginx configuration:
   ```
   server {
       listen 80;
       
       location / {
           root /usr/share/nginx/html;
           index index.html index.htm;
           try_files $uri $uri/ /index.html =404;
       }
       
       # This is for handling the API calls to our backend
       location /api/ {
           proxy_pass https://policechatbotrealtime-production.up.railway.app/api/;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. Create a railway.json file:
   ```json
   {
     "$schema": "https://railway.app/railway.schema.json",
     "build": {
       "builder": "DOCKERFILE",
       "dockerfile": "Dockerfile"
     },
     "deploy": {
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10
     }
   }
   ```

5. Deploy to Railway:
   ```bash
   railway init  # Creates a new project
   railway up    # Deploys the frontend
   ```

## After Deployment

1. Update CORS settings on the backend:
   - Go to your backend Railway project dashboard
   - Click on Variables
   - Set `ALLOWED_ORIGIN` to your frontend URL (e.g., https://your-frontend-app.railway.app)
   
2. Test the complete application by accessing the frontend URL provided by Railway

## Troubleshooting

1. CORS Issues:
   - Check the `ALLOWED_ORIGIN` environment variable on the backend
   - Make sure it includes the full frontend URL (including protocol)

2. API Connection Issues:
   - Verify the API URL in App.js is correct
   - Check browser console for any network errors

3. Railway Deployment Issues:
   - Check Railway logs: `railway logs`
   - Make sure all dependencies are correctly installed
   - Ensure railway.json configuration is correct
