# Importing the necessary Libraries
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify,send_file,Response,make_response,url_for,send_from_directory
from flask_ngrok import run_with_ngrok
from inference import create_synthesizer,synthesize
import soundfile as sf
from saveText import save_text, find_path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_swagger_ui import get_swaggerui_blueprint
import io
import wave

app = Flask(__name__,static_url_path='',static_folder="static") #html 폴더 경로 설정
CORS(app)
app.config['JSON_AS_ASCII'] = False
app.config.from_pyfile('config.py')
database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
Session = sessionmaker(database)
session = Session()
#run_with_ngrok(app)



SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name':"SilliconWildCat"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/TTS', methods=['POST'])
def text_speech(): 
    if request.method=='POST':   
        data=request.get_json()
        speech=data['speech']
        speech=speech+'.'
        voices=data['voices']
        syn=create_synthesizer(voices)
        speech=speech+"."
        wavs=synthesize(speech,syn)
        sf.write('static/audio.wav',wavs,22050,subtype='PCM_16')

        '''
        w = wave.open('audio.wav','r')
        frame = w.getnframes()
        rate = w.getframerate()
        '''

        #out = io.BytesIO()
        #syn.save_wav(wavs, out)
        #save_text(speech,database,session)
        #return 'ok' 
        #response=send_file('/static/audio.wav', mimetype="audio/wav")
        src=url_for('static', filename='audio.wav')
        response=make_response(jsonify({"msg":"success","data":src}))
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

@app.route('/<path:filename>')
def wav_return():
    return app.send_static_file('audio.wav')

@app.route('/SVS', methods=['GET'])
def singing_voice():
    param_dict = request.args.to_dict()
    title = param_dict['title']
    file_path = find_path(title, session)
    return file_path


def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response
    
def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    app.run(port=80, debug=True)