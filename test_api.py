import requests
import json
import time

def test_api():
    # API endpoint
    url = "http://localhost:8000/evaluate_credit"
    
    # Load test data
    with open('test_credit_request.json', 'r') as f:
        test_data = json.load(f)
    
    try:
        # Make the API call
        response = requests.post(url, json=test_data)
        
        print("=" * 50)
        print("API Test Results")
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
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API server.")
        print("Make sure the FastAPI server is running on http://localhost:8000")
        print("Run: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
