from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import History

history_bp = Blueprint('history', __name__, template_folder='templates')

@history_bp.route('/', methods=['GET'])
@login_required
def view_history():
    # Fetch history for the logged-in user
    user_history = History.query.filter_by(user_id=current_user.id).order_by(History.timestamp.desc()).all()
    
    return render_template('history.html', history=user_history, user=current_user)
