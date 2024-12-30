from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from profileupdateform import ProfileUpdateFor
from .app import mongo
from bson.objectid import ObjectId

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
            mongo.db.users.update_one(
                {'_id': ObjectId(current_user.id)},
                {'$set': {'email': form.email.data, 'password': generate_password_hash(form.password.data)}}    
            )
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

        user_id = "current_user_id"

    #Validating user information
    update_data = {}
        if username:
            current_user.username = username
        if email:
            current_user.email = email
        if password:
            current_user.password = generate_password_hash(password)

        mongo.db.users.update_one({'_id': ObjectId(current_user.id)}, {'$set': update_data})


        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile', user_id=current_user.id))

    user = mongo.db.users.find_one({"_id": ObjectId("current_user_id")})
    return render_template('edit_profile.html', user=user)
