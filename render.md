# Render Deployment Configuration

## Environment Variables
Set these in your Render service:
- `PYTHON_VERSION`: 3.11.6 (specified in runtime.txt)
- `PORT`: 8000 (Render will set this automatically)

## Build Command (Choose ONE)
**Option 1 (Recommended - No Rust compilation):**
```bash
pip install --upgrade pip==23.3.1 && pip install --no-compile --only-binary=all -r requirements.txt
```

**Option 2 (Alternative):**
```bash
pip install --no-compile -r requirements.txt
```

**Option 3 (Simple fallback):**
```bash
pip install -r requirements.txt
```

## Start Command
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Key Changes Made
- Downgraded to Pydantic v1.10.12 (no Rust required)
- Using FastAPI 0.95.2 (stable, compatible)
- Added `--no-compile` flag to prevent any compilation
- Updated type hints for Python 3.11 compatibility

## Docker Deployment
1. Connect your GitHub repository to Render
2. Select "Docker" as the environment
3. Render will automatically use the Dockerfile
4. Set the port to 8000 in the service settings

## Troubleshooting Build Issues

If you still encounter compilation errors:
1. Use Option 2 build command (simpler)
2. Make sure runtime.txt has Python 3.11.6
3. The new package versions avoid all Rust dependencies

## Health Check Endpoint
- URL: `/health`
- Expected response: `{"status": "healthy", "service": "credit-scoring-api"}`

## API Documentation
- Swagger UI: `/docs`
- OpenAPI JSON: `/openapi.json`
