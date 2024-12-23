import random

def fetch_playlist_for_mood(mood):
    # Mocked playlists for each mood
    mock_playlists = {
        'happy': [
            {'title': 'Happy Song 1', 'artist': 'Artist A', 'url': 'https://spotify.com/track/1'},
            {'title': 'Happy Song 2', 'artist': 'Artist B', 'url': 'https://spotify.com/track/2'},
        ],
        'sad': [
            {'title': 'Sad Song 1', 'artist': 'Artist C', 'url': 'https://spotify.com/track/3'},
            {'title': 'Sad Song 2', 'artist': 'Artist D', 'url': 'https://spotify.com/track/4'},
        ],
        'relaxed': [
            {'title': 'Relaxed Song 1', 'artist': 'Artist E', 'url': 'https://spotify.com/track/5'},
            {'title': 'Relaxed Song 2', 'artist': 'Artist F', 'url': 'https://spotify.com/track/6'},
        ],
        'energetic': [
            {'title': 'Energetic Song 1', 'artist': 'Artist G', 'url': 'https://spotify.com/track/7'},
            {'title': 'Energetic Song 2', 'artist': 'Artist H', 'url': 'https://spotify.com/track/8'},
        ]
    }

    return mock_playlists.get(mood, [])
