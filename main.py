# import libraries
import os, random, time
import pandas as pd
import numpy as np
import deeperData as cd
from sklearn import preprocessing
from collections import deque

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, BatchNormalization
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint

# starting constants
SEQ_LEN = 90
FUTURE_PERIOD_PREDICT = 5
COIN_TO_PREDICT = "poly"
EPOCHS = 10
BATCH_SIZE = 64
NAME = f"{SEQ_LEN}-SEQ-{FUTURE_PERIOD_PREDICT}-PRED-{COIN_TO_PREDICT}-{int(time.time())}"

coinlist = list(cd.coindata.keys())
main_df = pd.DataFrame()


def classify(current, future):
    if float(future) > float(current):
        return 1
    else:
        return 0

def preprocess_df(df):
    df = df.drop('future', 1)
    df.dropna(how="any",inplace=True)

    for col in df.columns:
        if col != "target":
            df[col] = df[col].pct_change()
            df.dropna(inplace=True)
            df[col] = preprocessing.scale(df[col].values)
    df.dropna(inplace=True)
    
    sequential_data = []
    prev_days = deque(maxlen=SEQ_LEN)
    for i in df.values:
        prev_days.append([n for n in i[:-1]])
        if len(prev_days) == SEQ_LEN:
            sequential_data.append([np.array(prev_days),i[-1]])
    random.shuffle(sequential_data)

    buys = []
    sells = []

    for seq, target in sequential_data:
        if target == 0:
            sells.append([seq,target])
        elif target == 1:
            buys.append([seq,target])

    random.shuffle(buys)
    random.shuffle(sells)
    lower = min(len(buys),len(sells))

    buys = buys[:lower]
    sells = sells[:lower]

    sequential_data = buys+sells

    random.shuffle(sequential_data)

    x = []
    y = []

    for seq, target in sequential_data:
        x.append(seq)
        y.append(target)

    return (np.array(x),y)


for c in coinlist:
    # print(f"\n---------- {c} ----------\n")
    df = pd.DataFrame(cd.coindata[c])
    df.rename(columns={"close":f"{c}_close","volume":f"{c}_volume",}, inplace=True)
    df.set_index("period", inplace=True)
    df = df[[f"{c}_close",f"{c}_volume"]]

    if len(main_df) == 0:
        main_df = df
    else:
        main_df = main_df.join(df)

for col in main_df.columns:
    main_df[col] = pd.to_numeric(main_df[col])

main_df.fillna(method="ffill", inplace=True)  # if there are gaps in data, use previously known values
main_df.dropna(inplace=True)

main_df["future"] = main_df[f"{COIN_TO_PREDICT}_close"].shift(-FUTURE_PERIOD_PREDICT)
main_df["target"] = list(map(classify, main_df[f"{COIN_TO_PREDICT}_close"], main_df["future"] ))
# print(main_df[[f"{COIN_TO_PREDICT}_close","future", "target"]].tail(10))
# print(main_df.dtypes)



times = sorted(main_df.index.values)

last_5percent = times[-int(0.05*len(times))]

# validation_main_df = main_df[(main_df.index >= last_5percent)]
# main_df = main_df[(main_df.index < last_5percent)]


train_x, train_y = preprocess_df(main_df)

FivePercentIndex = int(-(len(train_x)*0.05))

# print(f"\n\n{FivePercentIndex}\n\n")

validate_x = train_x[FivePercentIndex:]
train_x = train_x[:FivePercentIndex]
validate_y = train_y[FivePercentIndex:]
train_y = train_y[:FivePercentIndex]

print(f"\n\n---------------\nData Counts\n---------------")
print(f"train data: {len(train_x)} validation: {len(validate_x)}")
print(f"Dont buy: {train_y.count(0)}, buys: {train_y.count(1)}")
print(f"VALIDATION Dont buy: {validate_y.count(0)}, buys: {validate_y.count(1)}")
print(f"\n\n")



# Build the model

model = Sequential()
model.add(LSTM(128,input_shape=(train_x.shape[1:]), return_sequences=True))
model.add(Dropout(0.2))
model.add(BatchNormalization())

model.add(LSTM(128,input_shape=(train_x.shape[1:]), return_sequences=True))
model.add(Dropout(0.2))
model.add(BatchNormalization())

model.add(LSTM(128,input_shape=(train_x.shape[1:])))
model.add(Dropout(0.2))
model.add(BatchNormalization()) 

model.add(Dense(32, activation="relu"))
model.add(Dropout(0.2))

model.add(Dense(2, activation="softmax" ))

opt = tf.keras.optimizers.Adam(lr=0.001, decay=1e-6)

model.compile(loss='sparse_categorical_crossentropy', optimizer=opt, metrics=["accuracy"])

tensorboard = TensorBoard(log_dir=f"/tmp/logs/{NAME}")
filepath = "RNN_Final-{epoch:02d}-{val_accuracy:.3f}"  # unique file name that will include the epoch and the validation acc for that epoch
checkpoint = ModelCheckpoint("models/{}.model".format(filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')) # saves only the best ones

train_x = np.asarray(train_x)
train_y = np.asarray(train_y)
validate_x = np.asarray(validate_x)
validate_y = np.asarray(validate_y)

history = model.fit(
    train_x, train_y,
    batch_size=BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=(validate_x, validate_y),
    callbacks=[tensorboard,checkpoint]
)

