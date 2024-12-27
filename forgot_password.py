from flask import Blueprint, request, render_template, flash, redirect, url_for, current_app
from itsdangerous import URLSafeTimedSerializer
from models import User, db
from werkzeug.security import generate_password_hash
from utils import send_email
from forms import ResetPasswordForm

forgot_password_bp = Blueprint('forgot_password', __name__)

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.secret_key)
    return serializer.dumps(email, salt="password-reset-salt")

def confirm_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.secret_key)
    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=expiration)
    except Exception:
        return None
    return email

@forgot_password_bp.route('/', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate reset token
            token = generate_reset_token(email)
            reset_url = url_for('forgot_password.reset_password', token=token, _external=True)

            # Send email
            subject = "Reset Your Password"
            body = f"Hi {user.username},\n\nClick the link below to reset your password:\n{reset_url}\n\nIf you did not request this, please ignore this email.\n\nBest regards,\nFeelTunes Team"
            send_email(email, subject, body)

            flash("Password reset link has been sent to your email.", "success")
        else:
            flash("Email not found.", "danger")
        return redirect(url_for('forgot_password.forgot_password'))

    return render_template('forgot_password.html')


@forgot_password_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = confirm_reset_token(token)
    if not email:
        flash("The reset link is invalid or has expired.", "danger")
        return redirect(url_for('forgot_password.forgot_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user:
            try:
                user.password = generate_password_hash(form.password.data)
                db.session.commit()
                
                flash("Your password has been reset. You can now log in.", "success")
                return redirect(url_for('login.login'))
            except Exception as e:
                db.session.rollback()
                flash("An error occurred while resetting the password. Please try again.", "danger")
        else:
            flash("User not found.", "danger")

    print("Decoded email:", email)

    return render_template('reset_password.html', token=token, form=form)   
