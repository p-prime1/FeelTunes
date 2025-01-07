from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import pygame
import requests
from threading import Thread

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize pygame mixer
pygame.mixer.init()

# Last.fm API credentials
LASTFM_API_KEY = "814c72ddc961e78bf5bab7e0b32be363"
LASTFM_API_URL = "http://ws.audioscrobbler.com/2.0/"

# Globals
current_track = None
is_paused = False
playlist = []


# Play audio in a separate thread
def play_audio(filepath):
    global is_paused
    try:
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Error playing audio: {e}")
    is_paused = False


@app.route('/')
def index():
    return render_template('index.html', playlist=playlist)


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        playlist.append(file.filename)
        return jsonify({'message': 'File uploaded', 'playlist': playlist})
    return jsonify({'message': 'No file uploaded'}), 400


@app.route('/play/<filename>')
def play(filename):
    global current_track
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        current_track = filename
        Thread(target=play_audio, args=(filepath,), daemon=True).start()
        return jsonify({'message': f'Playing {filename}'})
    else:
        return jsonify({'message': 'File not found'}), 404


@app.route('/pause')
def pause():
    global is_paused
    if pygame.mixer.music.get_busy():
        if not is_paused:
            pygame.mixer.music.pause()
            is_paused = True
            return jsonify({'message': 'Playback paused'})
        else:
            pygame.mixer.music.unpause()
            is_paused = False
            return jsonify({'message': 'Playback resumed'})
    return jsonify({'message': 'No audio playing'}), 400


@app.route('/stop')
def stop():
    global current_track
    pygame.mixer.music.stop()
    current_track = None
    return jsonify({'message': 'Playback stopped'})


@app.route('/rewind')
def rewind():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.rewind()
        return jsonify({'message': 'Audio rewound'})
    return jsonify({'message': 'No audio playing'}), 400


@app.route('/metadata/<track>')
def get_metadata(track):
    """
    Fetch metadata from Last.fm for the given track.
    """
    params = {
        'method': 'track.search',
        'track': track,
        'api_key': LASTFM_API_KEY,
        'format': 'json'
    }
    response = requests.get(LASTFM_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and 'trackmatches' in data['results']:
            tracks = data['results']['trackmatches']['track']
            return jsonify({'metadata': tracks})
    return jsonify({'message': 'No metadata found'}), 404


@app.route('/search', methods=['GET'])
def search_music():
    """
    Search for music using the Last.fm API.
    """
    query = request.args.get('query', '')
    if not query:
        return jsonify({'message': 'No search query provided'}), 400

    params = {
        'method': 'track.search',
        'track': query,
        'api_key': LASTFM_API_KEY,
        'format': 'json'
    }
    response = requests.get(LASTFM_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and 'trackmatches' in data['results']:
            tracks = data['results']['trackmatches']['track']
            return jsonify({'tracks': tracks})
    return jsonify({'message': 'No tracks found'}), 404



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
