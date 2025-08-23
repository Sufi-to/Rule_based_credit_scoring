import requests
import json

def test_complete_denial():
    url = "http://localhost:8000/evaluate_credit"
    
    # Load test data for complete denial case
    with open('test_complete_denial.json', 'r') as f:
        test_data = json.load(f)
    
    try:
        response = requests.post(url, json=test_data)
        
        print("=" * 60)
        print("API Test Results - Complete Denial Case")
        print("=" * 60)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("approved"):
                print("✅ Credit APPROVED!")
                print(f"   Approved Amount: ${result.get('approved_amount')}")
                print(f"   Coverage: {result.get('coverage_percentage')}%")
            else:
                print("❌ Credit DENIED")
                print(f"   Credit Score: {result.get('credit_score')}")
                print(f"   Reason: {result.get('reason')}")
                if result.get('fraud_flags'):
                    print(f"   Fraud Flags: {result.get('fraud_flags')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_complete_denial()
