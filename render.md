# Render Deployment Configuration

## Environment Variables
Set these in your Render service:
- `PYTHON_VERSION`: 3.12
- `PORT`: 8000 (Render will set this automatically)

## Build Command
```bash
pip install -r requirements.txt
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

## Health Check Endpoint
- URL: `/health`
- Expected response: `{"status": "healthy", "service": "credit-scoring-api"}`

## API Documentation
- Swagger UI: `/docs`
- OpenAPI JSON: `/openapi.json`
