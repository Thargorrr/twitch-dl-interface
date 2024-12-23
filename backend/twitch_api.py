# backend/twitch_api.py
import os
import requests
import requests_cache
from dotenv import load_dotenv
from datetime import datetime
from config.settings import decrypt_data, ENV_PATH

# Set up requests cache
requests_cache.install_cache('twitch_cache', expire_after=600)  # Cache for 5 minutes

def get_twitch_access_token():
    load_dotenv(ENV_PATH, override=True)
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

import requests
import os

def search_twitch_channels(query, access_token):
    url = f'https://api.twitch.tv/helix/search/channels?query={query}'
    headers = {
        'Client-ID': decrypt_data(os.getenv('TWITCH_CLIENT_ID')),
        'Authorization': f'Bearer {access_token}'
    }
    
    # Fetch channels
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    channels = response.json()['data']

    for channel in channels:
        channel_id = channel['id']
        # Fetch additional channel information (including description)
        channel_info_url = f'https://api.twitch.tv/helix/users?id={channel_id}'
        channel_info_response = requests.get(channel_info_url, headers=headers)
        channel_info_response.raise_for_status()
        channel_info = channel_info_response.json().get('data', [])[0]

        # Debugging: Print the raw response to check the structure
        print("Channel Info Response:", channel_info_response.json())

        # Fetch the follower count from the channels/followers endpoint, with error handling
        try:
            follower_info_url = f'https://api.twitch.tv/helix/channels/followers?broadcaster_id={channel_id}'
            follower_info_response = requests.get(follower_info_url, headers=headers)
            follower_info_response.raise_for_status()
            follower_count = follower_info_response.json()['total']  # 'total' gives the follower count
        except requests.exceptions.HTTPError as e:
            # If we get an error, set follower count to 0 and continue
            print(f"Error fetching follower count for {channel_id}: {e}")
            follower_count = 0

        # Debugging: Print the follower count
        print("Follower Count:", follower_count)

        # Add the follower count and description
        if channel_info:
            channel['follower_count'] = follower_count
            channel['description'] = channel_info.get('description', 'No description available')
            channel['profile_image_url'] = channel_info.get('profile_image_url', 'https://static-cdn.jtvnw.net/user-default-pictures-uv/cdd517fe-def4-11e9-948e-784f43822e80-profile_image-300x300.png')
        else:
            channel['follower_count'] = 0
            channel['description'] = 'No description available'
            channel['profile_image_url'] = 'https://static-cdn.jtvnw.net/user-default-pictures-uv/cdd517fe-def4-11e9-948e-784f43822e80-profile_image-300x300.png'

        # Fetch stream information (live status, title, viewers, etc.)
        stream_info_url = f'https://api.twitch.tv/helix/streams?user_id={channel_id}'
        stream_info_response = requests.get(stream_info_url, headers=headers)
        stream_info_response.raise_for_status()
        streams = stream_info_response.json()['data']

        # Debugging: Print the raw response to check the structure
        print("Stream Info Response:", stream_info_response.json())

        if streams:
            stream = streams[0]
            channel['is_live'] = True
            channel['stream_title'] = stream['title']
            channel['viewer_count'] = stream['viewer_count']
            channel['thumbnail_url'] = get_stream_thumbnail_url(stream['thumbnail_url'], width=400, height=225)
            channel['stream_duration'] = calculate_stream_duration(stream['started_at'])
        else:
            channel['is_live'] = False
            # Adding fallback info for channels that are not live
            channel['last_live'] = 'Last live ' + channel_info.get('last_broadcast', 'unknown')

        # Calculate a relevance score based on the search query
        relevance_score = calculate_relevance_score(query, channel['display_name'], channel['description'])

        # Debugging: Print the relevance score for each channel
        print(f"Relevance Score for {channel['display_name']}: {relevance_score}")
        
        # Add a score for viewers/followers (normalize the values to a reasonable scale)
        follower_score = min(channel['follower_count'] / 10000, 1)  # Scale follower count
        viewer_score = min(channel.get('viewer_count', 0) / 10000, 1)  # Scale viewer count

        # Combine the scores (you can adjust the weights as needed)
        channel['final_score'] = relevance_score * 0.4 + viewer_score * 0.3 + follower_score * 0.3

    # Sort the channels based on the final score (highest first)
    channels.sort(key=lambda x: x['final_score'], reverse=True)

    return channels

def calculate_relevance_score(query, channel_name, channel_description):
    """Calculates a simple relevance score based on query matching."""
    query_terms = query.lower().split()  # Split the query into words
    score = 0
    
    # Check how many of the query terms appear in the channel name or description
    for term in query_terms:
        if term in channel_name.lower():
            score += 1
        if term in channel_description.lower():
            score += 1
    
    return score

def calculate_stream_duration(start_time_str):
    # Parse the stream start time (ISO 8601 format)
    start_time = datetime.fromisoformat(start_time_str.rstrip('Z'))

    # Get the current time
    current_time = datetime.utcnow()

    # Calculate the time difference
    duration = current_time - start_time

    # Extract hours and minutes
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60

    return f"{hours}h {minutes}min"

def get_stream_thumbnail_url(thumbnail_url, width, height):
    # Replace {width} and {height} placeholders with actual values
    return thumbnail_url.format(width=width, height=height)