#!/bin/bash

# Script to verify healthcheck endpoint
echo "Checking if application is running properly..."

# Wait a bit for the application to fully start
sleep 5

# Try to access the healthcheck endpoint
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/health)

echo "Healthcheck response code: $response"

if [ "$response" -eq 200 ]; then
    echo "Application is healthy!"
    exit 0
else
    echo "Application failed health check!"
    exit 1
fi
