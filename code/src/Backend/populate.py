import random
from faker import Faker
from collections import Counter
from datetime import datetime, timedelta

from app import app,db 
from models import User, Customer, FinancialBehavior, Transaction, RiskProfile, Products, Review

fake = Faker()

# CONFIGS
NUM_CUSTOMERS = 500
PASSWORD = '123456'  # default password for all users

def create_users_and_customers():
    users = []
    customers = []

    for _ in range(NUM_CUSTOMERS):
        username = fake.user_name()
        user = User(
            username=username,
            role='customer'
        )
        user.set_password(PASSWORD)
        db.session.add(user)
        db.session.flush()  # gets user.id before commit

        gender = random.choice(['Male', 'Female'])
        age = random.randint(21, 65)
        yearly_salary = random.randint(500000, 5000000)  # 5L - 50L realistic salary range
        education = random.choice(['Bachelor', 'Masters', 'PhD'])
        occupation = fake.job()

        customer = Customer(
            user_id=user.id,
            name=fake.name_male() if gender == 'Male' else fake.name_female(),
            gender=gender,
            age=age,
            education=education,
            occupation=occupation,
            yearly_salary=yearly_salary
        )
        db.session.add(customer)
        db.session.flush()

        users.append(user)
        customers.append(customer)

    db.session.commit()
    return users, customers


def create_financial_behaviors():
    products_in_db = {p.product_name: p for p in Products.query.all()}
    customers = Customer.query.all()
    for customer in customers:
        yearly_salary = customer.yearly_salary
        if not yearly_salary:
            continue
        age = customer.age or 30  
        
        # Probabilistic assignment based on salary and age
        eligible_products = []

        # Loans and Credit Card Eligibility
        if yearly_salary > 500000:
            eligible_products.append("Credit Card")
        if yearly_salary > 700000:
            eligible_products.append("Personal Loan")
        if yearly_salary > 1200000 and age >= 28:
            eligible_products.append("Home Loan")
        
        # Investment product eligibility (broad)
        eligible_products.extend([
            "Fixed Deposit",
            "Recurring Deposit",
            "Mutual Fund",
            "Equity Shares",
            "Government Bonds",
            "Gold ETF"
        ])
        
        # Assign 2-4 products randomly
        chosen_products = random.sample(eligible_products, random.randint(2, min(4, len(eligible_products))))
        
        for product_name in chosen_products:
            product_obj = products_in_db[product_name]
            
            # Initialize all fields to None
            loan_amount = None
            credit_limit = None
            credit_utilization = None
            investment_amount = None
            tenure_months = None
            returns_percentage = None
            emi_paid = None
            max_dpd = None
            default_status = False
            
            # Logic per product type
            if product_name == "Home Loan":
                loan_amount = random.randint(1000000, min(5000000, int(yearly_salary * 5)))
                tenure_months = random.choice([120, 180, 240, 300])  # 10-25 years
                emi_paid = random.randint(1, tenure_months)
                max_dpd = random.choice([0, 15, 30, 60])
                default_status = max_dpd >= 30
                
            elif product_name == "Personal Loan":
                loan_amount = random.randint(100000, min(2000000, int(yearly_salary * 2)))
                tenure_months = random.choice([12, 24, 36, 48, 60])
                emi_paid = random.randint(1, tenure_months)
                max_dpd = random.choice([0, 15, 30, 60, 90])
                default_status = max_dpd >= 30
                
            elif product_name == "Credit Card":
                credit_limit = random.randint(50000, min(300000, int(yearly_salary * 0.3)))
                credit_utilization = round(random.uniform(0.2, 0.9), 2)
                max_dpd = random.choice([0, 15, 30, 60])
                default_status = max_dpd >= 30
                
            elif product_name in ["Fixed Deposit", "Recurring Deposit", "Government Bonds"]:
                investment_amount = random.randint(50000, min(2000000, int(yearly_salary * 0.5)))
                tenure_months = random.choice([12, 24, 60, 120])  # 1-10 years
                returns_percentage = round(random.uniform(4.5, 7.5), 2)
                
            elif product_name == "Mutual Fund":
                investment_amount = random.randint(10000, min(1000000, int(yearly_salary * 0.2)))
                tenure_months = random.choice([12, 36, 60])
                returns_percentage = round(random.uniform(-5, 15), 2)  # Higher variance
                
            elif product_name == "Equity Shares":
                investment_amount = random.randint(10000, min(500000, int(yearly_salary * 0.1)))
                tenure_months = random.choice([6, 12, 36])
                returns_percentage = round(random.uniform(-20, 25), 2)  # High risk
                
            elif product_name == "Gold ETF":
                investment_amount = random.randint(20000, min(300000, int(yearly_salary * 0.1)))
                tenure_months = random.choice([12, 24, 60])
                returns_percentage = round(random.uniform(5, 12), 2)
            
            behavior = FinancialBehavior(
                customer_id=customer.user_id,
                product_id=product_obj.id,
                loan_amount=loan_amount,
                credit_limit=credit_limit,
                credit_utilization=credit_utilization,
                investment_amount=investment_amount,
                tenure_months=tenure_months,
                returns_percentage=returns_percentage,
                emi_paid=emi_paid,
                max_dpd=max_dpd,
                default_status=default_status
            )
            
            db.session.add(behavior)
    
    db.session.commit()


def create_transactions():
    customers = Customer.query.all()

    for customer in customers:
        num_transactions = random.randint(30, 100)
        transaction_date = datetime.now() - timedelta(days=365)  # last year
        account_balance = customer.yearly_salary * 3  # Starting balance, e.g., 3x salary

        for _ in range(num_transactions):
            days_to_add = random.randint(1, 10)
            transaction_date += timedelta(days=days_to_add)

            # Define salary transactions (monthly income)
            if transaction_date.day <= 5 and random.random() < 0.8:  # 80% chance to get salary in 1st week
                transaction_amount = customer.yearly_salary / 12
                description = "Monthly Salary"
                is_salary = True
                transaction_type = True  # Credit
                account_balance += transaction_amount
            else:
                # Random expense
                transaction_amount = round(random.uniform(500, 20000), 2)
                description = fake.word().capitalize() + " Expense"
                is_salary = False
                transaction_type = False  # Debit

                # Ensure balance doesn't go negative
                if account_balance >= transaction_amount:
                    account_balance -= transaction_amount
                else:
                    transaction_amount = account_balance
                    account_balance = 0

            txn = Transaction(
                customer_id=customer.user_id,
                transaction_date=transaction_date.date(),
                transaction_amount=transaction_amount,
                description=description,
                is_salary=is_salary,
                transaction_type=transaction_type,
                account_balance=account_balance
            )

            db.session.add(txn)

    db.session.commit()



def create_risk_profiles():
    customers = Customer.query.all()

    for customer in customers:
        behaviors = FinancialBehavior.query.filter_by(customer_id=customer.user_id).all()
        transactions = Transaction.query.filter_by(customer_id=customer.user_id).all()
        
        total_loans = sum(b.loan_amount or 0 for b in behaviors if b.loan_amount)
        total_credit_limit = sum(b.credit_limit or 0 for b in behaviors if b.credit_limit)
        total_credit_utilization = sum((b.credit_limit or 0) * (b.credit_utilization or 0) for b in behaviors if b.credit_utilization)
        
        # Debt-to-income ratio
        debt_to_income_ratio = total_loans / customer.yearly_salary if customer.yearly_salary else 0
        
        # Average credit utilization ratio
        avg_credit_utilization = (total_credit_utilization / total_credit_limit) if total_credit_limit else 0
        
        # Check for defaults
        defaults = any(b.default_status for b in behaviors)
        
        # Investment health (bad if multiple negative returns)
        risky_investments = sum(1 for b in behaviors if b.returns_percentage is not None and b.returns_percentage < 0)
        
        # High-value transaction flag
        high_txn_amount = any(t.transaction_amount > (customer.yearly_salary * 0.1) for t in transactions)
        
        # Base risk score starts high, reduced by risky behavior
        risk_score = 850
        
        # Penalize for debt-to-income ratio
        if debt_to_income_ratio > 0.5:
            risk_score -= 100
        
        if avg_credit_utilization > 0.5:
            risk_score -= 75
        
        if defaults:
            risk_score -= 150
        
        if risky_investments > 2:
            risk_score -= 50
        
        if high_txn_amount:
            risk_score -= 50
        
        # Add randomness for realism
        risk_score -= random.uniform(0, 50)
        
        # Clamp risk score between 300 and 850
        risk_score = max(300, min(850, risk_score))

        if risk_score <= 500:
            risk_score = 2  # High Risk
        elif risk_score <= 700:
            risk_score = 1  # Medium Risk
        else:
            risk_score = 0
        
        # Fraud flag can also be influenced by multiple red flags
        fraud_flag = False
        if high_txn_amount and defaults and avg_credit_utilization > 0.7:
            fraud_flag = True
        else:
            fraud_flag = random.random() < 0.03  # 3% random chance
        
        suspicious_transaction = high_txn_amount
        financial_distress = defaults or debt_to_income_ratio > 0.6
        
        risk_profile = RiskProfile(
            customer_id=customer.user_id,
            risk_score=risk_score,
            fraud_flag=fraud_flag,
            suspicious_transaction=suspicious_transaction,
            financial_distress=financial_distress
        )
        
        db.session.add(risk_profile)

    db.session.commit()

def populate_reviews():
    customers = db.session.query(Customer).all()
    products = db.session.query(Products).all()

    # Step 2: Populate reviews
    sample_reviews = [
        "Great product, really loved it!",
        "Not satisfied with the quality.",
        "Would definitely recommend!",
        "It didn't meet my expectations.",
        "Excellent value for money!",
        "Poor customer service experience.",
        "Five stars, totally worth it.",
        "Average product, okay for the price."
    ]

    reviews_to_add = []

    for customer in customers:
        # Let's add, say, 1 to 3 reviews per customer
        num_reviews = random.randint(1, 3)
        for _ in range(num_reviews):
            product = random.choice(products)

            review_text = random.choice(sample_reviews)
            review_date = datetime.utcnow().date()  # or random date
            is_positive = "not" not in review_text.lower() and "poor" not in review_text.lower() and "didn't" not in review_text.lower()

            review = Review(
                customer_id=customer.user_id,
                product_id=product.id,
                review_text=review_text,
                review_date=review_date,
                is_positive=is_positive
            )
            reviews_to_add.append(review)

    # Step 3: Bulk insert and commit
    db.session.bulk_save_objects(reviews_to_add)
    db.session.commit()





def populate_products():
    products = [
        {"product_name": "Home Loan", "risk_level": "Medium"},
        {"product_name": "Personal Loan", "risk_level": "High"},
        {"product_name": "Credit Card", "risk_level": "High"},
        {"product_name": "Fixed Deposit", "risk_level": "Low"},
        {"product_name": "Recurring Deposit", "risk_level": "Low"},
        {"product_name": "Mutual Fund", "risk_level": "Medium"},
        {"product_name": "Equity Shares", "risk_level": "High"},
        {"product_name": "Government Bonds", "risk_level": "Low"},
        {"product_name": "Gold ETF", "risk_level": "Medium"},
    ]

    for p in products:
        product = Products(product_name=p["product_name"], risk_level=p["risk_level"])
        db.session.add(product)

    db.session.commit()



def populate_database():

    # print("Create customers and users")
    # create_users_and_customers()

    # print("Creating Financial Behaviors...")
    # create_financial_behaviors()

    # print("Creating Transactions...")
    # create_transactions()

    print("Creating Risk Profiles...")
    create_risk_profiles()

    # print("Populating Products!!")
    # populate_products()

    print("Populating reviews")
    populate_reviews()

    print("Database populated successfully!")

# Run the script!
if __name__ == "__main__":
    with app.app_context():
        populate_database()
