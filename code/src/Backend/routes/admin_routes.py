from flask import Blueprint, jsonify,request
from models import User,Customer, Products
from utils.decorators import token_required, role_required
from .customer_insights import fetch_customer_features
import joblib
import pandas as pd
from .Insights import generate_customer_insights

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/insights', methods=['GET'])
@token_required
@role_required('admin')
def predict_risk(user_data):
    user_name = request.args.get("username")
    if not user_name:
        return jsonify({"error": "Username is required"}), 400
    customer = User.query.filter_by(username=user_name).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    customer_id = customer.id


    # Fetch customer features
    customer_features = fetch_customer_features(customer_id)

    model = joblib.load("best_risk_classification_model.joblib")

    if not customer_features:
        return jsonify({"error": "Customer not found"}), 404

    # Convert to DataFrame and predict
    input_df = pd.DataFrame([customer_features])
    risk_score = model.predict(input_df)[0]

    # Product recommendations
    risk_levels = {0: "Low", 1: "Medium", 2: "High"}
    recommended_products = Products.query.filter_by(risk_level=risk_levels[risk_score]).all()
    recommended_products = [product.product_name for product in recommended_products]

    # Generate insights
    insights = generate_customer_insights(customer_features,risk_levels[risk_score],recommended_products)

    return jsonify({
        "customer_id": customer_id,
        "recommended_products": recommended_products,
        "insights": insights
    })