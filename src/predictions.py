from keras.models import load_model
from keras.models import model_from_json
import json
from pydub import AudioSegment
import pandas as pd
import numpy as np
from scipy.fftpack import fft
import glob
import sys
import librosa
import librosa.display

# audioFile = sys.argv[1] --> en caso de ejecutar este .py desde la terminal. Al ejecutar desde api.py pasar el parámetro contenido en la función featuresFFT.

def getAudio(audioFile):
    return AudioSegment.from_file(audioFile, format='mp3')

def featuresMFCC(x):
    SAMPLE_RATE = 22050
    #y, sr = librosa.load(x, sr=SAMPLE_RATE, duration = 20) # Chop audio at 5 secs... 
    mfcc = librosa.feature.mfcc(y=x, sr=SAMPLE_RATE, n_mfcc = 5) # 5 MFCC components
    return mfcc.tolist()

def featuresFFT(audioFile):
    print("Iniciando featuresFFT...")
    # Audios de 20' con overlab 50%:
    audio_original = getAudio(audioFile)
    print("Completado getAudio de ", audioFile)
    mfcc = []
    interval = 20000
    counter = 0
    num = (len(audio_original)//interval)*2

    for _ in list(range(num)):
        if counter == 0:
            splited = audio_original[0:interval]
            splited_arr = splited.get_array_of_samples()
            mfcc.append(featuresMFCC(splited_arr))
            counter+=int(interval/2)
            interval+=int(counter)
        else: 
            splited = audio_original[counter:interval]
            splited_arr = splited.get_array_of_samples()
            mfcc.append(featuresMFCC(splited_arr))
            counter+=10000
            interval+=10000

    print('FIN! Ya tenemos features para predecir')

    df= pd.DataFrame()
    df['mfcc'] = mfcc[:-1]
    X = np.vstack(df.mfcc)
    return X

def predictAudio(X):
    print("Iniciando predictAudio...")
    with open('../models/50epochs_mfcc.json','r') as f:
        model_json = json.load(f)

    model = model_from_json(model_json)
    model.load_weights('../models/50epochs_mfcc.h5')

    predictions = model.predict(X)
    df= pd.DataFrame()
    df['y_predict'] = [list(e) for e in predictions]
    df['label_predict'] = df['y_predict'].apply(lambda x: x.index(max(x)))
    
    #print('predictions: ', predictions)
    speakers_predict = df.label_predict.to_list()
    speakers = []
    
    for i, e in enumerate (speakers_predict):
        if i == 0:
            speakers.append(e)
        elif i< len(speakers_predict)-1 and speakers_predict[i]!= speakers_predict[i+1] and speakers_predict[i]!= speakers[-1]:
            speakers.append(e)
        elif i == len(speakers_predict)-1 and speakers_predict[i]!= speakers[-1]:
            speakers.append(e)
    
    with open('../outputs/names_id.json') as f:
        names = json.load(f)
    #print("Correspondecia nombres vs etiquetas: ", names)

    speakers_names = []
    for s in speakers:
        for n in names.items():
            if n[1]==s:
                speakers_names.append(n[0])

    print ('En el audio hablan las siguientes personas: ', set(speakers_names), '\nHablan en el siguiente orden: ', '-'.join(speakers_names))
    
    return '\n'.join(speakers_names)

#predictAudio(featuresFFT())
