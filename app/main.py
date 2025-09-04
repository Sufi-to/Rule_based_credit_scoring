from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Tuple, List, Dict, Any
from datetime import datetime

app = FastAPI(title="Credit Scoring API", version="2.0.0")

# Add CORS middleware to allow requests from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    #allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class DetectedAsset(BaseModel):
    asset_type: str
    asset_count: int
    asset_category: str
    condition_score: float
    estimated_value: float
    gps_coordinates: Optional[Any]
    device_model: str
    timestamp: str
    camera_make: str
    camera_model: str
    image_source: str
    detection_confidence: float
    exif_verified: bool

class AuthenticityVerification(BaseModel):
    images_with_exif: int
    images_without_exif: int
    evaluation_policy: str
    note: str

class Summary(BaseModel):
    unique_asset_types: int
    asset_categories_found: List[str]
    total_estimated_value: float
    has_location_data: bool
    devices_detected: List[str]
    exif_verification_rate: str
    authenticity_verification: AuthenticityVerification

class CreditFeatures(BaseModel):
    total_asset_value: float
    asset_diversity_score: int
    asset_categories: Dict[str, int]
    has_transport_asset: bool
    has_electronics_asset: bool
    has_livestock_asset: bool
    has_property_asset: bool
    has_high_value_assets: bool
    high_value_asset_count: int
    average_asset_condition: float
    location_stability_score: int
    primary_device_model: str
    primary_device_tier_score: int
    unique_devices_count: int
    asset_to_device_ratio: float
    image_span_days: int
    images_per_day: int
    has_recent_images: bool
    asset_concentration_score: int
    average_detection_confidence: float

class AnalysisResult(BaseModel):
    batch_id: str
    loan_id: str
    analysis_timestamp: str
    total_images_processed: int
    total_assets_detected: int
    credit_features: CreditFeatures
    detected_assets: List[DetectedAsset]
    summary: Summary

class CreditAnalysisRequest(BaseModel):
    message: str
    batch_id: str
    user_id: str
    status: str
    total_files: int
    estimated_completion_time: str
    status_check_url: str
    loan_id: str
    analysis_result: AnalysisResult

class CreditResponse(BaseModel):
    user_id: str
    loan_id: str
    credit_score: int

def calculate_comprehensive_credit_score(analysis_data: CreditAnalysisRequest) -> int:
    """
    Calculate comprehensive credit score using all available asset analysis data
    Score breakdown (out of 100):
    - Asset Value & Coverage (30 points)
    - Asset Quality & Condition (20 points)
    - Asset Diversity & Portfolio (15 points)
    - Data Authenticity & Verification (15 points)
    - Technology & Device Quality (10 points)
    - Temporal & Behavioral Factors (10 points)
    """
    score = 0
    credit_features = analysis_data.analysis_result.credit_features
    summary = analysis_data.analysis_result.summary
    
    # Fixed loan amount for comparison
    LOAN_AMOUNT = 100000.0
    
    # 1. Asset Value & Coverage (30 points)
    asset_value_score = 0
    coverage_ratio = credit_features.total_asset_value / LOAN_AMOUNT if LOAN_AMOUNT > 0 else 0
    
    if coverage_ratio >= 1.0:
        asset_value_score = 30  # Full coverage
    elif coverage_ratio >= 0.8:
        asset_value_score = 25  # 80%+ coverage
    elif coverage_ratio >= 0.6:
        asset_value_score = 20  # 60%+ coverage
    elif coverage_ratio >= 0.4:
        asset_value_score = 15  # 40%+ coverage
    elif coverage_ratio >= 0.2:
        asset_value_score = 10  # 20%+ coverage
    else:
        asset_value_score = 5   # Minimal coverage
    
    # Bonus for high-value assets
    if credit_features.has_high_value_assets:
        asset_value_score += min(5, credit_features.high_value_asset_count * 2)
    
    score += min(30, asset_value_score)
    
    # 2. Asset Quality & Condition (20 points)
    condition_score = 0
    avg_condition = credit_features.average_asset_condition
    
    if avg_condition >= 8.0:
        condition_score = 20  # Excellent condition
    elif avg_condition >= 7.0:
        condition_score = 17  # Very good condition
    elif avg_condition >= 6.0:
        condition_score = 14  # Good condition
    elif avg_condition >= 5.0:
        condition_score = 11  # Fair condition
    elif avg_condition >= 4.0:
        condition_score = 8   # Poor condition
    else:
        condition_score = 4   # Very poor condition
    
    # Detection confidence bonus
    confidence_bonus = min(3, int(credit_features.average_detection_confidence * 3))
    condition_score += confidence_bonus
    
    score += min(20, condition_score)
    
    # 3. Asset Diversity & Portfolio (15 points)
    diversity_score = 0
    
    # Base diversity score
    diversity_score += min(8, credit_features.asset_diversity_score * 2)
    
    # Category bonuses
    category_bonuses = 0
    if credit_features.has_transport_asset:
        category_bonuses += 2
    if credit_features.has_electronics_asset:
        category_bonuses += 2
    if credit_features.has_livestock_asset:
        category_bonuses += 2
    if credit_features.has_property_asset:
        category_bonuses += 3  # Property is most valuable
    
    diversity_score += min(7, category_bonuses)
    score += min(15, diversity_score)
    
    # 4. Data Authenticity & Verification (15 points)
    authenticity_score = 0
    
    # EXIF verification rate
    exif_rate_str = summary.exif_verification_rate.replace('%', '')
    exif_rate = float(exif_rate_str) if exif_rate_str else 0
    authenticity_score += int(exif_rate / 100 * 10)  # Up to 10 points for 100% EXIF
    
    # Multiple images and processing
    if analysis_data.analysis_result.total_images_processed > 1:
        authenticity_score += 2
    if analysis_data.analysis_result.total_assets_detected > 1:
        authenticity_score += 2
    
    # Location stability
    location_bonus = min(1, credit_features.location_stability_score / 10)
    authenticity_score += location_bonus
    
    score += min(15, authenticity_score)
    
    # 5. Technology & Device Quality (10 points)
    tech_score = 0
    
    # Device tier score
    device_tier_bonus = min(6, credit_features.primary_device_tier_score * 1.5)
    tech_score += device_tier_bonus
    
    # Asset to device ratio (indicates ownership patterns)
    if credit_features.asset_to_device_ratio > 2.0:
        tech_score += 2  # High asset-to-device ratio is positive
    elif credit_features.asset_to_device_ratio > 1.0:
        tech_score += 1
    
    # Multiple unique devices
    if credit_features.unique_devices_count > 1:
        tech_score += 2
    
    score += min(10, tech_score)
    
    # 6. Temporal & Behavioral Factors (10 points)
    temporal_score = 0
    
    # Recent images indicate active engagement
    if credit_features.has_recent_images:
        temporal_score += 3
    
    # Asset concentration (focused vs scattered approach)
    if credit_features.asset_concentration_score >= 80:
        temporal_score += 2  # Focused asset strategy
    
    # Image frequency patterns
    if credit_features.images_per_day >= 1:
        temporal_score += 2
    
    # Image span indicates documentation consistency
    if credit_features.image_span_days > 0:
        temporal_score += min(3, credit_features.image_span_days / 10)
    
    score += min(10, temporal_score)
    
    # Final adjustments and caps
    final_score = min(100, max(0, score))
    
    return int(final_score)

@app.get("/")
def read_root():
    return {
        "message": "Advanced Credit Scoring API",
        "description": "Comprehensive credit scoring using asset analysis data",
        "version": "2.0.0",
        "features": [
            "Asset value and coverage analysis",
            "Asset quality and condition scoring",
            "Portfolio diversity assessment",
            "Data authenticity verification",
            "Technology and device quality evaluation",
            "Temporal and behavioral pattern analysis"
        ]
    }

@app.post("/evaluate_credit", response_model=CreditResponse)
def evaluate_credit(request: CreditAnalysisRequest):
    """
    Evaluate credit application using comprehensive asset analysis data
    Returns credit score out of 100 based on multiple factors
    """
    try:
        # Validate input
        if request.analysis_result.credit_features.total_asset_value < 0:
            raise HTTPException(status_code=400, detail="Asset value cannot be negative")
        
        if not request.analysis_result.detected_assets:
            raise HTTPException(status_code=400, detail="No assets detected in analysis")
        
        # Calculate comprehensive credit score
        credit_score = calculate_comprehensive_credit_score(request)
        
        # Return response with credit score
        return CreditResponse(
            user_id=request.user_id,
            loan_id=request.loan_id,
            credit_score=credit_score
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing credit evaluation: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "credit-scoring-api"}