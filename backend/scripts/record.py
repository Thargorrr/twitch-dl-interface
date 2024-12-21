import streamlink

def record_stream(url, quality, output):
    streams = streamlink.streams(url)
    stream = streams.get(quality, streams['best'])
    with stream.open() as fd:
        with open(output, 'wb') as out_file:
            while True:
                data = fd.read(1024)
                if not data:
                    break
                out_file.write(data)
