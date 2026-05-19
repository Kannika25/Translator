from flask import Flask, request, render_template, jsonify
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
import io

app = Flask(__name__)

# Supported target languages: display name -> (translator_code, gtts_code)
LANGUAGES = {
    "Kannada":   ("kn", "kn"),
    "Hindi":     ("hi", "hi"),
    "Tamil":     ("ta", "ta"),
    "Telugu":    ("te", "te"),
    "Malayalam": ("ml", "ml"),
    "Bengali":   ("bn", "bn"),
    "Marathi":   ("mr", "mr"),
    "French":    ("fr", "fr"),
    "Spanish":   ("es", "es"),
    "German":    ("de", "de"),
    "Japanese":  ("ja", "ja"),
    "Arabic":    ("ar", "ar"),
}

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = ""
    original_text = ""
    audio_data = None
    target_lang = "Kannada"
    error = None

    if request.method == 'POST':
        original_text = request.form.get('text', '').strip()
        target_lang = request.form.get('target_lang', 'Kannada')

        if original_text:
            try:
                lang_codes = LANGUAGES.get(target_lang, ("kn", "kn"))
                translator_code, gtts_code = lang_codes

                # Translate
                translator = GoogleTranslator(source='en', target=translator_code)
                translated_text = translator.translate(original_text)

                # Generate Audio
                if translated_text:
                    tts = gTTS(text=translated_text, lang=gtts_code)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    audio_data = base64.b64encode(fp.read()).decode('utf-8')

            except Exception as e:
                error = f"Translation failed: {str(e)}"

    return render_template(
        'index.html',
        original_text=original_text,
        translated_text=translated_text,
        audio_data=audio_data,
        target_lang=target_lang,
        languages=list(LANGUAGES.keys()),
        error=error
    )

if __name__ == '__main__':
    app.run(debug=True)
