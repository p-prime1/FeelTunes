from flask import Blueprint, redirect, url_for, flash, session
from flask_login import logout_user

# Define the blueprint
logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'success')
    
    print(session)  # Add this line to inspect the session data

    return redirect(url_for('login.login'))
