# Credit Scoring API

A simple FastAPI application that calculates credit scores based on asset values.

## Features

- Calculate credit scores (0-100) based on asset value vs loan amount
- Fixed loan amount of 100,000 for testing
- RESTful API with automatic documentation
- Docker containerized for easy deployment

## API Endpoints

- `POST /evaluate_credit` - Calculate credit score
- `GET /` - API information
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

## Local Development

### Using Python directly
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Using Docker
```bash
# Build the image
docker build -t credit-scoring-api .

# Run the container
docker run -p 8000:8000 credit-scoring-api

# Or use docker-compose
docker-compose up --build
```

## Deployment on Render

### Option 1: Docker Deployment (Recommended)
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Select "Docker" as the environment
4. Render will automatically detect and use the Dockerfile
5. The service will be available at your Render URL

### Option 2: Native Python Deployment
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Use these settings:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## API Usage Example

### Request
```bash
curl -X POST "https://your-render-url.com/evaluate_credit" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 123,
    "loan_id": 456,
    "asset_value": 150000.0
  }'
```

### Response
```json
{
  "user_id": 123,
  "loan_id": 456,
  "credit_score": 65
}
```

## Credit Scoring Logic

The API calculates credit scores based on the ratio of asset value to the fixed loan amount (100,000):

- **95 points**: Asset value ≥ 300,000 (3x+ coverage)
- **85 points**: Asset value ≥ 250,000 (2.5x+ coverage)
- **75 points**: Asset value ≥ 200,000 (2x+ coverage)
- **65 points**: Asset value ≥ 150,000 (1.5x+ coverage)
- **50 points**: Asset value ≥ 100,000 (1x coverage)
- **30 points**: Asset value ≥ 80,000 (0.8x coverage)
- **15 points**: Asset value ≥ 50,000 (0.5x coverage)
- **5 points**: Asset value < 50,000 (insufficient coverage)

## Environment Variables

No environment variables are required for basic operation. The application uses:
- Fixed loan amount: 100,000
- Default port: 8000 (configurable via `$PORT` environment variable)

## Health Check

The application includes a health check endpoint at `/health` that returns:
```json
{
  "status": "healthy",
  "service": "credit-scoring-api"
}
```