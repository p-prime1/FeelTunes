from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from spotify_api import fetch_playlist_for_mood 
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

class MoodForm(FlaskForm):
    mood = SelectField(choices=[('happy', 'Happy'), ('sad', 'Sad'), ('relaxed', 'Relaxed'), ('energetic', 'Energetic')], validators=[DataRequired()])

@dashboard_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    form = MoodForm()
    user = {"username": current_user.username}
    return render_template('dashboard.html', user=user, form=form)

@dashboard_bp.route('/generate_playlist/', methods=['POST'])
@login_required
def generate_playlist():
    data = request.get_json()
    print("Received data:", data)
    
    try:
        if not data or 'mood' not in data:
            print("Error: 'mood' key missing in request.")
            return jsonify({'error': 'Mood not provided'}), 400

        mood = data['mood']
        print(f"Selected mood: {mood}")
        playlist = fetch_playlist_for_mood(mood)
        print(f"Fetched Playlist: {playlist}")
        
        if playlist is None:  # If an error occurred in fetching playlists
            return jsonify({'error': 'Error fetching playlists. Please try again.'}), 500


        if not playlist:
            return jsonify({'message': f'No playlists found for mood "{mood}".'}), 404

        return jsonify({'playlist': playlist}), 200
    except Exception as e:
        print(f"Error in generate_playlist: {str(e)}")
        return jsonify({'error': 'Server error. Please try again.'}), 500
    1
    