from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from spotify_api import fetch_playlist_for_mood
from datetime import datetime

recommendation_bp = Blueprint('recommendation', __name__, template_folder='templates')

@recommendation_bp.route('/', methods=['GET'])
@login_required
def recommendation():
    """
    Recommend a playlist based on the day of the week and current time.
    """
    try:
        # Get current day and time
        current_time = datetime.now()
        day_of_week = current_time.strftime('%A')  # E.g., 'Monday'
        hour = current_time.hour  # 24-hour format

        # Determine mood based on time of day
        if 6 <= hour < 12:  # Morning
            mood = 'energetic'
        elif 12 <= hour < 18:  # Afternoon
            mood = 'relaxed'
        elif 18 <= hour < 22:  # Evening
            mood = 'happy'
        else:  # Night
            mood = 'calm'

        # Fetch playlist based on mood
        playlist = fetch_playlist_for_mood(mood)

        if not playlist:
            flash(f"No playlists found for mood '{mood}'.", "warning")
            return redirect(url_for('dashboard.dashboard'))

        # Render template with the recommended playlist
        return render_template(
            'recommendation.html',
            playlist=playlist,
            mood=mood,
            day_of_week=day_of_week,
            time=current_time.strftime('%I:%M %p'),  # Format: HH:MM AM/PM
            user=current_user
        )

    except Exception as e:
        print(f"Error in recommendation route: {str(e)}")
        flash("An error occurred while fetching the recommendation.", "danger")
        return redirect(url_for('dashboard.dashboard'))
