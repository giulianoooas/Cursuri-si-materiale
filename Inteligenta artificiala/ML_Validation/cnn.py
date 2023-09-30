import numpy as np
from PIL import Image
from keras.utils import to_categorical
from numpy.core.fromnumeric import argmax
from tensorflow.python.keras.utils.np_utils import normalize
"""
    Convolutional Neural Network
"""

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

"""
    Initial amn salvat poza sub forma unui dictionar de forma 
        key = numele
        value = poza sub forma de np.array
    
    am 3 narray-uri:
        1) train_foto = pentru pozele de antrenare
        2) test_foto = pentru am testa local accuarancy
        3) test_foto1 = pentru pozele de test
"""


test_labels = []
with open("validation.txt","r") as cin:
    fotgrafii = cin.readlines()
    for foto in fotgrafii:
        foto = foto.replace("\n", "")
        foto,label = foto.split(",")
        try:
            test_foto[foto] = np.asarray(Image.open("validation/" + foto))
            test_labels.append(label)
        except:
            pass

names = list(test_foto.keys())
train_foto = np.array(list(train_foto.values()))
train_labels = np.array(train_labels)
test_foto = np.array(list(test_foto.values()))
test_labels = np.array(test_labels)




i = 0

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
import tensorflow.keras as keras
from tensorflow.keras import Input


train_foto = keras.utils.normalize(train_foto)
test_foto = keras.utils.normalize(test_foto)
train_foto = np.reshape(train_foto, (15000,50,50,1))
test_foto = np.reshape(test_foto, (4500,50,50,1))

"""
    Pentru a folosi cnn am facut rehape tuturor pozelor de from 
     (nr de poze, 50,50,   1) si cu ajutorul keras.utils.normalize 
     le-am normalizat
"""

ml = Sequential()
ml.add(Input(shape = (50,50,1), batch_size=1500))
ml.add(Conv2D(16,(3,3),activation="relu"))
ml.add(AveragePooling2D(pool_size=(3,3)))
ml.add(Conv2D(16,(3,3),activation = "relu"))
ml.add(MaxPool2D(pool_size=(3,3)))
ml.add(Flatten())
ml.add(Dense(32,activation="relu"))
ml.add(Dropout(0.3))
ml.add(Dense(32,activation="relu"))
ml.add(Dense(3, activation='softmax'))
ml.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


"""
    Modelulul meu:
        1) Prima data am un layer de tip Input pentru a imi spune care e este dim datelor de intrare si a batch-ului.
        2) Un layer ce mi face convulatia de 3x3, urmat de un layer ce-mi face media pe convulatii.
        3) Un layer de convulatie ce-mi extrage valoarea maxima.
        4) layer-ul Flatten pentru a-mi transforma totul intr-un narray de 1D
        5) reteaua mea neuronala bazata pe 2 layeruri asunse
    
    Pentru optimizare am folosit adam.
    Adam calculeaza gradientul se bazează pe estimarea adaptativă a momentelor de ordinul întâi și de ordinul al doilea.

    Pentru functia de loss am folosit categorical_crossentropy, deoarece am 3 labeluri.

"""

ml.fit( 
        train_foto,
        keras.utils.to_categorical(train_labels,3),
        epochs = 50,
        batch_size = 1500 # datele le-am antrenat pe 50 de pasi de antrenare de dimensiune 15
    )

predictions = ml.predict(test_foto)
 

i = 0

with open("prediction.txt","w+") as cout:
    cout.write("id,label\n")
    for data in test_foto:
        
        cout.write(f"{names[i]},{argmax(predictions[i])}\n")
        i += 1
