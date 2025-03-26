import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib
import sys
import os
from datetime import datetime
from sqlalchemy import func
import fasttext
from sklearn.feature_extraction.text import TfidfVectorizer


# Adds the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from models import Customer, RiskProfile, FinancialBehavior, Transaction, Review, Products

def fetch_customer_data():
    customers = Customer.query.all()

    customer_data = []
    occupations = [customer.occupation for customer in customers]  # List of all occupations
    vectorizer = TfidfVectorizer(max_features=50)
    occupation_vectors = vectorizer.fit_transform(occupations).toarray()

    joblib.dump(vectorizer,"occupation_vectorizer")

    for customer in customers:
        # Risk Profile
        risk = customer.risk_profile

        # Transactions
        transactions = customer.transactions
        total_transaction_amount = sum([txn.transaction_amount for txn in transactions if txn.transaction_type])
        num_transactions = len(transactions)
        salary_txns = sum([1 for txn in transactions if txn.is_salary])
        avg_account_balance = (sum([txn.account_balance for txn in transactions]) / num_transactions) if num_transactions > 0 else 0

        # Financial Behaviors
        behaviors = customer.financial_behavior
        total_investment = sum([fb.investment_amount or 0 for fb in behaviors])
        total_loans = sum([fb.loan_amount or 0 for fb in behaviors])
        avg_credit_util = (sum([fb.credit_utilization or 0 for fb in behaviors]) / len(behaviors)) if behaviors else 0
        credit_limit = sum([fb.credit_limit or 0 for fb in behaviors])

        # Reviews
        reviews = customer.reviews
        num_reviews = len(reviews)
        positive_reviews = sum([1 for review in reviews if review.is_positive])
        review_ratio = (positive_reviews / num_reviews) if num_reviews > 0 else 0
        
        # Risk Profile details
        risk_score = risk.risk_score if risk else 0
        fraud_flag = 1 if (risk and risk.fraud_flag) else 0
        suspicious_transaction = 1 if (risk and risk.suspicious_transaction) else 0
        financial_distress = 1 if (risk and risk.financial_distress) else 0

        # Product risk level distribution
        product_risks = []
        for fb in behaviors:
            product = Products.query.get(fb.product_id)
            if product:
                product_risks.append(product.risk_level)

        risk_level_map = {'Low': 1, 'Medium': 2, 'High': 3}
        avg_product_risk = (
            sum([risk_level_map.get(risk, 0) for risk in product_risks]) / len(product_risks)
            if product_risks else 0
        )
        occupation_vector = vectorizer.transform([customer.occupation]).toarray().flatten()

        education_encoding = {'Bachelor':0, 'Masters':1, 'PhD':2}

        # Append feature set
        customer_data.append({
            'customer_id': customer.user_id,
            'age': customer.age,
            'gender': 1 if customer.gender == 'Male' else 0,
            'yearly_salary': customer.yearly_salary,
            'education_level': education_encoding[customer.education] if customer.education else 0,
            'occupation': customer.occupation if customer.occupation else 0,
            'occupation_vector':  occupation_vector.tolist() if customer.occupation else 0,

            # Transactions
            'total_transaction_amount': total_transaction_amount,
            'num_transactions': num_transactions,
            'salary_transactions': salary_txns,
            'avg_account_balance': avg_account_balance,
            # Financial Behavior
            'total_investment': total_investment,
            'total_loans': total_loans,
            'credit_limit': credit_limit,
            'avg_credit_util': avg_credit_util,

            # Reviews
            'num_reviews': num_reviews,
            'positive_review_ratio': review_ratio,

            # Risk Profile
            'risk_score': risk_score,
            'fraud_flag': fraud_flag,
            'suspicious_transaction': suspicious_transaction,
            'financial_distress': financial_distress,

            # Product Risk Levels
            'avg_product_risk': avg_product_risk
        })

    return pd.DataFrame(customer_data)

if __name__ == '__main__':
    with app.app_context():
        df = fetch_customer_data()

        # Preview the first few rows in the console (optional)
        print("Sample Data Preview:")
        print(df.head())

        # Handle missing values (optional but recommended before saving or clustering)
        # df.fillna(0, inplace=True)

        file_path = 'customer_feature.csv'

        # Save to CSV
        df.to_csv(file_path, index=False)

        print(f"Customer data saved successfully to {file_path}")

