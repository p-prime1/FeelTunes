import os
from dotenv import load_dotenv
from flask import Flask, render_template, session
from models import User
from extensions import login_manager
from flask_login import current_user
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_pymongo import PyMongo
from bson import ObjectId

mongo = PyMongo()


def create_app():
    # Load environment variables from .env
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")  # Fetch from .env

    # Initialize CSRF protection
    CSRFProtect(app)
    
    # flask force to clear cache each time
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    
    # Configure MongoDB
    app.config['MONGO_URI'] = os.getenv("MONGO_URI")
    mongo.init_app(app)
    
    # Cookies duration
    app.config['REMEMBER_COOKIE_DURATION'] = 60 * 60 * 24 * 7  # 1 week
    
    # Session implementaion
    app.config["SESSION_PERMANENT"] = True
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    
    # Email configuration
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
    app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == "True"
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")
    app.config['MAIL_DEBUG'] = os.getenv("MAIL_DEBUG") == "True"
    mail = Mail()

    mail.init_app(app)
    
    
    # Initialize extensions
    login_manager.init_app(app)
    # Set the login view route (for redirecting unauthenticated users)
    login_manager.login_view = 'login.login' 
    
    # Register blueprints
    from cookies import cookies_bp
    from login import login_bp
    from register import register_bp
    from dashboard import dashboard_bp
    from about import about_bp
    from privacy import privacy_bp
    from recommendation import recommendation_bp
    from terms import terms_bp
    from profile import profile_bp
    from logout import logout_bp
    from forgot_password import forgot_password_bp
    
    app.register_blueprint(cookies_bp)
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(register_bp, url_prefix='/register')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(about_bp, url_prefix='/about')
    app.register_blueprint(recommendation_bp, url_prefix='/recommendation')
    app.register_blueprint(privacy_bp, url_prefix='/privacy')
    app.register_blueprint(terms_bp, url_prefix='/terms')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(logout_bp)
    app.register_blueprint(forgot_password_bp, url_prefix='/forgot_password')

    @app.route('/')
    def home():
        return render_template('index.html')
    
    # use current_user in templates
    @app.context_processor
    def inject_user():
        return {'current_user': current_user}
        
    
    return app


# User loader function
@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(user_data) if user_data else None 
