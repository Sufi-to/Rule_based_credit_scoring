#!/usr/bin/env python3
"""
Simple test script for the Credit Scoring API
"""
import requests
import json

def test_api(base_url="http://localhost:8000"):
    """Test all API endpoints"""
    
    print(f"Testing API at: {base_url}")
    print("=" * 50)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health Check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return
    
    # Test 2: Root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Root Endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Root Endpoint Failed: {e}")
    
    # Test 3: Credit evaluation
    test_cases = [
        {"user_id": 123, "loan_id": 456, "asset_value": 150000.0},  # Should get score 65
        {"user_id": 124, "loan_id": 457, "asset_value": 100000.0},  # Should get score 50
        {"user_id": 125, "loan_id": 458, "asset_value": 50000.0},   # Should get score 15
        {"user_id": 126, "loan_id": 459, "asset_value": 300000.0},  # Should get score 95
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(
                f"{base_url}/evaluate_credit",
                headers={"Content-Type": "application/json"},
                json=test_case
            )
            result = response.json()
            print(f"✅ Test Case {i}: Asset {test_case['asset_value']:,} → Score {result['credit_score']}")
        except Exception as e:
            print(f"❌ Test Case {i} Failed: {e}")
    
    print("=" * 50)
    print("Testing complete!")

if __name__ == "__main__":
    import sys
    
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    test_api(base_url)
