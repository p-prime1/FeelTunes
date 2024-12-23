from flask import Blueprint, render_template

# Define the blueprint
terms_bp = Blueprint('terms', __name__, template_folder='templates')

# Route for the about page
@terms_bp.route('/')
def terms():
    return render_template('terms.html')
