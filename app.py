from flask import Flask, render_template, request, redirect, url_for
from backend.db.operations import *
from backend.twitch_api import get_twitch_access_token, search_twitch_channels
# get_favorited_channels, get_channel, update_channel_config, search_channels

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/css')

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


@app.route('/settings')
def settings():
    return render_template('settings.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
