from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from flask_login import login_user
from models import User
from forms import LoginForm

login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        
        # Fetch user from the database
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            if not user.is_confirmed:
                flash("Please confirm your email first", "warning")
                return redirect(url_for('login.login'))
            login_user(user, remember=remember_me)
            flash("Login successful!", "success")
            return redirect(url_for('dashboard.dashboard', form=form))
        
            response = make_response(redirect(url_for('dashboard.dashboard')))
            if not request.cookies.get('cookies_accepted'):
                response.set_cookie('cookies_accepted', 'true', max_age=60*60*24*30)  # 30 days
            flash("Login successful!", "success")
            return response
        else:
            flash("Invalid username or password", "danger")

    return render_template('login.html', form=form)
