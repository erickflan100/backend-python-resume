from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route("/")
def index():
    data = {
        'Mensagem': 'Resume está Ativo'
    }
    return jsonify(data)

@app.route("/transcript")
def result():
    transcript = YouTubeTranscriptApi.get_transcripts(["TPXr2fkz0EM"], languages=["pt"])
    texto = ""

    formatter = JSONFormatter()
    json_formatted = formatter.format_transcript(transcript)
    data = json.loads(json_formatted)

    data_list = data[0]

    texts = [item['text'] for item in data_list['TPXr2fkz0EM'] if 'text' in item]

    for text in texts:
        texto += text + " "
    data = {
        'Transcript': texto
    }
    return jsonify(data)