# Advanced Credit Scoring API

A sophisticated FastAPI application that calculates credit scores using comprehensive asset analysis data including image verification, device authentication, and multi-factor risk assessment.

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

- **Comprehensive Credit Scoring** (0-100) using multiple factors:
  - Asset value and loan coverage analysis
  - Asset quality and condition assessment
  - Portfolio diversity evaluation
  - Data authenticity and EXIF verification
  - Technology and device quality scoring
  - Temporal and behavioral pattern analysis
- **Advanced Asset Analysis** processing
- **EXIF metadata verification** for authenticity
- **Multi-device detection** and scoring
- **RESTful API** with automatic documentation
- **CORS enabled** for cross-origin requests

## API Endpoints

- `POST /evaluate_credit` - Calculate credit score
- `GET /` - API information and features
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
# Test locally (with comprehensive data)
python comprehensive_test.py

# Test deployed version
python comprehensive_test.py https://your-app.onrender.com
```

## Scoring Algorithm (100 Points Total)

### 1. Asset Value & Coverage (30 points)
- Loan coverage ratio analysis
- High-value asset bonuses
- Portfolio value assessment

### 2. Asset Quality & Condition (20 points)
- Average asset condition scoring
- Detection confidence weighting
- Quality verification

### 3. Asset Diversity & Portfolio (15 points)
- Asset category diversity
- Transport, Electronics, Livestock, Property assets
- Portfolio balance assessment

### 4. Data Authenticity & Verification (15 points)
- EXIF metadata verification rate
- Multi-image processing validation
- Location stability scoring

### 5. Technology & Device Quality (10 points)
- Device tier and quality assessment
- Asset-to-device ratio analysis
- Multi-device ownership patterns

### 6. Temporal & Behavioral Factors (10 points)
- Recent image activity
- Asset concentration patterns
- Documentation consistency

## Input Data Structure

The API expects comprehensive asset analysis data including:

```json
{
  "user_id": "string",
  "loan_id": "string", 
  "analysis_result": {
    "credit_features": {
      "total_asset_value": 0.0,
      "asset_diversity_score": 0,
      "has_transport_asset": true,
      "has_electronics_asset": false,
      "average_asset_condition": 0.0,
      "average_detection_confidence": 0.0,
      "primary_device_tier_score": 0,
      // ... additional features
    },
    "detected_assets": [...],
    "summary": {
      "exif_verification_rate": "100.0%",
      // ... additional summary data
    }
  }
}
```

## API Usage Example

### Request
```bash
curl -X POST "https://your-service-name.onrender.com/evaluate_credit" \
  -H "Content-Type: application/json" \
  -d @sample_analysis_data.json
```

### Response
```json
{
  "user_id": "111111",
  "loan_id": "1111", 
  "credit_score": 45
}
```

Let me test the updated API quickly:

## Technical Specifications

- **Python Version**: 3.10.12 (specified in `runtime.txt`)
- **Framework**: FastAPI 0.95.2 (stable, proven)
- **ASGI Server**: Uvicorn 0.22.0
- **Data Validation**: Pydantic 1.10.7 (pure Python)
- **Scoring Engine**: Multi-factor analysis with 6 categories

## Deployment Files

- `runtime.txt` - Python version specification for Render
- `requirements.txt` - Stable dependencies
- `render.md` - Detailed deployment instructions
- `build.sh` - Custom build script
- `Dockerfile` - Container configuration

## Environment Variables

No environment variables are required. The application uses:
- **Fixed loan amount**: 100,000 (for ratio calculations)
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
- **Service won't start**: Verify start command and Python version
- **Invalid input data**: Check API documentation at `/docs`
- **Low scores**: Review asset value, condition, and verification data