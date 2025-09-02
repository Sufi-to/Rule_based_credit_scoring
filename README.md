# Credit Scoring API

A simple FastAPI application that calculates credit scores based on asset values.

## 🚀 Quick Deploy to Render

### Option 1: Blueprint Deployment (Recommended)
1. **Fork/Clone** this repository
2. **Push** to your GitHub account
3. Go to [Render Dashboard](https://dashboard.render.com)
4. Click **"New +"** → **"Blueprint"**
5. **Connect** your repository
6. Render will auto-detect `render.yaml` and deploy!

### Option 2: Manual Web Service
1. Connect repository to Render
2. Create new **Web Service**
3. Use these settings:
   - **Runtime**: Python 3
   - **Build Command**: `pip install --upgrade pip==23.3.1 && pip install --no-compile --only-binary=all -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Features

- Calculate credit scores (0-100) based on asset value vs loan amount
- Fixed loan amount of 100,000 for testing
- RESTful API with automatic documentation
- Docker containerized for easy deployment
- Optimized for Render deployment (no Rust compilation)

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

### Test the API
```bash
# Test locally
python test_api_simple.py

# Test deployed version
python test_api_simple.py https://your-app.onrender.com
```

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

## Deployment Files

- `render.yaml` - Blueprint for one-click deployment
- `runtime.txt` - Python version specification
- `requirements.txt` - Optimized dependencies (no Rust compilation)
- `Dockerfile` - Container configuration
- `DEPLOYMENT_CHECKLIST.md` - Pre-deployment verification

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

## Troubleshooting

- **Build fails on Render**: Use simpler build command `pip install -r requirements.txt`
- **Rust compilation errors**: All dependencies are pure Python, should not occur
- **Import errors**: Check Python version is 3.11.6
- **Health check fails**: Verify `/health` endpoint responds with 200 status