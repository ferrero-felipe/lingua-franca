import warnings
import os
from functions import featureExtraction
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import Adam
from keras.utils import np_utils
from sklearn import metrics 
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def main():
    warnings.filterwarnings('ignore')
    if not os.path.exists('../data/database/sound_db.pkl'):
        print('Database not found. Creating one...')
        featureExtraction()
    print('Reading Database...')
    df = pd.read_pickle('../data/database/sound_db.pkl')

    print('Preparing Database...')
    df_t, df_val = train_test_split(df, test_size=0.2, random_state=42)
    X = np.array(df_t['feature_vector'].tolist())
    y = np.array(df_t['lang'].tolist())
    val_x = np.array(df_val['feature_vector'].tolist())
    val_y = np.array(df_val['lang'].tolist())
    lb = LabelEncoder()
    y = np_utils.to_categorical(lb.fit_transform(y))
    val_y = np_utils.to_categorical(lb.fit_transform(val_y))

    num_labels = y.shape[1]
    filter_size = 2

    # build model
    print('Building Neural Network...')
    model = Sequential()

    model.add(Dense(512, input_shape=(540,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(num_labels))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

    print('Training Model... It might take a while.')
    model.fit(X, y, batch_size=32, epochs=500, validation_data=(val_x, val_y))
    print('Done!')
    
    if not os.path.exists("../data/model"):
        os.makedirs("../data/model")
    model.save('../data/model/lang_classifier_model.h5')
    print('Model Saved!')

if __name__ == "__main__":
    main()