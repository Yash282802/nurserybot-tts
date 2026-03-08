from flask import Flask, request, send_file
from gtts import gTTS
import os
import uuid
import time

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def text_to_speech():
    try:
        data = request.json
        text = data.get('text', '')
        lang = data.get('lang', 'en')
        
        # Limit text length
        text = text[:2000]
        
        # Create unique filename
        filename = f"{uuid.uuid4()}.mp3"
        
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filename)
        
        response = send_file(
            filename,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='audio.mp3'
        )
        
        # Cleanup after sending
        @response.call_on_close
        def cleanup():
            if os.path.exists(filename):
                os.remove(filename)
                
        return response
        
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/')
def home():
    return 'NurseryBot TTS is running! 🎵'

@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
