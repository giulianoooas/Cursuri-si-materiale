import numpy as np
from PIL import Image
from keras.utils import to_categorical
from sklearn import preprocessing
"""
    Neural Network
    2 Hidden layers
"""

train_foto = {}
train_labels = []

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

train_foto = np.array(list(train_foto.values()))
train_labels = np.array(train_labels)
train_foto = np.reshape(train_foto, (15000,2500))


"""
    Initial amn salvat poza sub forma unui dictionar de forma 
        key = numele
        value = poza sub forma de np.array
    
    am 3 narray-uri:
        1) train_foto = pentru pozele de antrenare
        2) test_foto = pentru datele de test
"""

def normalize_data(train_data, test_data, type=None):
    if type is None:
        return (train_data, test_data)    
    elif type == "standard":
        scaler = preprocessing.StandardScaler()
        scaler.fit(train_data)
        scaled_train = scaler.transform(train_data)
        scaled_test = scaler.transform(test_data)
        return (scaled_train, scaled_test)   
    elif type == "l1":
        normalizer = preprocessing.Normalizer(norm='l1')
        normalizer.fit(train_data)
        normalized_test = normalizer.transform(train_data)
        normalized_train = normalizer.transform(train_data)
        return (normalized_train, normalized_test)    
    elif type == "l2":
        normalizer = preprocessing.Normalizer(norm='l2')
        normalizer.fit(train_data)
        normalized_test = normalizer.transform(train_data)
        normalized_train = normalizer.transform(train_data)
        return (normalized_train, normalized_test)

test_foto = {}
with open("validation.txt","r") as cin:
    fotgrafii = cin.readlines()
    for foto in fotgrafii:
        foto = foto.replace("\n", "")
        foto,label = foto.split(",")
        try:
            test_foto[foto] = np.asarray(Image.open("validation/" + foto))
        except:
            pass

names = list(test_foto.keys())
test_foto = np.array(list(test_foto.values()))
test_foto = np.reshape(test_foto, (4500,2500))

train_foto,test_foto = normalize_data(train_foto, test_foto,"l1")

train_Y_one_hot = to_categorical(train_labels)
i = 0


"""
    Am normalizat datele si dupa am reshape - uit array -urile sa fie de dimensiune 2500 in loc de 50x50
"""

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense,Dropout
import tensorflow.keras as keras
from tensorflow.keras import Input


inputs = Input(shape=(2500,))
x = Dense(64, activation="relu")(inputs)
p1 = Dropout(0.5)(x)
x3 = Dense(32, activation="relu")(p1)
outputs = Dense(3, activation="softmax")(x3)

"""
    Modelul meu este destul de simplu, are 2 hidden layers si intre ele un Dropout pentru a reduce riscul de overfit
"""


ml = Model(inputs = inputs, outputs = outputs)
ml.summary()
ml.compile(
    optimizer=keras.optimizers.Adam(),  # Optimizer
    # Loss function to minimize
    loss=keras.losses.SparseCategoricalCrossentropy(),
    # List of metrics to monitor
    metrics=[keras.metrics.SparseCategoricalAccuracy()],
)

"""
     Pentru optimizare am folosit adam.
    Adam calculeaza gradientul se bazează pe estimarea adaptativă a momentelor de ordinul întâi și de ordinul al doilea.

    Pentru functia de loss am folosit categorical_crossentropy, deoarece am 3 labeluri.

"""


ml.fit( train_foto,
        train_labels, 
        epochs = 200,
        batch_size = 64,
)

predictions = ml.predict(test_foto)


with open("prediction.txt","w+") as cout:
    cout.write("id,label\n")
    for data in range(4500):
        
        cout.write(f"{names[i]},{np.argmax(predictions[i])}\n")
        i += 1