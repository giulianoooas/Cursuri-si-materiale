import numpy as np
from PIL import Image
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

train_foto = np.array(list(train_foto.values()))
train_labels = np.array(train_labels)
train_foto = np.reshape(train_foto, (15000,2500))
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
test_foto = np.array(list(test_foto.values()))
test_foto = np.reshape(test_foto, (4500,2500))

class KnnClasifier:

    def __init__(self,train_data, train_labels):
        self.train_data = train_data
        self.train_labels = train_labels
    
    def predict(self,data, k = 3):
        arr = (self.train_data - data)**2
        arr = np.sqrt(arr.sum(axis = 1))
        indicii = arr.argsort()
        index = indicii[:k]
        return self.train_labels[index[index.argmax()]]


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


#train_foto,test_foto = normalize_data(train_foto, test_foto,"l1")

knn = knn = KnnClasifier(train_foto, train_labels)
i = 0

with open("prediction.txt","w+") as cout:
    cout.write("id,label\n")
    for data in test_foto:
        
        cout.write(f"{names[i]},{knn.predict(data,5)}\n")
        i += 1