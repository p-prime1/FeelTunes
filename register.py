from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId
from forms import RegisterForm
from send_confirmation_email import generate_confirmation_token, confirm_token
from flask import current_app
from flask_mail import Mail, Message
from app import mongo

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
        
        
        if mongo.db.users.find_one({"email": email}):
            flash("Email already registered", "danger")
            return render_template('register.html', form=form)
        
        # Hash the password and save user to the database
        hashed_password = generate_password_hash(password)
        new_user = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "is_confirmed": False
        }
        mongo.db.users.insert_one(new_user)
        
        # Send confirmation email
        send_confirmation_email(email, username)
        
        print(confirm_token)
        
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

    user = mongo.db.users.find_one({"email": email})
    if user and user.get("is_confirmed"):
        flash("Account already confirmed. Please log in.", "success")
    elif user:
        mongo.db.users.update_one({"_id": user["_id"]}, {"$set": {"is_confirmed": True}})
        flash("Your email has been confirmed. You can now log in.", "success")
    else:
        flash("User not found", "danger")
    return redirect('/login/')
