import warnings
warnings.filterwarnings('ignore')
import os
import librosa
import pandas as pd
import numpy as np
from scipy.fftpack import fft

def getFiles(directory,typ='.mp3'):
    """Generates paths to typ files in directory, default mp3"""
    for file in os.listdir(directory):
        if file.endswith(typ):
            yield('{}/{}'.format(directory,file))
        else:
            continue

def splitFile(audio,len_miliseconds=5000):
    """Generates audio chunks of given len, default 5000 ms"""
    for i in range(len(audio)//len_miliseconds):
        chunks = audio[i*len_miliseconds:(i+1)*len_miliseconds]
        yield chunks,i

def getAudio(file):
    """Loads given audio file"""
    data, sampling_rate = librosa.load(file, sr=None ,res_type='kaiser_fast')
    return data, sampling_rate

def getMFCC(row):
    """Gets MFCC for audio data on given row"""
    mfccs = np.mean(librosa.feature.mfcc(y=row['data'], sr=row['sample_rate'], n_mfcc=40).T,axis=0) 
    return mfccs

def getFFT(data,n=500):
    """Gets FFT for given data"""
    feature = fft(data,n)
    return feature

def getFeatureVector(row):
    """Combines MFCC and FFT into single feature vector"""
    vector = np.concatenate([row['mfcc'],row['fft']]) 
    return vector

def featureExtraction(directory='../data/samples'):
    df = pd.DataFrame(columns=['lang','data','sample_rate'])
    for lang in os.listdir(directory):
        print('Extracting features for files in {}'.format(lang))
        for file in getFiles('{}/{}'.format(directory,lang)):
            data, sample_rate = getAudio(file)
            df = df.append({'data':data,'lang':lang,'sample_rate':sample_rate}, ignore_index=True)
    df['mfcc'] = df[['data','sample_rate']].apply(getMFCC,axis=1)
    df['fft'] = df['data'].apply(lambda x: getFFT(x))
    df['feature_vector'] = df[['mfcc','fft']].apply(getFeatureVector,axis=1)
    if not os.path.exists("../data/database"):
                    os.makedirs("../data/database")
    print('Saving database...')
    df.to_pickle('../data/database/sound_db.pkl')
    print('Done!')

def getMax(values):
    for i in range(4):
        if values[i] == max(values):
            values[i] = 1
        else:
            values[i] = 0
    return values

