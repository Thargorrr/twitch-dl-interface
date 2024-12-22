import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import set_key, load_dotenv
from backend.db.operations import *
from backend.twitch_api import get_twitch_access_token, search_twitch_channels
from config.settings import encrypt_data, decrypt_data, ENV_PATH, initialize, get_database_path

initialize()

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/css')
load_dotenv(get_database_path())
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        access_token = get_twitch_access_token()
        channels = search_twitch_channels(query, access_token)
        return render_template('search.html', channels=channels)
    return render_template('search.html', channels=[])

@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    if request.method == 'POST':
        channel_id = request.form['channel_id']
        channel_name = request.form['channel_name']
        channel_image_url = request.form['channel_image_url']
        add_favorited_channel(channel_id, channel_name, channel_image_url)
        return redirect(url_for('favorites'))
    channels = get_favorited_channels()
    return render_template('favorites.html', channels=channels)

@app.route('/channel/<int:channel_id>/config', methods=['GET', 'POST'])
def config(channel_id):
    if request.method == 'POST':
        # Update channel configuration in the database
        update_channel_config(channel_id, request.form)
        return redirect('/favorites')
    channel = get_channel(channel_id)
    return render_template('config.html', channel=channel)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        client_secret = request.form.get('client_secret')

        if client_id and client_secret:
            encrypted_client_id = encrypt_data(client_id)
            encrypted_client_secret = encrypt_data(client_secret)
            
            set_key(ENV_PATH, 'TWITCH_CLIENT_ID', encrypted_client_id)
            set_key(ENV_PATH, 'TWITCH_CLIENT_SECRET', encrypted_client_secret)

            flash('Twitch credentials updated successfully.', 'success')
        else:
            flash('Both Client ID and Client Secret are required.', 'danger')

        return redirect(url_for('settings'))

    decrypted_client_id = decrypt_data(os.getenv('TWITCH_CLIENT_ID')) if os.getenv('TWITCH_CLIENT_ID') else ''
    decrypted_client_secret = decrypt_data(os.getenv('TWITCH_CLIENT_SECRET')) if os.getenv('TWITCH_CLIENT_SECRET') else ''
    
    return render_template('settings.html', client_id=decrypted_client_id, client_secret=decrypted_client_secret)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
