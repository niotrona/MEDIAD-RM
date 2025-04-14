from flask import Flask, Response
import requests

app = Flask(__name__)

STREAM_URL = "https://ca8s9.crackstreamslivehd.com/global/disney1/index.m3u8?token=bcdccee993e640e1348812404139818ef49a746f-0a-1744693562-1744661162&ip=196.65.185.163"

@app.route('/stream.m3u8')
def proxy_stream():
    # Forward the HLS stream
    r = requests.get(STREAM_URL, stream=True)
    return Response(r.iter_content(chunk_size=8192), content_type=r.headers['Content-Type'])

@app.route('/')
def player():
    return """
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Disney+ Stream</h1>
        <video width="800" controls autoplay>
            <source src="/stream.m3u8" type="application/x-mpegURL">
        </video>
        <p>If playback fails, try refreshing or check browser HLS support.</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
