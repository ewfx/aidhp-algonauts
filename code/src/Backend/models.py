from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'customer' or 'admin'
    
    def set_password(self, password):
        # bcrypt requires the password to be in bytes
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=12)
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        
        # Store the hash as a decoded string for storage
        self.password_hash = hashed_password.decode('utf-8')
    
    def check_password(self, password):
        password_bytes = password.encode('utf-8')
        hashed_password_bytes = self.password_hash.encode('utf-8')
        
        return bcrypt.checkpw(password_bytes, hashed_password_bytes)

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    education = db.Column(db.String(50))
    occupation = db.Column(db.String(100))
    yearly_salary = db.Column(db.Float)

    financial_behavior = db.relationship('FinancialBehavior', backref='customer', lazy=True)
    transactions = db.relationship('Transaction', backref='customer', lazy=True)
    risk_profile = db.relationship('RiskProfile', backref='customer', uselist=False)
    reviews = db.relationship('Review', backref='customer', lazy=True)

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.user_id'), nullable=False)
    transaction_date = db.Column(db.Date)
    transaction_amount = db.Column(db.Float)
    description = db.Column(db.String(255))
    is_salary = db.Column(db.Boolean, default=False)
    transaction_type = db.Column(db.Boolean, default=True)
    account_balance = db.Column(db.Float)

class RiskProfile(db.Model):
    __tablename__ = 'risk_profiles'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.user_id'), nullable=False)
    risk_score = db.Column(db.Float)
    fraud_flag = db.Column(db.Boolean, default=False)
    suspicious_transaction = db.Column(db.Boolean, default=False)
    financial_distress = db.Column(db.Boolean, default=False)

class FinancialBehavior(db.Model):
    __tablename__ = 'financial_behavior'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Common financial metrics
    investment_amount = db.Column(db.Float, nullable=True)    # For investments like FDs, Mutual Funds
    loan_amount = db.Column(db.Float, nullable=True)          # For loans
    credit_limit = db.Column(db.Float, nullable=True)         # For credit cards
    credit_utilization = db.Column(db.Float, nullable=True)   # For credit cards

    tenure_months = db.Column(db.Integer, nullable=True)
    returns_percentage = db.Column(db.Float, nullable=True)   # For investments (FD, MF, Bonds)
    emi_paid = db.Column(db.Integer, nullable=True)
    max_dpd = db.Column(db.Integer, nullable=True)
    default_status = db.Column(db.Boolean, default=False)


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    review_text = db.Column(db.Text)
    review_date = db.Column(db.Date)
    is_positive = db.Column(db.Boolean)

class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50))
    risk_level = db.Column(db.String(20))  # Low, Medium, High
    
