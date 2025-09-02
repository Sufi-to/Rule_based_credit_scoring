# Render Web Service Deployment Guide

## Build Command (Try in this order)
**Option 1 (Recommended):**
```bash
bash build.sh
```

**Option 2 (Fallback):**
```bash
pip install --upgrade pip==23.2.1 && pip install --no-cache-dir -r requirements.txt
```

**Option 3 (Simple):**
```bash
pip install -r requirements.txt
```

## Start Command
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Environment Variables (Set these in Render)
- `PYTHON_VERSION`: `3.10.12`
- `PORT`: Auto-set by Render

## Deployment Steps
1. Push your code to GitHub
2. Go to Render Dashboard
3. Click "New +" → "Web Service"
4. Connect your GitHub repository: `Rule_based_credit_scoring`
5. Configure service:
   - **Name**: `credit-scoring-api`
   - **Runtime**: `Python 3`
   - **Build Command**: `bash build.sh`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free` or `Starter`
6. **Add Environment Variable**: 
   - Key: `PYTHON_VERSION`
   - Value: `3.10.12`
7. Click "Create Web Service"

## Health Check
- Path: `/health`
- Expected response: `{"status": "healthy", "service": "credit-scoring-api"}`

## API Endpoints
- `POST /evaluate_credit` - Main scoring endpoint
- `GET /health` - Health check
- `GET /docs` - Interactive documentation
- `GET /` - API information

## Troubleshooting
- **Build fails**: Try Option 2 or 3 build commands
- **Python version issues**: Ensure `PYTHON_VERSION=3.10.12` is set
- **App won't start**: Verify start command syntax is correct
