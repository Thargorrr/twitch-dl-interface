import streamlink
import sqlite3
from config.settings import DATABASE

def record_stream(channel_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT url, quality FROM channels WHERE id = ?', (channel_id,))
        channel = cursor.fetchone()
        if not channel:
            return
        url, quality = channel

        streams = streamlink.streams(url)
        stream = streams.get(quality, streams['best'])

        output = f"recordings/{channel_id}/{quality}.mp4"
        with stream.open() as fd:
            with open(output, 'wb') as out_file:
                while True:
                    data = fd.read(1024)
                    if not data:
                        break
                    out_file.write(data)
