import numpy as np
from PIL import Image

"""
     K-Nearest Neighbor - 0.49 rata 
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

train_foto = np.array(list(train_foto.values()))
train_labels = np.array(train_labels)
train_foto = np.reshape(train_foto, (15000,2500))

with open("test.txt","r") as cin:
    fotgrafii = cin.readlines()
    for foto in fotgrafii:
        foto = foto.replace("\n", "")
        try:
            test_foto[foto] = np.asarray(Image.open("test/" + foto))
        except:
            pass

names = list(test_foto.keys())
test_foto = np.array(list(test_foto.values()))
test_foto = np.reshape(test_foto, (3900,2500))


"""
    Initial amn salvat poza sub forma unui dictionar de forma 
        key = numele
        value = poza sub forma de np.array
    
    am 3 narray-uri:
        1) train_foto = pentru pozele de antrenare
        2) test_foto = pentru datele de test
"""

class KnnClasifier:
    """
        Clasa Knn clasifier este clasa ce-mi va calcua predictia pentru fiecare dintre datele de intrare.

        El va face asta in felul urmator:
            imi va calcula distanta sqrt((x1-y1)**2 + ... + (x2500 - y2500)**2) dintre fiecare din datele de intrare si imi va vedea care este cel
            mai apropiat vecin.

        Am pus ca dimensiune 2500, deoarece fiecare poza va primi un reshape pentru a deveni 2500 in loc de 50x50
    """
    def __init__(self,train_data, train_labels):
        self.train_data = train_data
        self.train_labels = train_labels
    
    def predict(self,data, k = 3):
        arr = (self.train_data - data)**2
        arr = np.sqrt(arr.sum(axis = 1))
        indicii = arr.argsort()
        index = indicii[:k]
        return self.train_labels[index[index.argmax()]]



knn = knn = KnnClasifier(train_foto, train_labels)
i = 0

with open("prediction.txt","w+") as cout:
    cout.write("id,label\n")
    for data in test_foto:
        
        cout.write(f"{names[i]},{knn.predict(data,5)}\n")
        i += 1