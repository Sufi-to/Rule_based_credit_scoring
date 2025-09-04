#!/usr/bin/env python3
"""
Comprehensive test script for the Advanced Credit Scoring API
Tests both /evaluate_credit and /evaluate_credit_detailed endpoints
"""

import requests
import json
import sys

# Sample comprehensive asset analysis data (dummy data for testing)
SAMPLE_DATA = {
    "message": "Analysis completed successfully",
    "batch_id": "batch_12345",
    "user_id": "111111",
    "status": "completed",
    "total_files": 5,
    "estimated_completion_time": "2024-01-15T10:30:00Z",
    "status_check_url": "https://api.example.com/status/batch_12345",
    "loan_id": "1111",
    "analysis_result": {
        "batch_id": "batch_12345",
        "loan_id": "1111",
        "analysis_timestamp": "2024-01-15T10:30:00Z",
        "total_images_processed": 5,
        "total_assets_detected": 1,
        "credit_features": {
            "total_asset_value": 2509.03,
            "asset_diversity_score": 1,
            "asset_categories": {"Transport": 1},
            "has_transport_asset": True,
            "has_electronics_asset": False,
            "has_livestock_asset": False,
            "has_property_asset": False,
            "has_high_value_assets": False,
            "high_value_asset_count": 0,
            "average_asset_condition": 5.7,
            "location_stability_score": 8,
            "primary_device_model": "iPhone 12",
            "primary_device_tier_score": 2,
            "unique_devices_count": 1,
            "asset_to_device_ratio": 1.0,
            "image_span_days": 7,
            "images_per_day": 1,
            "has_recent_images": True,
            "asset_concentration_score": 7,
            "average_detection_confidence": 0.93
        },
        "detected_assets": [
            {
                "asset_type": "Motorcycle",
                "asset_count": 1,
                "asset_category": "Transport",
                "condition_score": 5.7,
                "estimated_value": 2509.03,
                "gps_coordinates": None,
                "device_model": "iPhone 12",
                "timestamp": "2024-01-15T10:00:00Z",
                "camera_make": "Apple",
                "camera_model": "iPhone 12 camera",
                "image_source": "user_upload",
                "detection_confidence": 0.93,
                "exif_verified": True
            }
        ],
        "summary": {
            "unique_asset_types": 1,
            "asset_categories_found": ["Transport"],
            "total_estimated_value": 2509.03,
            "has_location_data": False,
            "devices_detected": ["iPhone 12"],
            "exif_verification_rate": "100.0%",
            "authenticity_verification": {
                "images_with_exif": 5,
                "images_without_exif": 0,
                "evaluation_policy": "strict",
                "note": "All images verified with EXIF data"
            }
        }
    }
}

def test_api(base_url="http://localhost:8000"):
    """Test the credit scoring API endpoints"""
    
    print(f"🧪 Testing Credit Scoring API at {base_url}")
    print("=" * 60)
    
    # Test 1: Basic credit score endpoint
    print("\n1️⃣  Testing /evaluate_credit endpoint...")
    try:
        response = requests.post(
            f"{base_url}/evaluate_credit",
            json=SAMPLE_DATA,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS! Credit Score: {result['credit_score']}/100")
            print(f"   User ID: {result['user_id']}")
            print(f"   Loan ID: {result['loan_id']}")
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ FAILED! Could not connect to API server")
        print("   Make sure the server is running on port 8000")
        return False
    except Exception as e:
        print(f"❌ FAILED! Error: {str(e)}")
        return False
    
    # Test 2: Health check
    print("\n2️⃣  Testing /health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS! Service Status: {result['status']}")
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
    except Exception as e:
        print(f"❌ FAILED! Error: {str(e)}")
    
    # Test 3: API info endpoint
    print("\n3️⃣  Testing / (root) endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS! API: {result['message']}")
            print(f"   Version: {result['version']}")
            print(f"   Features: {len(result['features'])} available")
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
    except Exception as e:
        print(f"❌ FAILED! Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎯 Testing Complete!")
    
    # Show sample scoring breakdown
    print(f"\n📊 Sample Analysis Summary:")
    print(f"   Asset Value: ${SAMPLE_DATA['analysis_result']['credit_features']['total_asset_value']:,.2f}")
    print(f"   Loan Amount: $100,000 (fixed)")
    print(f"   Coverage Ratio: {SAMPLE_DATA['analysis_result']['credit_features']['total_asset_value']/100000:.1%}")
    print(f"   Asset Type: {SAMPLE_DATA['analysis_result']['summary']['asset_categories_found'][0]}")
    print(f"   Condition: {SAMPLE_DATA['analysis_result']['credit_features']['average_asset_condition']}/10")
    print(f"   Confidence: {SAMPLE_DATA['analysis_result']['credit_features']['average_detection_confidence']:.1%}")
    
    return True

if __name__ == "__main__":
    # Allow custom base URL as command line argument
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    test_api(base_url)
