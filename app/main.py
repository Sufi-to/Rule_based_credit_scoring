from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Credit Scoring API", version="1.0.0")

class CreditRequest(BaseModel):
    user_id: int
    loan_id: int
    asset_value: float

class CreditResponse(BaseModel):
    user_id: int
    loan_id: int
    credit_score: int

def calculate_credit_score(asset_value: float, requested_amount: float) -> int:
    """
    Calculate credit score out of 100 based on asset value vs requested amount
    """
    if requested_amount <= 0:
        return 0
    
    # Calculate asset coverage ratio
    coverage_ratio = asset_value / requested_amount
    
    # Base score calculation
    if coverage_ratio >= 3.0:
        # Asset worth 3x+ the loan amount - excellent
        base_score = 95
    elif coverage_ratio >= 2.5:
        # Asset worth 2.5x+ the loan amount - very good
        base_score = 85
    elif coverage_ratio >= 2.0:
        # Asset worth 2x+ the loan amount - good
        base_score = 75
    elif coverage_ratio >= 1.5:
        # Asset worth 1.5x+ the loan amount - fair
        base_score = 65
    elif coverage_ratio >= 1.0:
        # Asset covers the loan amount exactly - minimum acceptable
        base_score = 50
    elif coverage_ratio >= 0.8:
        # Asset covers 80%+ of loan amount - risky
        base_score = 30
    elif coverage_ratio >= 0.5:
        # Asset covers 50%+ of loan amount - very risky
        base_score = 15
    else:
        # Asset covers less than 50% - unacceptable
        base_score = 5
    
    # Ensure score is within 0-100 range
    return min(100, max(0, base_score))

def determine_approval(credit_score: int, asset_value: float, requested_amount: float) -> tuple[bool, float, str]:
    """
    Determine loan approval based on credit score and asset coverage
    Returns: (approved, approved_amount, reason)
    """
    # Minimum requirement: asset value must equal or exceed requested amount
    if asset_value < requested_amount:
        return False, 0.0, f"Asset value ({asset_value}) is less than requested amount ({requested_amount}). Minimum requirement not met."
    
    # Additional check: minimum credit score of 50
    if credit_score < 50:
        return False, 0.0, f"Credit score ({credit_score}) is below minimum threshold of 50."
    
    # Approve full amount if requirements are met
    return True, requested_amount, "Loan approved - asset value covers requested amount and credit score meets minimum requirements."

@app.get("/")
def read_root():
    return {
        "message": "Credit Scoring API",
        "description": "Simple credit scoring based on asset value vs loan amount",
        "version": "1.0.0"
    }

@app.post("/evaluate_credit", response_model=CreditResponse)
def evaluate_credit(request: CreditRequest):
    """
    Evaluate credit application and return user info with calculated credit score
    Fixed requested amount: 100,000 for testing purposes
    """
    # Fixed requested amount for testing
    REQUESTED_AMOUNT = 100000.0
    
    try:
        # Validate input
        if request.asset_value < 0:
            raise HTTPException(status_code=400, detail="Asset value cannot be negative")
        
        # Calculate credit score
        credit_score = calculate_credit_score(request.asset_value, REQUESTED_AMOUNT)
        
        # Return response with credit score
        return CreditResponse(
            user_id=request.user_id,
            loan_id=request.loan_id,
            credit_score=credit_score
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "credit-scoring-api"}