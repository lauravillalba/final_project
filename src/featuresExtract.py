import glob
import pandas as pd
from pydub import AudioSegment
import numpy as np
from scipy.fftpack import fft
import json
import librosa
import librosa.display

def fileList():
    return glob.glob("../outputs/selection/**.mp3")

def featuresFourier(x):
    return np.abs(fft((AudioSegment.from_file(x, format='mp3')).get_array_of_samples()))

def dataGenerator():
    print("Iniciando dataGenerator...")
    filelist = fileList()

    df = pd.DataFrame(filelist).rename(columns={0:'path'})
    df['file'] = df.path.apply(lambda x: (x.split("/")[3]))
    df['label'] = df.file.apply(lambda x: (x.split("_")[0]))
    df['audio_num'] = df.file.apply(lambda x: (x.split("_")[1].split(".")[0]))
    df['fft'] = df.path.apply(lambda x: featuresFourier(x))


    df.sort_values(by=('audio_num'),inplace = True)
    names = list(df.label.unique())
    print(f"Existen un total de {len(names)} personas identificadas: {names}")

    name = {}
    for i, n in enumerate(names):
        name[n] = i    
    df['label_num']=df.label.apply(lambda x: name[str(x)])
    
    with open('../outputs/names_id.json', 'w') as fp:
        json.dump(name, fp)
    
    print("La correspondencia entre nombre y etiquetas se guarda en: ../outputs/names_id.json" )

    print(df.head())

    return df

def dataTrainTest (num):
    print("Iniciando dataTrainTest...")
    print( "Num = ", num)
    df = dataGenerator()

    print("df.shape = ", df.shape)

    y = df['label_num'].to_numpy()
    X = np.vstack(df['fft'])

    train = int(df.shape[0]*int(num)/100)
    X_train = X[:train]
    y_train = y[:train]
    X_test = X[-train:]
    y_test = y[-train:]

    return X_train, y_train, X_test, y_test, df

#dataGenerator()