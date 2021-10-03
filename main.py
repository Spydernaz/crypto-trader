# import libraries
import os, random
import pandas as pd
import numpy as np
import cryptodata as cd
from sklearn import preporocessing
from collections import deque

# starting constants
SEQ_LEN = 20
FUTURE_PERIOD_PREDICT = 3
COIN_TO_PREDICT = "dot"


coinlist = list(cd.coindata.keys())
main_df = pd.DataFrame()


def classify(current, future):
    if float(future) > float(current):
        return 1
    else:
        return 0

def preprocess_df(df):
    df = df.drop('future', 1)
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
    
main_df['future'] = main_df[f"{COIN_TO_PREDICT}_close"].shift(-FUTURE_PERIOD_PREDICT)
main_df["target"] = list(map(classify, main_df[f"{COIN_TO_PREDICT}_close"], main_df["future"] ))




# print(main_df[[f"{COIN_TO_PREDICT}_close","future", "target"]].head(10))


times = sorted(main_df.index.values)

last_5percent = times[-int(0.05*len(times))]

validation_main_df = main_df[(main_df.index >= last_5percent)]
main_df = main_df[(main_df.index < last_5percent)]

train_x, train_y = preproccess_df(main_df)
validate_x, validate_y = preprocess_df(validation_main_df)