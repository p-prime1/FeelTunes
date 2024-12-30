from flask import Blueprint, render_template, request, jsonify, session, flash
from spotify_api import fetch_playlist_for_mood  # Hypothetical helper for fetching playlists
from flask_login import login_required, current_user
import os

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    user = {"username": current_user.username} 
    songs = os.listdir('static/music') # songs to be gotten from spotify_api
    return render_template('dashboard.html', user=user, songs=songs)

@dashboard_bp.route('/generate-playlist/', methods=['POST'])
def generate_playlist():
    
    data = request.get_json()
    mood = data.get('mood')

    if not mood:
        return jsonify({'error': 'Mood not provided'}), 400

    try:
        playlist = fetch_playlist_for_mood(mood)  # Fetch playlist based on mood
        return jsonify({'playlist': playlist})
    except Exception as e:
        return jsonify({'error': 'Failed to fetch playlist', 'details': str(e)}), 500
