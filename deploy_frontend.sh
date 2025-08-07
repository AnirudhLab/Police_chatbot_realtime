#!/bin/bash

# Script to deploy frontend to Railway

echo "Preparing frontend for Railway deployment..."

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "Installing npm packages..."
npm install

# Create a Dockerfile for the frontend
cat > Dockerfile << 'EOF'
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
EOF

# Create nginx configuration
cat > nginx.conf << 'EOF'
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
EOF

# Create railway.json
cat > railway.json << 'EOF'
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
EOF

echo "Frontend files prepared for Railway deployment."
echo ""
echo "To deploy:"
echo "1. Navigate to the frontend directory: cd frontend"
echo "2. Login to Railway if not already: railway login"
echo "3. Link to a new project: railway init"
echo "4. Deploy: railway up"
echo ""
echo "After deployment, Railway will provide a URL for your frontend."
