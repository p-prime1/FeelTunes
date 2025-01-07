from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from spotify_api import fetch_playlist_for_mood 
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import DataRequired
from models import History, db


dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

class MoodForm(FlaskForm):
    mood = SelectField(choices=[('happy', 'Happy'), ('sad', 'Sad'), ('relaxed', 'Relaxed'), ('energetic', 'Energetic')], validators=[DataRequired()])

@dashboard_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    form = MoodForm()
    moodState = current_user.mood_state
    emoji = get_mood_emoji(moodState) if moodState else None
    
    user = {"username": current_user.username,
            "avatar": current_user.avatar if hasattr(current_user, 'avatar') and current_user.avatar else 'default_avatar.png'}
    return render_template('dashboard.html', user=user, form=form, moodState=moodState, emoji=emoji)

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
        
        # Log the searched mood in the History table
        history_entry = History(user_id=current_user.id, mood=mood)
        db.session.add(history_entry)
        db.session.commit()
        
        if playlist is None:  # If an error occurred in fetching playlists
            return jsonify({'error': 'Error fetching playlists. Please try again.'}), 500


        if not playlist:
            return jsonify({'message': f'No playlists found for mood "{mood}".'}), 404

        return jsonify({'playlist': playlist}), 200
    except Exception as e:
        print(f"Error in generate_playlist: {str(e)}")
        return jsonify({'error': 'Server error. Please try again.'}), 500
    1
    
@dashboard_bp.route('/generate_playlist/', methods=['GET'])
@login_required
def generate_playlist_from_history():
    mood = request.args.get('mood')  # Get mood from query string
    if not mood:
        return redirect(url_for('dashboard.dashboard'))  # Redirect if no mood is provided

    # Fetch playlist for the given mood
    playlist = fetch_playlist_for_mood(mood)

    if not playlist:
        flash('No playlists found for the selected mood.', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    # You can render a template with the playlist or handle it accordingly
    return render_template('history.html', playlist=playlist, user=current_user)
    
    
def get_mood_emoji(mood):
    """Map mood to an emoji."""
    mood_emojis = {
        'happy': '😊',
        'sad': '😢',
        'angry': '😡',
        'relaxed': '😌',
        'energetic': '⚡',
        'excited': '🎉',
        'calm': '🧘',
    }
    return mood_emojis.get(mood.lower(), '🙂')  # Default emoji


@dashboard_bp.route('/dashboard/set_mood', methods=['POST'])
@login_required
def set_mood():
    
    """Set the user's mood and store it in the database."""
    mood = request.form.get('mood')

    # Save the mood in the database
    current_user.mood_state = mood
    db.session.commit()
    return redirect(url_for('dashboard.dashboard'))