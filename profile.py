from flask import Blueprint, request, render_template, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from extensions import db
import os
from werkzeug.utils import secure_filename
from flask import current_app
from profileupdateform import ProfileUpdateForm
from utils import send_email



profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileUpdateForm()

    email_updated = False
    password_updated = False

    # Handle the update form
    if form.validate_on_submit():
        if form.email.data and form.email.data != current_user.email:
            current_user.email = form.email.data
            email_updated = True
        
        if form.password.data:
            current_user.password = generate_password_hash(form.password.data)
            password_updated = True
            
        # Handle the avatar update
        if form.avatar.data:
            avatar_file = form.avatar.data
            avatar_filename = secure_filename(avatar_file.filename)
            avatar_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], avatar_filename))
            current_user.avatar = avatar_filename

        # Handle the bio update
        if form.bio.data:
            current_user.bio = form.bio.data

        try:
            db.session.commit()
            
            # Send notification emails
            if email_updated:
                send_email(
                    to=current_user.email,
                    subject="Email Updated",
                    body=f"Hi {current_user.username},\n\nYour email address has been successfully updated.\n\nBest regards,\nFeelTunes Team"
                )
            if password_updated:
                send_email(
                    to=current_user.email,
                    subject="Password Updated",
                    body=f"Hi {current_user.username},\n\nYour password has been successfully updated. \n\nIf you did not make this change, please contact us immediately.\n\nBest regards,\nFeelTunes Team"
                )
                
            flash('Your profile has been updated.', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')

        return redirect(url_for('profile.profile'))

    return render_template('profile.html', user=current_user, form=form)


@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileUpdateForm()

    if form.validate_on_submit():
        if form.avatar.data:
            avatar_file = form.avatar.data
            avatar_filename = secure_filename(avatar_file.filename)
            avatar_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], avatar_filename))
            current_user.avatar = avatar_filename
        
        if form.bio.data:
            current_user.bio = form.bio.data
        
        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.profile'))

    return render_template('edit_profile.html', user=current_user, form=form)
