from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from flask import Flask, jsonify, request
import json
import requests

# para rodar o flask -> flask --app index.py run
# para subir para o vercel -> vercel --prod
# para criar o requirements -> pip freeze > requirements.txt

app = Flask(__name__)
aplication = app

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
        # transcript = YouTubeTranscriptApi.get_transcripts([video_id], languages=["pt"])
        
        #fazer um request no link do youtube
        data = get_youtube_video_page(video_id)
        return jsonify(data)
    except:
        data = {
            'Mensagem': 'Erro ao buscar o transcript'
        }
        return jsonify(data), 500
    
    # texto = ""

    # formatter = JSONFormatter()
    # json_formatted = formatter.format_transcript(transcript)
    # data = json.loads(json_formatted)

    # data_list = data[0]
    
    # texts = [item['text'] for item in data_list[video_id] if 'text' in item]

    # for text in texts:
    #     texto += text + " "
    # data = {
    #     'Transcript': texto
    # }
    # return jsonify(data)

def get_youtube_video_page(video_id):
    # Defina os headers
    headers = {
        'Accept-Language': 'pt-BR',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    # Construa a URL do vídeo
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        # Faz a requisição GET
        response = requests.get(video_url, headers=headers)
        
        # Verifica se a resposta foi bem-sucedida (status code 200)
        if response.status_code == 200:
            # Retorna o conteúdo HTML da página
            video_page_body = response.text
            return video_page_body
        else:
            print(f"Erro ao buscar a página do vídeo. Código de status: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao fazer a requisição: {str(e)}")
        return None