# from youtube_transcript_api import YouTubeTranscriptApi
# from youtube_transcript_api.formatters import JSONFormatter
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
    texto = ""
    try:
        # transcript = YouTubeTranscriptApi.get_transcripts([video_id], languages=["pt"])
        
        #fazer um request no link do youtube
        # Defina os headers
        headers = {
            'Accept-Language': 'pt-BR',
            'Content-Type': 'application/json',
            'User-Agent': 'Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59'
        }
        
        # Construa a URL do vídeo
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        # Faz a requisição GET
        response = requests.get(video_url, headers=headers)
            
        # Verifica se a resposta foi bem-sucedida (status code 200)
        if response.status_code == 200:
            # Retorna o conteúdo HTML da página
            video_page_body = response.text
            splittedHTML = video_page_body.split('"captions":')

            if len(splittedHTML) < 1:
                if not 'class="g-recaptcha"' in splittedHTML:
                    data = {
                        'Mensagem': 'Erro transcription nao encontrado',
                    }
                    return jsonify(data), 500
                data = {
                    'Mensagem': 'Erro videoId invalido'
                }
                return jsonify(data), 500
            
            try:
                caption = json.loads(splittedHTML[1].split(',"videoDetails')[0].replace('\n', ''))
            except json.JSONDecodeError:
                return jsonify({'Mensagem': 'Erro ao processar o JSON'}), 500

            if 'captionTracks' not in caption['playerCaptionsTracklistRenderer']:
                data = {
                    'Mensagem': 'Erro captionTracks nao encontrado'
                }
                return jsonify(data), 500
            
            # caption = caption['playerCaptionsTracklistRenderer']['captionTracks'][0]['baseUrl']

            # response_captions = requests.get(caption, headers=headers)
            # if response_captions.status_code == 200:
            #     # Retorna o conteúdo HTML da página
            #     transcript = response_captions.text
            #     # for text in transcript:
            #     #     texto += {
            #     #         'text': text[3],
            #     #         'duration': text[2],
            #     #         'offset': text[1]
            #     #     }
            #     data = {
            #         'Transcript': transcript
            #     }
            #     return jsonify(data)
            # else:
                # data = {
                #     'Mensagem': 'Erro ao buscar o transcript'
                # }
                # return jsonify(data), 500
            data = {
                'Transcript': splittedHTML,
                'status_code': len(splittedHTML)
            }
            return jsonify(data)
        else:
            data = {
                'Mensagem': 'Erro ao buscar o transcript'
            }
            return jsonify(data), 500
    except:
        data = {
            'Mensagem': 'Erro ao buscar o transcript'
        }
        return jsonify(data), 500

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
