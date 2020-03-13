import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, jsonify, render_template
from werkzeug.utils import secure_filename
from predictions import predictAudio, featuresFFT
import glob

UPLOAD_FOLDER = '../outputs/audioMix'
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def inicio():
    return render_template("index.html")

@app.route('/upload')
def upload():
    return render_template("upload.html")

@app.route('/speakers', methods=['GET','POST'])
def olakase():
    path = f"../outputs/audioMix/{request.files['file'].filename}"
    X, speech = featuresFFT(path)
    allNames, speakers_names, speech = predictAudio(X, speech)
    
    subtitles = tuple(zip(allNames, speech))
    print(subtitles)

    resum = speakers_names
    print("speakers_names: ",speakers_names)

    print(request.files)
    return render_template('result.html', data=subtitles)

app.run('0.0.0.0', port=5000, debug=False, threaded=False)