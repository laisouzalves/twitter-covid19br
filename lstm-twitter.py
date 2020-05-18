print("Importing base library...")
import import pandas as pd
import numpy as np
import seaborn as sns
import re
from collections import Counter
from cleantts.py import *
import random

print("Importing keras and sklearn modules...")
from keras.preprocessing import sequence,text
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Dense,Dropout,Embedding,LSTM,Conv1D,GlobalMaxPooling1D,Flatten,MaxPooling1D,GRU,SpatialDropout1D,Bidirectional
from keras.callbacks import EarlyStopping
from keras.utils import to_categorical
from keras.losses import categorical_crossentropy
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, average_precision_score, f1_score, confusion_matrix, recall_score, precision_score
from sklearn.utils import resample

from tensorflow import set_random_seed

seed = 42
random.seed(seed)
np.random.seed(seed)
set_random_seed(seed)

### LOADING DATA ###
print("Loading data...")
data = pd.read_csv('twitter_data.csv')
mask = data['sentiment'].isin([1, 2, 3]) # Seleciona os dados que estão tabulados corretamente
new_data = data[mask]
sentiments = new_data['sentiment']
texts = new_data['original_text']

# Indexando os sentimentos em zero:
labels = np.array([(int(sentiments[i])-1) for i in range(1,len(sentiments))])

### CLEANING TWEETS ###
sentiments = sentiments.to_list()
texts_list = texts.to_list()
clean_texts = clean_tts(texts_list)

### COUNTING WORDS ###
all_text = []
for idx, item in enumerate(clean_texts):
    string = item
    for idx, item in enumerate(string.split(' ')):
        all_text.append(item)

counts = Counter(all_text)
vocabulary = sorted(counts, key=counts.get, reverse=True)

df = pd.concat([labels, clean_texts],  axis = 1) # Cria o dataframe que vamos utilizar no treino
df.rename(columns = {'labels' : 'sentiment', 'clean_text' : 'tweet'}, inplace = True)
total_twittes = df.shape[0]

### PRINTS RELEVANT STATISTICS ###
print("O total de twittes é de {}.".format(total_twittes))
print("Total de palavras em todos os tweets: {}".format(len(all_text)))
print("Total de palavras no vocabulario: {}".format(len(vocabulary)))


### SELECIONANDO OS DADOS DE TREINAMENTO E AS LABELS ###
x = df['tweet']
y = df['sentiment']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state = seed, shuffle=True)

### RESAMPLING DATA ###
X = pd.concat([x_train, y_train], axis=1)
X.head()

category0 = X[X.sentiment==0]
category1 = X[X.sentiment==1]
category2 = X[X.sentiment==2]

number=len(category1)

category0_upsampled = resample(category0, replace=True, n_samples=number, random_state=seed)
category1_upsampled = resample(category1, replace=True, n_samples=number, random_state=seed)
category2_upsampled = resample(category2, replace=True, n_samples=number, random_state=seed)

resampled_data = pd.concat([category0_upsampled, category1_upsampled, category2_upsampled])

### TOKENIZING TWEETS ###
tam_vocab = len(vocabulary)

tokenizer = Tokenizer(num_words=tam_vocab)
tokenizer.fit_on_texts(list(x_train))
tokenizer.fit_on_texts(list(x_test))

X_train = tokenizer.texts_to_sequences(x_train)
X_test = tokenizer.texts_to_sequences(x_test)
X_train = pad_sequences(X_train, maxlen=22)
X_test = pad_sequences(X_test, maxlen=22)

Y_train = to_categorical(y_train.values)

### SEPARATING TRAIN DATA INTO TRAIN SET AND VALIDATION SET ###
train_x, val_x, train_y, val_y = train_test_split(X_train, Y_train, test_size=0.3)

### DEFINING NEURAL NET ###
max_features = len(vocabulary)

model=Sequential()
model.add(Embedding(max_features,512,mask_zero=True))
model.add(LSTM(256,dropout=0.4, recurrent_dropout=0.4,return_sequences=True))
model.add(LSTM(512,dropout=0.5, recurrent_dropout=0.5,return_sequences=False))
model.add(Dense(3,activation='softmax'))
model.compile(loss='categorical_crossentropy',optimizer=Adam(lr=0.001),metrics=['accuracy'])
model.summary()

### TRAINING PHASE ###
epochs = 50
batch_size = 128

model.fit(train_x, train_y, validation_data=(val_x, val_y), epochs=epochs, batch_size=batch_size, verbose=1)

### RESULTS ###
predictions = model.predict_classes(X_test, batch_size=batch_size, verbose=1)
pd.DataFrame(confusion_matrix(y_test, predictions))

acc_score = accuracy_score(y_test, predictions)
print("Accuracy = {:.2f} %".format(acc_score*100))
f1 = f1_score(y_test, predictions, average=None)
print("F1 Score: ", f1)
