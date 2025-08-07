#!/bin/bash

# Script to build frontend and prepare for Railway deployment

echo "Building frontend for production deployment..."

# Make sure data directory exists
echo "Checking data directory..."
mkdir -p data
if [ ! -f "data/Police_Chatbot_Legal_Template.xlsx" ]; then
    echo "Creating placeholder data file..."
    echo '{"columns":["Law Type","Law Name/Section","Law Details","When Applicable","Legal Reference"],"data":[["Example","Section 1","This is an example law","When relevant","Legal Code 1"]]}' > data/placeholder_data.json
fi

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
