from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from extensions import db
from profileupdateform import ProfileUpdateForm

profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def profile():
    
    form = ProfileUpdateForm()
    
    # Update the user's email and password
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.password = generate_password_hash(form.password.data)
        
        try:
            db.session.commit()
            flash('Your profile has been updated.', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error updating profile: {str(e)}', 'danger')
    
        return redirect(url_for('profile.profile'))
    
    return render_template('profile.html', user=current_user, form=form)

@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

    #Validating user information
        if username:
            current_user.username = username
        if email:
            current_user.email = email
        if password:
            current_user.password = generate_password_hash(password)

        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile', user_id=current_user.id))
    return render_template('edit_profile.html', user=current_user)
