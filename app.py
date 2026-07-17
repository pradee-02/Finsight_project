import os
from flask import Flask, redirect, url_for, request
from flask_login import LoginManager, UserMixin
from dotenv import load_dotenv

# Load env variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "finsight_ultra_secure_secret_key_2026_july")

# Configure session cookies for cross-origin iframe context (SameSite=None, Secure=True)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_HTTPONLY=True
)

# Ensure static/uploads exists
os.makedirs("static/uploads", exist_ok=True)

# Login manager configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.login_message = "Please authenticate to access your dashboard."
login_manager.login_message_category = "info"

# Simple User Session Wrapper for Flask-Login
class User(UserMixin):
    def __init__(self, user_dict):
        self.id = user_dict["email"]
        self.email = user_dict["email"]
        self.full_name = user_dict.get("full_name", "")
        self.monthly_income = user_dict.get("monthly_income", 0)
        self.profile_picture = user_dict.get("profile_picture", "")
        self.security_question = user_dict.get("security_question", "")

@login_manager.user_loader
def load_user(email):
    from database import db_engine
    user_data = db_engine.get_user_by_email(email)
    if user_data:
        return User(user_data)
    return None

# Register blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(dashboard_bp, url_prefix="")

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("dashboard.index"))

if __name__ == "__main__":
    # In production, bind to 0.0.0.0:3000 as required
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
