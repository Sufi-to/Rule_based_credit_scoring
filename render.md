# Render Deployment Configuration

## Environment Variables
Set these in your Render service:
- `PYTHON_VERSION`: 3.11.6 (specified in runtime.txt)
- `PORT`: 8000 (Render will set this automatically)

## Build Command
**Option 1 (Recommended):**
```bash
./build.sh
```

**Option 2 (Alternative):**
```bash
pip install --upgrade pip==23.3.1 && pip install --only-binary=all -r requirements.txt
```

## Start Command
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Docker Deployment
1. Connect your GitHub repository to Render
2. Select "Docker" as the environment
3. Render will automatically use the Dockerfile
4. Set the port to 8000 in the service settings

## Troubleshooting Build Issues

If you encounter Rust/maturin compilation errors:
1. Use the custom build script: `./build.sh`
2. Ensure `runtime.txt` specifies Python 3.11.6
3. The build script forces binary-only installation to avoid compilation

## Health Check Endpoint
- URL: `/health`
- Expected response: `{"status": "healthy", "service": "credit-scoring-api"}`

## API Documentation
- Swagger UI: `/docs`
- OpenAPI JSON: `/openapi.json`
