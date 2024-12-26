from flask import Blueprint, render_template, request, redirect, url_for

terms_bp = Blueprint('terms', __name__, template_folder='templates')

@terms_bp.route('/', methods=['GET', 'POST'])
def terms():
    if request.method == 'POST':
        if 'accept_terms' in request.form:
            return redirect(url_for('success_page'))
    return render_template('terms.html')