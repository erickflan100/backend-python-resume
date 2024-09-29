from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from flask import Flask, jsonify, request
import json

# para rodar o flask -> flask --app index.py run
# para subir para o vercel -> vercel --prod
# para criar o requirements -> pip freeze > requirements.txt

app = Flask(__name__)

@app.route("/")
def index():
    data = {
        'Mensagem': 'Resume está Ativo'
    }
    return jsonify(data)

@app.route("/transcript")
def result():
    data = request.get_json()
    video_url = data.get('url')
    video_id = video_url.split("v=")[1]
    try:
        transcript = YouTubeTranscriptApi.get_transcripts([video_id], languages=["pt"])
    except:
        data = {
            'Mensagem': 'Erro ao buscar o transcript'
        }
        return jsonify(data), 500
    
    texto = ""

    formatter = JSONFormatter()
    json_formatted = formatter.format_transcript(transcript)
    data = json.loads(json_formatted)

    data_list = data[0]
    
    texts = [item['text'] for item in data_list[video_id] if 'text' in item]

    for text in texts:
        texto += text + " "
    data = {
        'Transcript': texto
    }
    return jsonify(data)