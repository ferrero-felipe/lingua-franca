from keras.models import load_model
from functions import getMax, getMFCC, getFFT, getFeatureVector, getAudio
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import librosa.display

model = load_model('../data/model/my_model.h5')
lang_list = ['es_es', 'fr', 'pt_br', 'sv']
languages = {'pt_br':'Brazilian Portuguese', 'es_es':'Spanish', 'sv':'Swedish', 'fr':'French'}

def prepare(file='../data/test.ogg'):
    test = pd.DataFrame(columns=['data','sample_rate'])
    data, sample_rate = getAudio(file)
    test = test.append({'data':data,'sample_rate':sample_rate}, ignore_index=True)
    test['mfcc'] = test[['data','sample_rate']].apply(getMFCC,axis=1)
    test['fft'] = test['data'].apply(lambda x: getFFT(x))
    test['feature_vector'] = test[['mfcc','fft']].apply(getFeatureVector,axis=1)
    test.to_pickle('../data/test.pkl')

def identify(file='../data/test.pkl'):
    prepare()
    test = pd.read_pickle(file)
    X_test = np.array(test['feature_vector'].tolist())
    test_y = model.predict(X_test)
    print(test_y)
    bin_y = getMax(test_y[0])
    print(bin_y)
    lang = np.where(bin_y == 1)[0][0]
    print(lang)
    print(languages[lang_list[lang]])
    return languages[lang_list[lang]]

def createGraph(file='../data/test.ogg'):
    data, sample_rate = getAudio(file)
    plt.figure(figsize=(8, 5))
    librosa.display.waveplot(data, sr=sample_rate)
    plt.savefig('graph.png')