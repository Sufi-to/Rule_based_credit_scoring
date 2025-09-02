# Render Web Service Deployment Guide

## Build Command
```bash
pip install -r requirements.txt
```

## Start Command
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Environment Variables
- `PYTHON_VERSION`: 3.11.9 (auto-detected from runtime.txt)
- `PORT`: Auto-set by Render

## Deployment Steps
1. Push your code to GitHub
2. Go to Render Dashboard
3. Click "New +" → "Web Service"
4. Connect your GitHub repository: `Rule_based_credit_scoring`
5. Configure service:
   - **Name**: `credit-scoring-api`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free` or `Starter`
6. Click "Create Web Service"

## Health Check
- Path: `/health`
- Expected response: `{"status": "healthy", "service": "credit-scoring-api"}`

## API Endpoints
- `POST /evaluate_credit` - Main scoring endpoint
- `GET /health` - Health check
- `GET /docs` - Interactive documentation
- `GET /` - API information

## Troubleshooting
- **Build fails**: Ensure runtime.txt has correct Python version
- **App won't start**: Verify start command syntax is correct
- **Health check fails**: Test `/health` endpoint locally first
