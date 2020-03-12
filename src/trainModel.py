from keras import layers
from keras import models
from keras.layers.normalization import BatchNormalization
from keras.models import model_from_json
from sklearn import preprocessing
import json
import pandas as pd
from featuresExtract import dataTrainTest
import sys

num = sys.argv[1]
print(num)

def trainModel(num):
    print("iniciando trainModel...")
    print(num)
    
    X_train, y_train, X_test, y_test, df = dataTrainTest(num)

    number_classes = len(df.label_num.unique())

    inshape=(X_train.shape[1],)
        
    model = models.Sequential()
    model.add(layers.Dense(512, activation='relu', input_shape=inshape))
    model.add(layers.Dense(256, activation='relu'))

    model.add(BatchNormalization())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(number_classes,activation='softmax'))
    model.compile(optimizer='adam',
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy', 'mse'])
    print("Model compiled")
    model.fit(X_train,
                y_train,
                epochs=22,
                batch_size=50,
                validation_data=(X_test, y_test))


    results = model.evaluate(X_test, y_test)
    print("\n")
    print("Resultados: ",results)
    print("\n")

    predictions = model.predict(X_test)
    print("Predicción: ", predictions)

    print("\nModelo: ", model,"\n")
    name='../models/22epochs_15seg'

    model_json = model.to_json()
    with open(name+'.json', "w") as json_file:
        json.dump(model_json, json_file)

    model.save_weights(name+'.h5')
    print(f"Modelo {name}.h5 guardado")

    return predictions, y_test

def resultsPredict (predictions, y_test):
    print("Iniciando resultPredict...")
    df_predict = pd.DataFrame()
    df_predict['y_test'] = y_test
    df_predict['y_predict'] = [list(e) for e in predictions]
    df_predict['label_predict'] = df_predict['y_predict'].apply(lambda x: x.index(max(x)))
    df_predict['diff'] = (df_predict.y_test == df_predict.label_predict)
    print("Validación predicciones: \n", df_predict[['y_test', 'label_predict', 'diff']])

    print('Conteo de aciertos: ',df_predict['diff'].value_counts())


pred, yTest = trainModel(num)

resultsPredict(pred, yTest)


