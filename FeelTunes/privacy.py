from flask import Blueprint, render_template, session
from flask_login import current_user

# Define the blueprint
privacy_bp = Blueprint('privacy', __name__, template_folder='templates')

# Route for the about page
@privacy_bp.route('/')
def privacy():
    return render_template('privacy.html')
