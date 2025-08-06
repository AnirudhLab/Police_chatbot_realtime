#!/bin/bash

# This script builds the React frontend and copies it to the Flask static folder

echo "Building React frontend..."
cd frontend
npm install
npm run build

echo "Creating static folder in Flask app if it doesn't exist..."
mkdir -p ../app/static

echo "Copying build files to Flask static folder..."
cp -r build/* ../app/static/

echo "Frontend build complete and copied to Flask static folder"
