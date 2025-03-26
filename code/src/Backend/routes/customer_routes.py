from flask import Blueprint, request, jsonify
from models import db, Customer,Review,Transaction,Products,FinancialBehavior
import joblib
from datetime import datetime
from utils.decorators import token_required, role_required

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/profile', methods=['GET', 'PUT'])
@token_required
@role_required('customer')
def profile(user_data):
    user_id = user_data["user_id"]
    profile = Customer.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify(msg="Profile not found"), 404

    if request.method == 'GET':
        return jsonify(
            name=profile.name,
            age=profile.age,
            gender=profile.gender,
            education=profile.education,
            occupation=profile.occupation,
            yearly_salary=profile.yearly_salary
        )
    
    if request.method == 'PUT':
        data = request.json
        profile.name = data.get('name', profile.name)
        profile.age = data.get('age', profile.age)
        profile.gender = data.get('gender', profile.gender)
        profile.education = data.get('education', profile.education)
        profile.occupation = data.get('occupation', profile.occupation)
        profile.yearly_salary = data.get('yearly_salary', profile.yearly_salary)
        
        db.session.commit()
        return jsonify(msg='Profile updated successfully')


@customer_bp.route('/transactions', methods=['GET'])
@token_required
@role_required('customer')
def transactions(user_data):
    user_id = user_data['user_id']
    profile = Customer.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify({"error": "Customer not found"}), 404

    # Get query param to decide if we fetch all transactions
    all_transactions = request.args.get('all', 'false').lower() == 'true'

    query = Transaction.query.filter_by(customer_id=profile.user_id).order_by(Transaction.transaction_date.desc())

    # If "all=true" is passed, return all transactions, else limit to 5
    if not all_transactions:
        query = query.limit(5)

    transactions = query.all()

    return jsonify([
        {
            'id': txn.id,
            'transaction_date': txn.transaction_date.strftime('%Y-%m-%d'),
            'amount': txn.transaction_amount,
            'description': txn.description,
            'transaction_type': txn.transaction_type is True
        }
        for txn in transactions
    ])
@customer_bp.route('/reviews', methods=['GET'])
@token_required
@role_required('customer')
def reviews(user_data):
    user_id = user_data['user_id']
    if request.method == 'GET':
        profile = Customer.query.filter_by(user_id=user_id)
        if not profile:
            return ({'message':"User not found"}),404
        reviews = Review.query.filter_by(customer_id=user_id).all()
        
        return jsonify([{
            "product_id":r.product_id,
            "review_text":r.review_text,
            "review_date":r.review_date,
            "is_positive":r.is_positive
        } for r in reviews])
@customer_bp.route('/addreviews', methods=['POST'])
@token_required
@role_required('customer')
def reviewPost(user_data):
        if not profile:
            return ({'message':"User not found"}),404
        data = request.json
        vectorizer = joblib.load("review_vectorizer.joblib")
        model = joblib.load("review_classifier.joblib")
        cleaned_text = data['review'].lower()  # Basic preprocessing (same as training)
        transformed_text = vectorizer.transform([cleaned_text])  # Convert text to TF-IDF features
        prediction = model.predict(transformed_text)[0] 

        txn = Review(
            customer_id=user_data['user_id'],
            product_id=data["product_id"],
            review_date=datetime.now(),
            review_text=data['review'],
            is_positive=prediction
        )
        db.session.add(txn)
        db.session.commit()
        return jsonify(msg='Transaction added successfully')

@customer_bp.route("/finance",methods = ['GET'])
@token_required
@role_required('customer')
def get_financial_details(user_data):
    try:
        # Get the authenticated user's ID
        user_id = user_data['user_id']

        # Fetch financial behavior details for the user
        financial_details = db.session.query(
            FinancialBehavior, Products.product_name
        ).join(Products, FinancialBehavior.product_id == Products.id) \
         .filter(FinancialBehavior.customer_id == user_id).all()

        if not financial_details:
            return jsonify({"message": "No financial details found"}), 404

        # Structure the response
        financial_data = [
            {
                "product_name": product_name,
                "investment_amount": entry.investment_amount,
                "loan_amount": entry.loan_amount,
                "credit_limit": entry.credit_limit,
                "credit_utilization": entry.credit_utilization,
                "tenure_months": entry.tenure_months,
                "returns_percentage": entry.returns_percentage,
                "emi_paid": entry.emi_paid,
                "max_dpd": entry.max_dpd,
                "default_status": entry.default_status,
            }
            for entry, product_name in financial_details
        ]

        return jsonify(financial_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500