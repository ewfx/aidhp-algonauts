from functools import wraps
from flask import request, jsonify
import jwt
from config import Config

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from headers
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify(msg='Token is missing'), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify(msg='Token has expired'), 401
        except jwt.InvalidTokenError:
            return jsonify(msg='Invalid token'), 401

        return f(data, *args, **kwargs)  # Pass decoded token data

    return decorated

def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped(data, *args, **kwargs):
            if data.get("role") != role:
                return jsonify(msg="Unauthorized role"), 403
            return f(data, *args, **kwargs)
        return wrapped
    return decorator

