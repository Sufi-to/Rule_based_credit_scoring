# Credit Scoring API

A simple FastAPI application that calculates credit scores based on asset values.

## 🚀 Deploy to Render (Web Service)

### Step-by-Step Deployment
1. **Push** this repository to your GitHub account
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click **"New +"** → **"Web Service"**
4. **Connect** your GitHub repository
5. Configure the service:
   - **Name**: `credit-scoring-api`
   - **Runtime**: `Python 3`
   - **Build Command**: `bash build.sh`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free` (for testing) or `Starter` ($7/month)
6. **Add Environment Variable**:
   - **Key**: `PYTHON_VERSION`
   - **Value**: `3.10.12`
7. Click **"Create Web Service"**
7. Wait for deployment (2-3 minutes)
8. Your API will be live at: `https://your-service-name.onrender.com`

## Features

- Calculate credit scores (0-100) based on asset value vs loan amount
- Fixed loan amount of 100,000 for testing
- RESTful API with automatic documentation
- Optimized for Render deployment (no Rust compilation)
- Health check endpoint for monitoring

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
curl -X POST "https://your-service-name.onrender.com/evaluate_credit" \
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

## Technical Specifications

- **Python Version**: 3.11.6 (specified in `runtime.txt`)
- **Framework**: FastAPI 0.95.2 (stable, no Rust dependencies)
- **ASGI Server**: Uvicorn 0.22.0
- **Data Validation**: Pydantic 1.10.12 (pure Python)

## Deployment Files

- `runtime.txt` - Python version specification for Render
- `requirements.txt` - Optimized dependencies (no Rust compilation)
- `render.md` - Detailed deployment instructions
- `Dockerfile` - Container configuration for Docker deployment

## Environment Variables

No environment variables are required. The application uses:
- **Fixed loan amount**: 100,000
- **Port**: Automatically set by Render via `$PORT`

## Health Check

The application includes a health check endpoint at `/health`:
```json
{
  "status": "healthy",
  "service": "credit-scoring-api"
}
```

## Troubleshooting

- **Build fails on Render**: Try fallback command `pip install -r requirements.txt`
- **Service won't start**: Verify start command is exactly `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health check fails**: Test `/health` endpoint returns 200 status
- **Import errors**: Ensure Python 3.11.6 is specified in `runtime.txt`