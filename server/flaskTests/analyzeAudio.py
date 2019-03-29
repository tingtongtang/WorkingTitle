from flaskTests.decorator import crossdomain
import base64
import requests
from flask import (
    Blueprint, request
)
import speech_recognition as sr
r = sr.Recognizer()

bp = Blueprint('analyzeAudio', __name__, url_prefix='/analyzeAudio')

def getTempo(file): 
    """ given a file, retrieves the tempo of the file from the sonicapi endpoint """ 
    files = {'input_file': open(file,'rb')}
    payload = {
        'access_id' : 'fcd97d07-bb10-439c-9f65-5f15f3b237dd', 
        'blocking': 'true', 
        'format': 'json'
    }
    resp = requests.post("https://api.sonicapi.com/analyze/tempo", data=payload, files=files)
    return resp.json()

@bp.route('/', methods=['GET', 'POST', 'OPTIONS'])
@crossdomain(origin='*')
def analyzeAudio():
    with open('audio.wav', 'wb') as infile:
         infile.write(request.data)
    tempoJson = getTempo('audio.wav')
    src = sr.AudioFile('audio.wav')
    with src as source:
        audio = r.record(source)
        print(type(audio))
        try:
            text = r.recognize_google(audio)
            print("you said :{} ".format(text))
        except:
            print("didnt recognize")
    return('This is the analyze')

