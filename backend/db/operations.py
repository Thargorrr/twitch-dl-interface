import sqlite3
from config.settings import DATABASE

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS channels (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL,
                          image_url TEXT NOT NULL,
                          info TEXT,
                          quality TEXT NOT NULL,
                          save_duration TEXT NOT NULL,
                          record_length INTEGER,
                          favorited INTEGER DEFAULT 0)''')
        conn.commit()
def get_favorited_channels():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, image_url, info FROM channels WHERE favorited = 1')
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"General error: {e}")
        return []

def add_favorited_channel(channel_id, channel_name, channel_image_url):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO channels (id, name, image_url, favorited) 
                              VALUES (?, ?, ?, 1) 
                              ON CONFLICT(id) DO UPDATE SET favorited=1''',
                           (channel_id, channel_name, channel_image_url))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"General error: {e}")

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

# Ensure the database and tables are created
init_db()