from flask import Flask
from config import Config
from models import db, FinancialBehavior
from routes.auth_routes import auth_bp
from routes.customer_routes import customer_bp
from routes.admin_routes import admin_bp
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)s

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

db.init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(customer_bp, url_prefix='/customer')
app.register_blueprint(admin_bp, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)
