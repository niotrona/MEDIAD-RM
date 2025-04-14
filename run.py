from flask import Flask, Response, request, render_template_string
import requests

app = Flask(__name__)

STREAM_URL = "https://us.hirahi.sbs/hls/ZRRRQ.m3u8"
USER_AGENT = "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"
REFERER = "http://www.fawanews.com/"
ORIGIN = "http://www.fawanews.com"

@app.route('/proxy/<path:url>')
def proxy(url):
    headers = {
        'User-Agent': USER_AGENT,
        'Referer': REFERER,
        'Origin': ORIGIN
    }
    r = requests.get(url, headers=headers, stream=True)
    return Response(r.iter_content(chunk_size=8192), content_type=r.headers['Content-Type'])

@app.route('/')
def player():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Stream Player</title>
        <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    </head>
    <body>
        <video id="video" controls width="800"></video>
        <script>
            const video = document.getElementById('video');
            if(Hls.isSupported()) {
                const hls = new Hls();
                hls.loadSource("/proxy/{{ stream_url }}");
                hls.attachMedia(video);
                hls.on(Hls.Events.MANIFEST_PARSED, function() {
                    video.play();
                });
            } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                video.src = "/proxy/{{ stream_url }}";
                video.addEventListener('loadedmetadata', function() {
                    video.play();
                });
            }
        </script>
    </body>
    </html>
    ''', stream_url=STREAM_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
