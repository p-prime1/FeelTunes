from flask import Flask, render_template
from models import User
from extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.secret_key = "_secret_key_hereYEBDBHBDHJHNBDYH"

    # Configure SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    # Set the login view route (for redirecting unauthenticated users)
    login_manager.login_view = 'login.login' 
    
    # Register blueprints
    from login import login_bp
    from register import register_bp
    from dashboard import dashboard_bp
    from about import about_bp
    from privacy import privacy_bp
    from recommendation import recommendation_bp
    from terms import terms_bp
    from profile import profile_bp
    
    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(register_bp, url_prefix='/register')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(about_bp, url_prefix='/about')
    app.register_blueprint(recommendation_bp, url_prefix='/recommendation')
    app.register_blueprint(privacy_bp, url_prefix='/privacy')
    app.register_blueprint(terms_bp, url_prefix='/terms')
    app.register_blueprint(profile_bp, url_prefix='/profile')

    @app.route('/')
    def home():
        return render_template('index.html')
    
    
    return app

# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 