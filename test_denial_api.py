import requests
import json

def test_denial_case():
    url = "http://localhost:8000/evaluate_credit"
    
    # Load test data for denial case
    with open('test_denial_case.json', 'r') as f:
        test_data = json.load(f)
    
    try:
        response = requests.post(url, json=test_data)
        
        print("=" * 50)
        print("API Test Results - Denial Case")
        print("=" * 50)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("approved"):
                print("✅ Credit APPROVED!")
                print(f"   Approved Amount: ${result.get('approved_amount')}")
            else:
                print("❌ Credit DENIED")
                print(f"   Reason: {result.get('reason')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_denial_case()
