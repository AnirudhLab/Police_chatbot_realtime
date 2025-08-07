## Minimal Railway Deployment Steps

### Option 1: Deploy the Current Backend

1. Use the following railway.json:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn 'app:create_app()' --bind=0.0.0.0:$PORT --log-level debug",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

2. Run:
```bash
railway up
```

### Option 2: Try the Minimal Backend First

If Option 1 still has issues, try this minimal approach:

1. Rename app_minimal.py to app.py:
```bash
cp app_minimal.py app.py
```

2. Create a simplified requirements.txt:
```bash
echo -e "Flask\nFlask-Cors\ngunicorn" > requirements_minimal.txt
mv requirements_minimal.txt requirements.txt
```

3. Deploy to Railway:
```bash
railway up
```

### Deploy Frontend Separately

After the backend is deployed:

1. Get your Railway URL from the dashboard
2. Edit the frontend/src/App.js.railway file:
   - Replace "your-railway-app-url.railway.app" with your actual Railway URL
   - Save it as App.js: `cp frontend/src/App.js.railway frontend/src/App.js`

3. Build and deploy the frontend to a static hosting service like Netlify or Vercel
