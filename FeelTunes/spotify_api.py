from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

# Load environment variables
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {"grant_type": "client_credentials"}
    
    result = post(url, headers=headers, data=data)
    json_result = result.json()
    token = json_result["access_token"]
    return token


def get_auth_header():
    token = get_token()
    return {"Authorization": "Bearer " + token}


def fetch_playlist_for_mood(mood):
    """
    Fetch playlists for a given mood from Spotify's API.
    """
    
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header()
    query = f"?q={mood}&type=playlist&limit=15"
    query_url = url + query

    try:
        result = get(query_url, headers=headers)
        result.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse JSON safely
        try:
            json_result = result.json()
            
        except ValueError as e:
            print(f"Error decoding JSON response: {str(e)}")
            return []
                
        playlists = json_result.get("playlists", {}).get("items", [])

        if not playlists:
            print(f"No playlists found for mood: {mood}")
            return []
        
        playlists = [playlist for playlist in playlists if playlist is not None]

        return [
            {
                "name": playlist.get("name"),
                "url": playlist.get("external_urls", {}).get("spotify"),
                "description": playlist.get("description", "No description available."),
                "image": playlist.get("images", [{}])[0].get("url", "No image available")
            }
            for playlist in playlists
            if playlist.get("name") and playlist.get("external_urls", {}).get("spotify")
        ]
        
    except Exception as e:
        print(f"Error fetching playlists: {str(e)}")
        return None