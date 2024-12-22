# backend/twitch_api.py
import os
import requests
from config.settings import decrypt_data

def get_twitch_access_token():
    client_id = decrypt_data(os.getenv('TWITCH_CLIENT_ID'))
    client_secret = decrypt_data(os.getenv('TWITCH_CLIENT_SECRET'))
    
    response = requests.post('https://id.twitch.tv/oauth2/token', data={
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    })

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception('Failed to get access token from Twitch.')

def search_twitch_channels(query, access_token):
    url = f'https://api.twitch.tv/helix/search/channels?query={query}'
    headers = {
        'Client-ID': decrypt_data(os.environ['TWITCH_CLIENT_ID']),
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['data']