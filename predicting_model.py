from keras.models import Sequential
from keras.layers import LSTM, Embedding, Dense, Activation, Dropout
import pandas as pd
import numpy as np

data_set = pd.read_csv("dataset.csv", sep='\t')
train_y = data_set["R"][:15000]
test_y = data_set["R"][15000:]
train_x = data_set.drop(columns=["R"])[:15000]
#train_x = np.reshape(train_x, (train_x.shape[0], 10, train_x.shape[1]))
test_x = data_set.drop(columns=["R"])[15000:]

max_features = 500
model = Sequential()
model.add(Embedding(max_features, 7))
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(train_x, train_y, epochs=15, batch_size=50,  verbose=1)
print(model.evaluate(test_x, test_y))
