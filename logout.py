from flask import Blueprint, redirect, url_for, flash
from flask_login import logout_user

# Define the blueprint
logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login.login'))
