#!/bin/bash

# Script to build frontend and prepare for Railway deployment

echo "Building frontend for production deployment..."

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "Installing npm packages..."
npm install

# Build the React app
echo "Building React application..."
npm run build

# Create static folder in Flask app if it doesn't exist
echo "Creating static folder in Flask app..."
mkdir -p ../app/static

# Copy build files to Flask static folder
echo "Copying build files to static folder..."
cp -r build/* ../app/static/

echo "Frontend build completed and copied to Flask app static folder."
echo "You can now deploy to Railway with 'railway up'"
