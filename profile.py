from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from profileupdateform import ProfileUpdateForm
from bson.objectid import ObjectId

profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def profile():
    
    form = ProfileUpdateForm()
    
    # Update the user's email and password
    if form.validate_on_submit():
        update_data = {}
        update_data['email'] = form.email.data
        update_data['password'] = generate_password_hash(form.password.data)

        try:
            current_app.mongo.db.users.update_one(
                {'_id': ObjectId(current_user.id)},
                {'$set': {'email': form.email.data, 'password': generate_password_hash(form.password.data)}}    
            )
            flash('Your profile has been updated.', 'success')
            current_user.email = form.email.data
            current_user.password = form.update_data['password']
        except Exception as e:
            db.session.rollback()
            flash(f'An error updating profile: {str(e)}', 'danger')
    
        return redirect(url_for('profile.profile'))
    
    return render_template('profile.html', user=current_user, form=form)

@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        update_data = {}
        if 'username' in request.form and request.form['username']:
            update_data['username'] = request.form['username']
            current_user.username = request.form['username']

        if 'email' in request.form and request.form['email']:
            update_data['email'] = request.form['email']
            current_user.email = request.form['email']

        if 'password' in request.form and request.form['password']:
            hashed_password = generate_password_hash(request.form['password'])
            update_data['password'] = hashed_password
            current_user.password = hashed_password

        if update_data:  # Update only if there's something to change
            current_app.mongo.db.users.update_one({'_id': ObjectId(current_user.id)}, {'$set': update_data})
            flash('Profile updated successfully!', 'success')
        else:
            flash('No changes were made.', 'info')

        return redirect(url_for('profile.profile'))

    user = current_app.mongo.db.users.find_one({"_id": ObjectId(current_user.id)})
    return render_template('edit_profile.html', user=user)
