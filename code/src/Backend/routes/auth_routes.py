from flask import Blueprint, request, jsonify
import jwt
import datetime
from models import db, User, Customer
from werkzeug.security import generate_password_hash
from config import Config  # Ensure Config.SECRET_KEY exists

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    password = data['password']
    role = data['role']  # customer or admin

    if User.query.filter_by(username=username).first():
        return jsonify(msg='Username already exists'), 409

    user = User(username=username, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # For customers, create an empty profile
    if role == 'customer':
        customer_profile = Customer(user_id=user.id)
        db.session.add(customer_profile)
        db.session.commit()

    return jsonify(msg='Account created successfully'), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    role = data['role']

    user = User.query.filter_by(role=role, username=username).first()
    if not user or not user.check_password(password):
        return jsonify(msg='Invalid username or password'), 401

    # Generate JWT token manually
    payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

    return jsonify(access_token=token), 200
