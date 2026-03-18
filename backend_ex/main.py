from flask import Flask
from flask_cors import CORS
from flask_sock import Sock
import numpy as np
import whisper
import tempfile, os, json
import soundfile as sf
from murf import Murf
from google import genai
from dotenv import load_dotenv

load_dotenv()

# 🔐 Use ENV variables in real projects
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_ai(text):
    prompt = f"""
You are Echo, a helpful voice assistant for blind users.
Reply with short and simple answers.
Use easy English.
Maximum two sentences.

If user wants to open a website:
ONLY return in this format:
https://example.com open

No extra words.

User: {text}
Assistant:
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text.strip()


app = Flask(__name__)
CORS(app)
sock = Sock(app)

model = whisper.load_model("base")

BUFFER_SECONDS = 4
SAMPLE_RATE = 16000
buffer = []

@sock.route('/audio')
def audio_stream(ws):
    global buffer

    murf_client = Murf(api_key=os.getenv("MURF_API_KEY"))

    while True:
        data = ws.receive()

        if data is None:
            break

        audio_chunk = np.frombuffer(data, dtype=np.float32)
        buffer.extend(audio_chunk)

        if len(buffer) >= SAMPLE_RATE * BUFFER_SECONDS:

            audio_np = np.array(buffer[:SAMPLE_RATE * BUFFER_SECONDS], dtype=np.float32)
            buffer = []

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                sf.write(f.name, audio_np, SAMPLE_RATE)
                temp_path = f.name

            try:
                result = model.transcribe(temp_path)
                user_text = result["text"].strip()
                print("User:", user_text)
            except Exception as e:
                print("Whisper error:", e)
                os.remove(temp_path)
                continue

            os.remove(temp_path)

            if user_text == "":
                continue

            ai_text = ask_ai(user_text)
            print("AI:", ai_text)

            if "open" in ai_text and "http" in ai_text:
                response_payload = {
                    "type": "open",
                    "data": ai_text.replace(" open", "").strip()
                }
                ws.send(json.dumps(response_payload))
                continue

            tts = murf_client.text_to_speech.generate(
                text=ai_text,
                voice_id="Terrell",
                locale="en-US"
            )

            response_payload = {
                "type": "audio",
                "data": tts.audio_file
            }

            ws.send(json.dumps(response_payload))


if __name__ == "__main__":
    app.run(port=5000, debug=True)