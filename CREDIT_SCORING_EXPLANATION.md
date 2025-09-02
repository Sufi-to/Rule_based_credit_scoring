# Rule-Based Credit Scoring System - Detailed Developer Guide

## 🏗️ System Architecture Overview

This is a **FastAPI-based REST API** that takes in multiple data sources about a loan applicant and returns a credit decision. The system is specifically designed for healthcare financing - helping people get loans for essential medications.

### Technology Stack:
- **FastAPI**: Modern Python web framework for building APIs
- **Pydantic**: Data validation and serialization using Python type hints
- **Uvicorn**: ASGI server for running the FastAPI application

## 📊 Data Sources & Input Models

The system analyzes **5 different data sources** to make credit decisions:

### 1. Bank Data (BankData class)
This contains comprehensive banking history with **39 different metrics**:

**Core Balance Metrics:**
- `opening_balance`, `closing_balance`, `average_balance`
- `net_cash_flow`, `turnover`

**Transaction Analysis:**
- **Deposits**: count, amounts, averages, standard deviations
- **Withdrawals**: detailed breakdown including main withdrawals vs. charges
- **Activity Patterns**: active days, transaction frequency

**Risk Indicators:**
- `has_bounced_cheques`: Major red flag for credit risk
- `has_betting_transactions`: Indicates risky financial behavior
- `has_salary_inflow`: Positive indicator for stable income
- `has_loan_repayment`: Shows credit history experience

### 2. Call Log Analysis (CallLogAnalysis class)
Analyzes phone usage patterns to assess social stability:
- `call_frequency`: How often the person makes calls
- `stable_contacts_ratio`: Percentage of regular contacts (stability indicator)
- `night_vs_day`: Ratio of night to day calls (fraud detection)
- `missed_only`: Ratio of missed calls (communication behavior)
- `geographic_pattern`: Geographic spread of calls

### 3. M-Pesa Data (MpesaFeatures class)
Mobile money transaction history (common in East African markets):
- **Transaction Types**: Paybill, merchant, customer transfers, airtime
- **Financial Flow**: Total inflow/outflow, balance patterns
- **Spending Patterns**: Merchant spending, recurring payments
- **Behavioral Metrics**: Transaction frequency, unique recipients

### 4. Asset Data (AssetData class)
Information about collateral:
- `asset_value`: Value of assets that can secure the loan

### 5. Medication Data (MedicationData class)
The loan request details:
- `medication`: Cost of medication needed (loan amount requested)

## 🧮 Credit Scoring Algorithm

The heart of the system is the `calculate_credit_score()` function, which uses a **weighted scoring system (0-100 scale)**:

### Scoring Breakdown:

#### 1. Asset Scoring (40% weight - Highest Priority)
This is the most important factor because assets serve as collateral:
```
asset_ratio = asset_value / medication_cost
```
- **Score 40**: Asset worth 2x+ medication cost (200%+ coverage)
- **Score 32**: Asset worth 1.5x+ medication cost (150%+ coverage)  
- **Score 25**: Asset covers medication cost (100% coverage)
- **Score 15**: Asset covers 50%+ of cost
- **Score 5**: Some asset value

#### 2. Income Scoring (25% weight)
Assesses ability to repay:
- **Score 25**: Has regular salary inflow (most reliable)
- **Score 22**: High mobile money inflow (3x+ medication cost)
- **Score 18**: Moderate inflow (1x+ medication cost)
- **Score 12**: Some inflow detected

#### 3. Financial Behavior Scoring (20% weight)
Evaluates financial responsibility:
- **-15 points**: Has bounced cheques (major penalty)
- **-10 points**: Has betting transactions (risky behavior)
- **+5 points**: Has loan repayment history (positive experience)

#### 4. Account Activity Scoring (10% weight)
Measures engagement with financial services:
- Based on `percentage_active_days` 
- **+2 bonus**: Recent activity (last 7 days)

#### 5. Social Stability Scoring (5% weight)
Uses call log data to assess stability:
- Based on `stable_contacts_ratio`
- **+1 bonus**: Active communication (15+ calls)

## 🚨 Fraud Detection System

The `detect_fraud_indicators()` function identifies suspicious patterns:

### Fraud Flags:
1. **High night call ratio** (>70%): Unusual communication patterns
2. **Wide geographic pattern** (>300km): Potential location spoofing
3. **Suspicious income sources**: High mobile money but no bank deposits
4. **High missed call ratio** (>80%): Poor communication behavior
5. **Abnormal transaction ratios**: Extremely high inflow vs outflow
6. **Extreme balance volatility**: Unstable financial behavior

## 💰 Credit Limit Determination

The `determine_credit_limit()` function calculates how much to lend:

### Automatic Denial Conditions:
- **2+ fraud flags**: Multiple suspicious indicators
- **Credit score < 30**: Too risky
- **Asset value < 30% of medication cost**: Insufficient collateral

### Credit Limit Calculation:
Based on credit score ranges:
- **Score 80+**: Up to 90% of asset value, 100% of medication cost
- **Score 65-79**: Up to 70% of asset value, 90% of medication cost
- **Score 50-64**: Up to 50% of asset value, 70% of medication cost
- **Score 40-49**: Up to 40% of asset value, 50% of medication cost
- **Score 30-39**: Up to 30% of asset value, 30% of medication cost

**Final approved amount** = `min(asset_limit, medication_limit, medication_cost)`

## 🏥 Medication Risk Categories

The system categorizes loans by medication cost:

- **High-cost** (>$5,000): Requires minimum score of 70
- **Medium-cost** ($2,001-$5,000): Requires minimum score of 50  
- **Low-cost** (≤$2,000): Requires minimum score of 40

## 🔄 API Workflow

### Endpoint: POST /evaluate_credit

1. **Input Validation**: Pydantic validates all input data
2. **Credit Score Calculation**: Weighted algorithm produces 0-100 score
3. **Fraud Detection**: Scans for suspicious patterns
4. **Risk Assessment**: Determines medication risk category
5. **Credit Decision**: Approves/denies with specific reasoning
6. **Limit Calculation**: If approved, calculates maximum loan amount

### Sample API Response (Approval):
```json
{
  "approved": true,
  "approved_amount": 1350.0,
  "requested_amount": 1500.0,
  "credit_score": 85,
  "coverage_percentage": 90.0,
  "reason": "Credit approved",
  "fraud_flags": [],
  "medication_profile": {
    "category": "low",
    "min_score": 40,
    "description": "Low-cost medication"
  },
  "asset_coverage_ratio": 1.33
}
```

### Sample API Response (Denial):
```json
{
  "approved": false,
  "credit_score": 25,
  "reason": "Credit score 25 below minimum 40 for Low-cost medication",
  "fraud_flags": ["High missed call ratio"],
  "medication_profile": {
    "category": "low", 
    "min_score": 40,
    "description": "Low-cost medication"
  }
}
```

## 🧪 Testing Infrastructure

The codebase includes comprehensive testing:

- **`test_credit_request.json`**: Good applicant (should approve)
- **`test_denial_case.json`**: Poor applicant (should deny)
- **`test_api.py`**: Python script to test the API endpoint
- **Multiple test scenarios**: Different denial reasons and approval cases

## 🎯 Key Business Rules

1. **Asset-backed lending**: Assets must cover at least 30% of medication cost
2. **Income verification**: Multiple income sources considered (salary > mobile money)
3. **Behavioral analysis**: Financial responsibility heavily weighted
4. **Fraud prevention**: Multiple suspicious indicators trigger denial
5. **Graduated limits**: Higher scores unlock higher lending ratios
6. **Medical focus**: Specialized for healthcare financing needs

## 🔍 How to Use This System

1. **Start the API server**: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
2. **Send POST request** to `/evaluate_credit` with applicant data
3. **Receive credit decision** with detailed reasoning
4. **Use approved amount** for medication purchase

## 📋 Code Structure Deep Dive

### Main Components:

#### Pydantic Models (Data Validation)
- **BankData**: 39 banking metrics with strict type validation
- **CallLogAnalysis**: 8 communication behavior metrics
- **MpesaFeatures**: 26 mobile money transaction metrics
- **AssetData**: Collateral information
- **MedicationData**: Loan request details
- **CreditRequest**: Container for all input data

#### Core Functions:

**`calculate_credit_score()`**
- Takes all data sources as input
- Returns weighted score (0-100)
- Implements business logic for each scoring category
- Handles edge cases and missing data

**`detect_fraud_indicators()`**
- Analyzes patterns across all data sources
- Returns list of fraud flags
- Uses thresholds to identify suspicious behavior
- Critical for risk management

**`determine_credit_limit()`**
- Takes score, medication cost, asset value, and fraud flags
- Returns approved amount and reason
- Implements automatic denial rules
- Calculates final lending limits

**`get_medication_risk_profile()`**
- Categorizes loans by medication cost
- Sets minimum score requirements
- Adjusts risk tolerance based on loan size

**`evaluate_credit()`**
- Main orchestration function
- Calls all other functions in sequence
- Returns comprehensive credit decision
- Used by the API endpoint

#### API Endpoint:
**`@app.post("/evaluate_credit")`**
- Single REST endpoint for credit evaluation
- Accepts CreditRequest model
- Returns detailed credit decision
- Handles all validation and error cases

## 🛠️ Development Guidelines

### Adding New Features:
1. Update relevant Pydantic models for new data fields
2. Modify scoring functions to incorporate new data
3. Update test cases with new data structures
4. Ensure backward compatibility

### Modifying Scoring Logic:
1. Update weights in `calculate_credit_score()`
2. Test with existing test cases
3. Validate business logic with stakeholders
4. Document changes in code comments

### Adding New Fraud Detection:
1. Add new checks to `detect_fraud_indicators()`
2. Define clear thresholds and rationale
3. Test with both legitimate and suspicious cases
4. Monitor false positive rates

This system balances **accessibility** (helping people get needed medication) with **risk management** (protecting lenders from defaults) through comprehensive data analysis and rule-based decision making.
