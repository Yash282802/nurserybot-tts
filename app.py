from flask import Flask, request, send_file
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def text_to_speech():
    data = request.json
    text = data.get('text', '')
    lang = data.get('lang', 'en')
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save('output.mp3')
    return send_file('output.mp3',
                    mimetype='audio/mpeg',
                    as_attachment=True,
                    download_name='audio.mp3')

@app.route('/')
def home():
    return 'NurseryBot TTS is running! 🎵'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
