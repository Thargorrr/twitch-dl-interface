import sqlite3
from config.settings import DATABASE

def get_favorited_channels():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, image_url, info FROM channels WHERE favorited = 1')
        return cursor.fetchall()

def get_channel(channel_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM channels WHERE id = ?', (channel_id,))
        return cursor.fetchone()

def update_channel_config(channel_id, form):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE channels SET 
                          recording = ?, quality = ?, save_duration = ?, record_length = ?
                          WHERE id = ?''',
                       (form['recording'], form['quality'], form['save_duration'], form['record_length'], channel_id))
        conn.commit()

def search_channels(query):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, url FROM channels WHERE name LIKE ?', ('%' + query + '%',))
        return cursor.fetchall()
