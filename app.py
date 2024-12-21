from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        search_results = search_channels(query)
        return render_template('search.html', results=search_results)
    return render_template('search.html', results=[])


@app.route('/favorites')
def favorites():
    # Fetch favorited channels from the database
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
    app.run(debug=True)
