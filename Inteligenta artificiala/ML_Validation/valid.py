import numpy as np
from PIL import Image
from keras.utils import to_categorical
from tensorflow.python.keras.utils.np_utils import normalize
"""
    Convolutional Neural Network
"""

from sklearn import preprocessing



train_foto = {}
train_labels = []
test_foto = {}

with open("train.txt","r") as cin:
    fotgrafii = cin.readlines()
    for foto in fotgrafii:
        foto = foto.replace("\n", "")
        foto = foto.split(",")
        try:
            train_foto[foto[0]] = np.asarray(Image.open("train/" + foto[0]))
            train_labels.append(int(foto[1]))
        except:
            pass

test_labels = []
with open("validation.txt","r") as cin:
    fotgrafii = cin.readlines()
    for foto in fotgrafii:
        foto = foto.replace("\n", "")
        foto = foto.split(",")
        try:
            #train_foto[foto[0]] = np.asarray(Image.open("validation/" + foto[0]))
            test_foto[foto[0]] = np.asarray(Image.open("validation/" + foto[0]))
            #train_labels.append(int(foto[1]))
            test_labels.append(int(foto[1]))
        except:
            pass

names = list(test_foto.keys())
train_foto = np.array(list(train_foto.values()))
train_labels = np.array(train_labels)
test_foto = np.array(list(test_foto.values()))
test_labels = np.array(test_labels)

test_foto1 = {}
with open("test.txt","r") as cin:
    fotgrafii = cin.readlines()
    for foto in fotgrafii:
        foto = foto.replace("\n", "")
        try:
            test_foto1[foto] = np.asarray(Image.open("test/" + foto))
        except:
            pass

names1 = list(test_foto1.keys())
test_foto1 = np.array(list(test_foto1.values()))

i = 0

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
import tensorflow.keras as keras
from tensorflow.keras import Input

train_foto = keras.utils.normalize(train_foto)
test_foto1 = keras.utils.normalize(test_foto1)
test_foto = keras.utils.normalize(test_foto)
train_foto = np.reshape(train_foto, (15000,50,50,1))
test_foto = np.reshape(test_foto, (4500,50,50,1))
test_foto1 = np.reshape(test_foto1, (3900,50,50,1))
ml = Sequential()
ml.add(Input(shape = (50,50,1), batch_size=10))
ml.add(Conv2D(16,(3,3)))
ml.add(AveragePooling2D(pool_size=(3,3)))
ml.add(Conv2D(16,(5,5)))
ml.add(MaxPool2D(pool_size=(2,2)))
ml.add(Flatten())
ml.add(Dense(32,activation="relu"))
ml.add(Dropout(0.3))
ml.add(Dense(32,activation="relu"))
ml.add(Dense(3, activation='softmax'))
ml.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


ml.fit( 
        train_foto,
        keras.utils.to_categorical(train_labels,3),
        epochs = 50,
        batch_size = 10
    )

predictions = ml.predict(test_foto)
 

nr = 0
for i in range(4500):
    if np.argmax(predictions[i]) == test_labels[i]:
        nr += 1
print(nr/4500)

predictions = ml.predict(test_foto1)

with open("prediction.txt","w+") as cout:
    cout.write("id,label\n")
    for data in range(3900):
        
        cout.write(f"{names1[data]},{np.argmax(predictions[data])}\n")
