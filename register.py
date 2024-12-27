from flask import Blueprint, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash
from models import User, db
from forms import RegisterForm

register_bp = Blueprint('register', __name__)

@register_bp.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        
        
        # Check if the username or email already exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            return render_template('register.html', form=form)
        if User.query.filter_by(email=email).first():
            flash("Email already registered", "danger")
            return render_template('register.html', form=form)
        
        # Hash the password and save user to the database
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! Please log in.", "success")
        return redirect('/login/')
    return render_template('register.html', form=form)
