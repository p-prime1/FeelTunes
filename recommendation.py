from flask import Blueprint, render_template

# Define the blueprint
recommendation_bp = Blueprint('recommendation', __name__, template_folder='templates')

# Route for the about page
@recommendation_bp.route('/')
def recommendation():
    return render_template('recommendation.html')
