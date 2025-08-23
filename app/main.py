from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class BankData(BaseModel):
    opening_balance: float
    closing_balance: float
    average_balance: float
    statement_period_days: int
    turnover: float
    net_cash_flow: float
    total_deposits_amount: float
    count_deposits: int
    average_deposit_amount: float
    max_deposit_amount: float
    min_deposit_amount: float
    std_dev_deposits: float
    total_withdrawals_amount: float
    total_main_withdrawals_amount: float
    total_charges_amount: float
    count_main_withdrawals: int
    count_debit_transactions: int
    average_main_withdrawal_amount: float
    max_main_withdrawal_amount: float
    min_main_withdrawal_amount: float
    std_dev_main_withdrawals: float
    closing_to_opening_ratio: float
    average_to_closing_balance_ratio: float
    total_withdrawals_to_opening_balance_ratio: float
    balance_volatility_std_dev: float
    active_days_in_period: int
    days_since_last_transaction: int
    percentage_active_days: float
    average_transactions_per_active_day: float
    has_salary_inflow: int
    is_likely_student: int
    count_mobile_money_transfers_out: int
    total_mobile_money_transfers_out_amount: float
    has_single_dominant_beneficiary: int
    percentage_withdrawals_to_dominant_beneficiary: float
    has_loan_repayment: int
    has_betting_transactions: int
    has_bounced_cheques: int
    avg_days_between_large_deposits: float
    avg_days_between_large_withdrawals: float

class CallLogAnalysis(BaseModel):
    call_frequency: int
    call_duration: float
    active_behavior: float
    stable_contacts_ratio: float
    night_vs_day: float
    missed_only: float
    regular_patterns_std: float
    geographic_pattern: int

class CallLogs(BaseModel):
    analysis: CallLogAnalysis

class MpesaFeatures(BaseModel):
    total_transactions: int
    num_paybill: int
    num_merchant: int
    num_customer_transfers: int
    num_airtime_purchases: int
    total_inflow: float
    total_outflow: float
    avg_transaction_size: float
    max_transaction_size: float
    min_transaction_size: float
    merchant_spend_total: float
    paybill_spend_total: float
    airtime_spend_total: float
    avg_balance: float
    min_balance: float
    max_balance: float
    balance_volatility: float
    end_balance: float
    inflow_outflow_ratio: float
    merchant_ratio: float
    airtime_ratio: float
    paybill_ratio: float
    unique_recipients: int
    recurring_payments: int
    avg_time_between_large_balances_sec: float
    avg_time_between_inflows_sec: float

class MpesaData(BaseModel):
    features: MpesaFeatures

class AssetData(BaseModel):
    user_id: int
    asset_value: float = Field(..., alias="asset value")

class MedicationData(BaseModel):
    user_id: int
    medication: float

class CreditRequest(BaseModel):
    bank_data: BankData
    call_logs: CallLogs
    mpesa_data: MpesaData
    asset_data: AssetData
    medication_data: MedicationData

def calculate_credit_score(bank_data, call_logs, mpesa_data, asset_data, medication_data):
    """Calculate credit score based on weighted factors (0-100 scale)"""
    score = 0
    
    # Asset scoring (40% weight - most important for collateral)
    if asset_data.asset_value > 0:
        asset_ratio = asset_data.asset_value / medication_data.medication
        if asset_ratio >= 2.0: 
            score += 40  # Asset worth 2x+ medication cost
        elif asset_ratio >= 1.5: 
            score += 32  # Asset worth 1.5x+ medication cost
        elif asset_ratio >= 1.0: 
            score += 25  # Asset covers medication cost
        elif asset_ratio >= 0.5: 
            score += 15  # Asset covers 50%+ of cost
        else: 
            score += 5   # Some asset value
    
    # Income scoring (25% weight)
    if bank_data.has_salary_inflow:
        score += 25  # Regular salary is best
    elif mpesa_data.features.total_inflow > medication_data.medication * 3:
        score += 22  # High mobile money inflow
    elif mpesa_data.features.total_inflow > medication_data.medication:
        score += 18  # Moderate inflow
    elif mpesa_data.features.total_inflow > 0:
        score += 12  # Some inflow
    
    # Financial behavior scoring (20% weight)
    behavior_score = 20
    if bank_data.has_bounced_cheques:
        behavior_score -= 15  # Major penalty
    if bank_data.has_betting_transactions:
        behavior_score -= 10  # Moderate penalty
    if bank_data.has_loan_repayment:
        behavior_score += 5   # Bonus for loan history
    score += max(0, behavior_score)
    
    # Account activity scoring (10% weight)
    activity_score = min(bank_data.percentage_active_days * 10, 10)
    if bank_data.days_since_last_transaction <= 7:
        activity_score += 2  # Recent activity bonus
    score += min(10, activity_score)
    
    # Social stability scoring (5% weight)
    social_score = min(call_logs.analysis.stable_contacts_ratio * 5, 5)
    if call_logs.analysis.call_frequency > 15:
        social_score += 1  # Active communication bonus
    score += min(5, social_score)
    
    return min(100, score)

def detect_fraud_indicators(bank_data, call_logs, mpesa_data):
    """Detect potential fraud indicators"""
    fraud_flags = []
    
    # Suspicious call patterns
    if call_logs.analysis.night_vs_day > 0.7:
        fraud_flags.append("High night call ratio")
    
    # Geographic spread too wide
    if call_logs.analysis.geographic_pattern > 300:
        fraud_flags.append("Unusually wide geographic pattern")
    
    # No bank deposits but high mobile money
    if (bank_data.count_deposits == 0 and 
        mpesa_data.features.total_inflow > mpesa_data.features.avg_balance * 5):
        fraud_flags.append("Suspicious income source pattern")
    
    # Too many failed calls
    if call_logs.analysis.missed_only > 0.8:
        fraud_flags.append("High missed call ratio")
    
    # Unusual transaction patterns
    if mpesa_data.features.inflow_outflow_ratio > 5.0:
        fraud_flags.append("Abnormally high inflow to outflow ratio")
    
    # Very high balance volatility
    if (mpesa_data.features.balance_volatility > mpesa_data.features.avg_balance * 2 and
        mpesa_data.features.avg_balance > 0):
        fraud_flags.append("Extremely high balance volatility")
    
    return fraud_flags

def determine_credit_limit(score, medication_cost, asset_value, fraud_flags):
    """Determine credit limit based on score and risk factors"""
    
    # Automatic denial conditions
    if len(fraud_flags) >= 2:
        return 0, "Multiple fraud indicators detected"
    
    if score < 30:
        return 0, "Credit score too low"
    
    if asset_value < medication_cost * 0.3:
        return 0, "Insufficient asset coverage"
    
    # Calculate base credit limit
    if score >= 80:
        max_ratio = 0.9  # Can borrow up to 90% of asset value
        med_ratio = 1.0  # Can get full medication cost
    elif score >= 65:
        max_ratio = 0.7
        med_ratio = 0.9
    elif score >= 50:
        max_ratio = 0.5
        med_ratio = 0.7
    elif score >= 40:
        max_ratio = 0.4
        med_ratio = 0.5
    else:  # 30-39
        max_ratio = 0.3
        med_ratio = 0.3
    
    # Apply fraud penalty
    if len(fraud_flags) == 1:
        max_ratio *= 0.8
        med_ratio *= 0.8
    
    # Calculate final limit
    asset_limit = asset_value * max_ratio
    medication_limit = medication_cost * med_ratio
    
    approved_amount = min(asset_limit, medication_limit, medication_cost)
    
    if approved_amount < medication_cost * 0.2:  # Less than 20% of needed amount
        return 0, "Approved amount too low to be useful"
    
    return approved_amount, "Credit approved"

def get_medication_risk_profile(medication_cost):
    """Get risk profile based on medication cost"""
    if medication_cost > 5000:
        return {"category": "high", "min_score": 70, "description": "High-cost medication"}
    elif medication_cost > 2000:
        return {"category": "medium", "min_score": 50, "description": "Medium-cost medication"}
    else:
        return {"category": "low", "min_score": 40, "description": "Low-cost medication"}

def evaluate_credit(bank_data, call_logs, mpesa_data, asset_data, medication_data):
    """Enhanced credit evaluation with scoring system"""
    
    # Calculate credit score
    credit_score = calculate_credit_score(bank_data, call_logs, mpesa_data, asset_data, medication_data)
    
    # Detect fraud indicators
    fraud_flags = detect_fraud_indicators(bank_data, call_logs, mpesa_data)
    
    # Get medication risk profile
    med_profile = get_medication_risk_profile(medication_data.medication)
    
    # Check minimum score for medication category
    if credit_score < med_profile["min_score"]:
        return {
            "approved": False,
            "credit_score": credit_score,
            "reason": f"Credit score {credit_score} below minimum {med_profile['min_score']} for {med_profile['description']}",
            "fraud_flags": fraud_flags,
            "medication_profile": med_profile
        }
    
    # Determine credit limit
    approved_amount, approval_reason = determine_credit_limit(
        credit_score, 
        medication_data.medication, 
        asset_data.asset_value, 
        fraud_flags
    )
    
    if approved_amount > 0:
        return {
            "approved": True,
            "approved_amount": round(approved_amount, 2),
            "requested_amount": medication_data.medication,
            "credit_score": credit_score,
            "coverage_percentage": round((approved_amount / medication_data.medication) * 100, 1),
            "reason": approval_reason,
            "fraud_flags": fraud_flags,
            "medication_profile": med_profile,
            "asset_coverage_ratio": round(asset_data.asset_value / medication_data.medication, 2)
        }
    else:
        return {
            "approved": False,
            "credit_score": credit_score,
            "reason": approval_reason,
            "fraud_flags": fraud_flags,
            "medication_profile": med_profile
        }

@app.post("/evaluate_credit")
def evaluate_credit_endpoint(request: CreditRequest):
    result = evaluate_credit(
        request.bank_data,
        request.call_logs,
        request.mpesa_data,
        request.asset_data,
        request.medication_data
    )
    return result