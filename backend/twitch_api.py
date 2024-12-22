# backend/twitch_api.py
import requests
from config.settings import TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET

def get_twitch_access_token():
    url = 'https://id.twitch.tv/oauth2/token'
    payload = {
        'client_id': TWITCH_CLIENT_ID,
        'client_secret': TWITCH_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()['access_token']

def search_twitch_channels(query, access_token):
    url = f'https://api.twitch.tv/helix/search/channels?query={query}'
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']
