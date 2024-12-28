from flask import Blueprint, render_template, session

# Define the blueprint
privacy_bp = Blueprint('privacy', __name__, template_folder='templates')

# Route for the about page
@privacy_bp.route('/')
def privacy():
    return render_template('privacy.html')
