from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from flask_login import login_user
from models import User
from forms import LoginForm
from app import mongo


login_bp = Blueprint('login', __name__)

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        
        # Fetch user from the database
        user = mongo.db.users.find_one({"username": username})

        if user and check_password_hash(user[password], password):
            user_obj = User(user)
            login_user(user_obj, remember=remember_me)

            if not user["is_confirmed"]:
                flash("Please confirm your email first", "warning")
                return redirect(url_for('login.login'))
        
            
            # Set session variables
            session['user_id'] = str(user["_id"])
            session['username'] = user["username"]
            session['email'] = user["email"]
            session['logged_in'] = True

            
            flash("Login successful!", "success")
            return redirect(url_for('dashboard.dashboard', form=form))

        else:
            flash("Invalid username or password", "danger")

    return render_template('login.html', form=form)
