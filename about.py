from flask import Blueprint, render_template
from flask_login import current_user

# Define the blueprint
about_bp = Blueprint('about', __name__, template_folder='templates')

# Route for the about page
@about_bp.route('/')
def about():
    return render_template('about.html')
