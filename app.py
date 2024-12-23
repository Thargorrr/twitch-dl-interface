import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_caching import Cache
from dotenv import set_key, load_dotenv
from backend.db.operations import *
from backend.twitch_api import get_twitch_access_token, search_twitch_channels

initialize()

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
load_dotenv(ENV_PATH, override=True)
app.secret_key = os.getenv('SECRET_KEY')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    # Retrieve query from URL if it's a GET request, otherwise from the form
    query = request.args.get('query') if request.method == 'GET' else request.form['query']
    
    if query:
        # Check if we have cached results
        cached_channels = cache.get(query)
        if cached_channels:
            return render_template('search.html', channels=cached_channels, query=query)
        
        access_token = get_twitch_access_token()
        channels = search_twitch_channels(query, access_token)
        # Cache the results for 10 minutes
        cache.set(query, channels, timeout=10 * 60)
        return render_template('search.html', channels=channels, query=query)
    
    return render_template('search.html', channels=[], query=query)

@app.route('/favorites')
def favorites():
    return render_template('favorites.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    # Handle form submission for new credentials
    if request.method == 'POST':
        # Get client_id and client_secret from form input
        client_id = request.form.get('client_id')
        client_secret = request.form.get('client_secret')
        print(f"client_id: {client_id}, client_secret: {client_secret}")

        # If both fields are filled, encrypt and save them to .env file
        if client_id and client_secret:
            encrypted_client_id = encrypt_data(client_id)
            encrypted_client_secret = encrypt_data(client_secret)
            print(f"encrypted_client_id: {encrypted_client_id}, encrypted_client_secret: {encrypted_client_secret}")
            print(f"Nach dem entcrypten: client_id: {client_id}, client_secret: {client_secret}")
            # Save the encrypted credentials to the .env file
            set_key(ENV_PATH, 'TWITCH_CLIENT_ID', encrypted_client_id)
            set_key(ENV_PATH, 'TWITCH_CLIENT_SECRET', encrypted_client_secret)

            load_dotenv(ENV_PATH, override=True)

            flash('Twitch credentials updated successfully.', 'success')
        else:
            flash('Both Client ID and Client Secret are required.', 'danger')

        # After saving, reload the credentials from the .env file and decrypt them
        decrypted_client_id = decrypt_data(os.getenv('TWITCH_CLIENT_ID')) if os.getenv('TWITCH_CLIENT_ID') else ''
        decrypted_client_secret = decrypt_data(os.getenv('TWITCH_CLIENT_SECRET')) if os.getenv('TWITCH_CLIENT_SECRET') else ''
        print(f"decrypted_client_id: {decrypted_client_id}, decrypted_client_secret: {decrypted_client_secret}")
        return render_template('settings.html', 
                               client_id=decrypted_client_id, 
                               client_secret=decrypted_client_secret,
                               censored_client_id="****" if decrypted_client_id else None,
                               censored_client_secret="****" if decrypted_client_secret else None)

    load_dotenv(ENV_PATH, override=True)

    # Decrypt the saved credentials if they exist
    decrypted_client_id = decrypt_data(os.getenv('TWITCH_CLIENT_ID')) if os.getenv('TWITCH_CLIENT_ID') else None
    decrypted_client_secret = decrypt_data(os.getenv('TWITCH_CLIENT_SECRET')) if os.getenv('TWITCH_CLIENT_SECRET') else None
    print(f"decrypted_client_id: {decrypted_client_id}, decrypted_client_secret: {decrypted_client_secret}")
    # Create censored versions if not available
    censored_client_id = "****" if decrypted_client_id else None
    censored_client_secret = "****" if decrypted_client_secret else None

    # Render the settings page with current credentials (either decrypted or censored)
    return render_template(
        'settings.html', 
        client_id=decrypted_client_id,
        client_secret=decrypted_client_secret,
        censored_client_id=censored_client_id,
        censored_client_secret=censored_client_secret
    )

@app.route('/get_credentials', methods=['GET'])
def get_credentials():
    load_dotenv(ENV_PATH, override=True)
    decrypted_client_id = decrypt_data(os.getenv('TWITCH_CLIENT_ID')) if os.getenv('TWITCH_CLIENT_ID') else None
    decrypted_client_secret = decrypt_data(os.getenv('TWITCH_CLIENT_SECRET')) if os.getenv('TWITCH_CLIENT_SECRET') else None
    print(f"decrypted_client_id: {decrypted_client_id}, decrypted_client_secret: {decrypted_client_secret}")
    return jsonify({
        'client_id': decrypted_client_id,
        'client_secret': decrypted_client_secret
    })

@app.route('/channel/<int:channel_id>/config', methods=['GET', 'POST'])
def config(channel_id):
    if request.method == 'POST':
        # Update channel configuration in the database
        update_channel_config(channel_id, request.form)
        return redirect('/favorites')
    channel = get_channel(channel_id)
    return render_template('config.html', channel=channel)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
