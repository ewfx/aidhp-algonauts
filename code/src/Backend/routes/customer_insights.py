from models import Customer,Products,FinancialBehavior,Transaction,RiskProfile,Review
def fetch_customer_features(customer_id):
    customer = Customer.query.filter_by(user_id=customer_id).first()
    
    if not customer:
        return None

    transactions = customer.transactions
    behaviors = customer.financial_behavior
    reviews = customer.reviews
    risk = customer.risk_profile

    total_transaction_amount = sum([txn.transaction_amount for txn in transactions])
    num_transactions = len(transactions)
    salary_txns = sum([1 for txn in transactions if txn.is_salary])
    avg_account_balance = (sum([txn.account_balance for txn in transactions]) / num_transactions) if num_transactions > 0 else 0

    total_investment = sum([fb.investment_amount or 0 for fb in behaviors])
    total_loans = sum([fb.loan_amount or 0 for fb in behaviors])
    avg_credit_util = (sum([fb.credit_utilization or 0 for fb in behaviors]) / len(behaviors)) if behaviors else 0
    credit_limit = sum([fb.credit_limit or 0 for fb in behaviors])

    num_reviews = len(reviews)
    positive_reviews = sum([1 for review in reviews if review.is_positive])
    review_ratio = (positive_reviews / num_reviews) if num_reviews > 0 else 0

    fraud_flag = 1 if (risk and risk.fraud_flag) else 0
    suspicious_transaction = 1 if (risk and risk.suspicious_transaction) else 0
    financial_distress = 1 if (risk and risk.financial_distress) else 0

    risk_level_map = {'Low': 1, 'Medium': 2, 'High': 3}
    product_risks = [
        risk_level_map.get(Products.query.get(fb.product_id).risk_level, 0)
        for fb in behaviors if Products.query.get(fb.product_id)
    ]
    avg_product_risk = (sum(product_risks) / len(product_risks)) if product_risks else 0

    education_encoding = {'Bachelor': 0, 'Masters': 1, 'PhD': 2}

    return {
        'age': customer.age,
        'gender': 1 if customer.gender == 'Male' else 0,
        'yearly_salary': customer.yearly_salary,
        'education_level': education_encoding.get(customer.education, 0),

        'total_transaction_amount': total_transaction_amount,
        'num_transactions': num_transactions,
        'salary_transactions': salary_txns,
        'avg_account_balance': avg_account_balance,

        'total_investment': total_investment,
        'total_loans': total_loans,
        'credit_limit': credit_limit,
        'avg_credit_util': avg_credit_util,

        'num_reviews': num_reviews,
        'positive_review_ratio': review_ratio,

        'fraud_flag': fraud_flag,
        'suspicious_transaction': suspicious_transaction,
        'financial_distress': financial_distress,

        'avg_product_risk': avg_product_risk
    }

