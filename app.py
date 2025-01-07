import os
from flask import request, redirect, url_for
from dotenv import load_dotenv
from flask import Flask, render_template, session
from models import User
from extensions import login_manager
from flask_login import current_user
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Initialize PyMongo without creating an app context
mongo = PyMongo()

def create_app():
    # Load environment variables from .env
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")  # Fetch from .env

    # Initialize CSRF protection
    CSRFProtect(app)
    
    # Flask force to clear cache each time
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Configure MongoDB
    app.config['MONGO_URI'] = os.getenv("MONGO_URI")

    # Initialize PyMongo with the Flask app
    mongo.init_app(app)

    # Ensure the app context is pushed to test the MongoDB connection
    with app.app_context():
        try:
            mongo.cx.admin.command('ping')
            print("Connected to MongoDB Atlas")
        except Exception as e:
            print(f"Connection failed: {e}")

        print("MongoDb initialized:", mongo.db)
        print("MongoDB connection:", mongo)
        print("MONGO_URI from .env:", os.getenv("MONGO_URI"))
    
    # Cookies duration
    app.config['REMEMBER_COOKIE_DURATION'] = 60 * 60 * 24 * 7  # 1 week
    
    # Session implementation
    app.config["SESSION_PERMANENT"] = True
    app.config["SESSION_USE_SIGNER"] = True
    app.config["PERMANENT_SESSION_LIFETIME"] = 60 * 60 * 24 * 7
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

    # Set the folder to save avatar images
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static/uploads')

    
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
    from history import history_bp



    
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
    app.register_blueprint(history_bp, url_prefix='/history')

    @app.route('/')
    def home():
        return render_template('index.html')
    
    # Use current_user in templates
    @app.context_processor
    def inject_user():

        if current_user.is_authenticated:
            # Add a default avatar if the user's avatar is not set
            user_data = {
                'username': current_user.username,
                'avatar': current_user.avatar if hasattr(current_user, 'avatar') and current_user.avatar else 'default_avatar.png'
            }
        else:
            user_data = None  # No user data if not authenticated

        return {'current_user': user_data}
    

        return {'current_user': current_user}

    return app

# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 

