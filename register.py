from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash
from models import User, db
from forms import RegisterForm
from send_confirmation_email import generate_confirmation_token, confirm_token
from flask import current_app
from flask_mail import Mail, Message

mail = Mail()
register_bp = Blueprint('register', __name__)


@register_bp.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # # Check if the "accept_terms" checkbox is checked
        # accept_terms = request.form.get('accept_terms')
        # if not accept_terms:
        #     flash("You must agree to the Terms of Service to register.", "danger")
        #     return redirect(url_for('register.register'))
        
        
        # Check if the username or email already exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            db.session.rollback()
            return render_template('register.html', form=form)
        if User.query.filter_by(email=email).first():
            flash("Email already registered", "danger")
            db.session.rollback()
            return render_template('register.html', form=form)
        
        # Hash the password and save user to the database
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        # Send confirmation email
        send_confirmation_email(email, username)
        
        
        flash("Registration successful! Please check your email to confirm your account.", "info")
        return redirect('/login/')
    return render_template('register.html', form=form)

def send_confirmation_email(email, username):
    try: 
        token = generate_confirmation_token(email)
        confirm_url = url_for('register.confirm_email', token=token, _external=True)
        subject = "Welcome to FeelTunes! Confirm Your Email"
        body = f"Hi {username},\n\nWelcome to FeelTunes! Please confirm your email by clicking the link below:\n{confirm_url}, \n\nBest regards,\nFeelTunes Team"
        
        msg = Message(subject, recipients=[email], body=body)
        mail = current_app.extensions.get('mail')
        mail.send(msg)
        
        print(f"Confirmation email sent to {email}")
        
    except Exception as e:
        print(f"Error sending email: {e}")
        
@register_bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash("The confirmation link is invalid or has expired.", "danger")
        return redirect('/register/')

    user = User.query.filter_by(email=email).first_or_404()
    if user.is_confirmed:
        flash("Account already confirmed. Please log in.", "success")
    else:
        user.is_confirmed = True
        db.session.commit()
        flash("Your email has been confirmed. You can now log in.", "success")
    return redirect('/login/')