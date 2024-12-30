from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

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

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header()
    query = f"?q={artist_name}&type=artist&limit=1"

    
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    
    return json_result[0]

def search_for_playlist(token, keyword):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header()
    query = f"?q={keyword}&type=playlist&limit=5"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content).get("playlists", {}).get("items", [])
    
    playlists = []
    for playlist in json_result:
        if playlist:  # Check if playlist is not None
            # Ensure the required fields exist
            if playlist.get("name") and playlist.get("external_urls", {}).get("spotify"):
                playlists.append({
                    "name": playlist["name"],
                    "url": playlist["external_urls"]["spotify"]
                })
    return playlists

token = get_token()
playlist_results = search_for_playlist(token, "party")
if playlist_results:
    print("\nPlaylists for 'party':")
    for i, playlist in enumerate(playlist_results, 1):
        print(f"{i}. {playlist['name']} - {playlist['url']}")
else:
    print("No playlists found for 'party'.")
