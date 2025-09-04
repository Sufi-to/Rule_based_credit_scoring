#!/usr/bin/env python3
"""
Test script for the Advanced Credit Scoring API
"""
import requests
import json

def get_sample_data():
    """Sample data matching the expected structure"""
    return {
        "message": "Batch processed successfully",
        "batch_id": "9f151a41-6e8a-46a1-9e96-a8e2b06e05ee",
        "user_id": "111111",
        "status": "completed",
        "total_files": 1,
        "estimated_completion_time": "Completed",
        "status_check_url": "/analysis/batch/9f151a41-6e8a-46a1-9e96-a8e2b06e05ee/status",
        "loan_id": "1111",
        "analysis_result": {
            "batch_id": "9f151a41-6e8a-46a1-9e96-a8e2b06e05ee",
            "loan_id": "1111",
            "analysis_timestamp": "2025-09-04T13:41:10.738326",
            "total_images_processed": 1,
            "total_assets_detected": 1,
            "credit_features": {
                "total_asset_value": 2509.03,
                "asset_diversity_score": 1,
                "asset_categories": {
                    "Transport": 1
                },
                "has_transport_asset": True,
                "has_electronics_asset": False,
                "has_livestock_asset": False,
                "has_property_asset": False,
                "has_high_value_assets": True,
                "high_value_asset_count": 1,
                "average_asset_condition": 5.7,
                "location_stability_score": 10,
                "primary_device_model": "Galaxy S25",
                "primary_device_tier_score": 50,
                "unique_devices_count": 1,
                "asset_to_device_ratio": 50.18,
                "image_span_days": 0,
                "images_per_day": 1,
                "has_recent_images": False,
                "asset_concentration_score": 100,
                "average_detection_confidence": 0.93
            },
            "detected_assets": [
                {
                    "asset_type": "car",
                    "asset_count": 1,
                    "asset_category": "Transport",
                    "condition_score": 5.7,
                    "estimated_value": 2509.03,
                    "gps_coordinates": None,
                    "device_model": "Galaxy S25",
                    "timestamp": "2025-07-26T14:29:18",
                    "camera_make": "samsung",
                    "camera_model": "Galaxy S25",
                    "image_source": "e6a9b5db-f32e-40bc-8c13-dadb75591b18.jpg",
                    "detection_confidence": 0.929868221282959,
                    "exif_verified": True
                }
            ],
            "summary": {
                "unique_asset_types": 1,
                "asset_categories_found": ["Transport"],
                "total_estimated_value": 2509.03,
                "has_location_data": False,
                "devices_detected": ["Galaxy S25"],
                "exif_verification_rate": "100.0%",
                "authenticity_verification": {
                    "images_with_exif": 1,
                    "images_without_exif": 0,
                    "evaluation_policy": "Asset evaluation requires EXIF metadata for authenticity verification",
                    "note": "All images passed EXIF verification"
                }
            }
        }
    }

def get_high_value_sample():
    """Sample with higher asset value for comparison"""
    data = get_sample_data()
    data["user_id"] = "222222"
    data["loan_id"] = "2222"
    data["analysis_result"]["credit_features"]["total_asset_value"] = 150000.0
    data["analysis_result"]["credit_features"]["has_property_asset"] = True
    data["analysis_result"]["credit_features"]["has_electronics_asset"] = True
    data["analysis_result"]["credit_features"]["asset_diversity_score"] = 3
    data["analysis_result"]["credit_features"]["average_asset_condition"] = 8.5
    data["analysis_result"]["summary"]["total_estimated_value"] = 150000.0
    return data

def test_api(base_url="http://localhost:8000"):
    """Test all API endpoints"""
    
    print(f"Testing Advanced Credit Scoring API at: {base_url}")
    print("=" * 60)
    
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
        result = response.json()
        print(f"✅ Root Endpoint: {response.status_code}")
        print(f"   Version: {result.get('version')}")
        print(f"   Features: {len(result.get('features', []))} scoring factors")
    except Exception as e:
        print(f"❌ Root Endpoint Failed: {e}")
    
    # Test 3: Basic credit evaluation
    print("\n📊 Testing Credit Evaluation:")
    test_cases = [
        ("Low Asset Value", get_sample_data()),
        ("High Asset Value", get_high_value_sample())
    ]
    
    for name, test_data in test_cases:
        try:
            response = requests.post(
                f"{base_url}/evaluate_credit",
                headers={"Content-Type": "application/json"},
                json=test_data
            )
            
            if response.status_code == 200:
                result = response.json()
                asset_value = test_data["analysis_result"]["credit_features"]["total_asset_value"]
                print(f"✅ {name}: Asset ${asset_value:,.0f} → Score {result['credit_score']}/100")
            else:
                print(f"❌ {name}: HTTP {response.status_code} - {response.text[:100]}")
                
        except Exception as e:
            print(f"❌ {name} Failed: {e}")
    
    # Test 4: Detailed evaluation
    print("\n📋 Testing Detailed Evaluation:")
    try:
        response = requests.post(
            f"{base_url}/evaluate_credit_detailed",
            headers={"Content-Type": "application/json"},
            json=get_sample_data()
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Detailed Analysis: Score {result['credit_score']}/100")
            breakdown = result.get('score_breakdown', {})
            print(f"   Coverage Ratio: {breakdown.get('asset_coverage_ratio', 'N/A')}")
            print(f"   Asset Condition: {breakdown.get('asset_condition', 'N/A')}/10")
            print(f"   Verification: {breakdown.get('exif_verification_rate', 'N/A')}")
        else:
            print(f"❌ Detailed Analysis: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Detailed Analysis Failed: {e}")
    
    print("=" * 60)
    print("🎯 Testing complete!")

if __name__ == "__main__":
    import sys
    
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    test_api(base_url)
