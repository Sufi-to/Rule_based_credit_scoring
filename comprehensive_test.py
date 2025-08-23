import requests
import json

def run_comprehensive_tests():
    url = "http://localhost:8000/evaluate_credit"
    
    test_cases = [
        {
            "name": "High-Quality Applicant",
            "file": "test_credit_request.json",
            "description": "Good income, assets, and behavior"
        },
        {
            "name": "Marginal Applicant", 
            "file": "test_denial_case.json",
            "description": "Lower income and assets, some risk factors"
        },
        {
            "name": "High-Risk Applicant",
            "file": "test_complete_denial.json", 
            "description": "Poor financial behavior and multiple fraud flags"
        }
    ]
    
    print("🏥 MEDICATION CREDIT SCORING SYSTEM - COMPREHENSIVE TEST")
    print("=" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 TEST {i}: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print("-" * 50)
        
        try:
            with open(test_case['file'], 'r') as f:
                test_data = json.load(f)
            
            response = requests.post(url, json=test_data)
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"📊 Credit Score: {result.get('credit_score', 'N/A')}/100")
                
                if result.get("approved"):
                    print("✅ STATUS: APPROVED")
                    print(f"💰 Approved Amount: ${result.get('approved_amount'):,.2f}")
                    print(f"💊 Requested Amount: ${result.get('requested_amount'):,.2f}")
                    print(f"📈 Coverage: {result.get('coverage_percentage', 0):.1f}%")
                    print(f"🏠 Asset Coverage Ratio: {result.get('asset_coverage_ratio', 0):.2f}x")
                else:
                    print("❌ STATUS: DENIED")
                    print(f"🚫 Reason: {result.get('reason', 'N/A')}")
                
                # Show medication profile
                med_profile = result.get('medication_profile', {})
                print(f"💊 Medication Category: {med_profile.get('category', 'N/A').title()}-cost ({med_profile.get('description', 'N/A')})")
                
                # Show fraud flags if any
                fraud_flags = result.get('fraud_flags', [])
                if fraud_flags:
                    print(f"⚠️  Fraud Flags ({len(fraud_flags)}): {', '.join(fraud_flags)}")
                else:
                    print("✅ No fraud indicators detected")
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except FileNotFoundError:
            print(f"❌ Test file not found: {test_case['file']}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 80)
    print("🎯 SYSTEM SUMMARY:")
    print("• Scoring Range: 0-100 points")
    print("• Asset Weight: 40% | Income Weight: 25% | Behavior: 20% | Activity: 10% | Social: 5%")
    print("• Medication Categories: Low (<$2K), Medium ($2K-$5K), High (>$5K)")
    print("• Fraud Detection: Multiple behavioral and pattern indicators")
    print("• Risk-based Limits: Credit amount based on score and asset coverage")

if __name__ == "__main__":
    run_comprehensive_tests()
