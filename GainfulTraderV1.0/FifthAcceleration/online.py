import random
from keras.models import load_model
from keras.callbacks import Callback
from keras import regularizers
from keras.regularizers import l1, l2, l1_l2
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
import numpy as np
import oandapy as ond
from datetime import timedelta, datetime
import pandas as pd
import time



def Insert_row(row_number, df, row_value):
    # Starting value of upper half
    start_upper = 0

    # End value of upper half
    end_upper = row_number

    # Start value of lower half
    start_lower = row_number

    # End value of lower half
    end_lower = df.shape[0]

    # Create a list of upper_half index
    upper_half = [*range(start_upper, end_upper, 1)]

    # Create a list of lower_half index
    lower_half = [*range(start_lower, end_lower, 1)]

    # Increment the value of lower half by 1
    lower_half = [x.__add__(1) for x in lower_half]

    # Combine the two lists
    index_ = upper_half + lower_half

    # Update the index of the dataframe
    df.index = index_

    # Insert a row at the end
    df.loc[row_number] = row_value

    # Sort the index labels
    df = df.sort_index()

    # return the dataframe
    return df

def collect(today='2017-01-30'):

    print('ond import successfull')
    timeframe = "M5"
    it = datetime.strftime(datetime.strptime(today, "%Y-%m-%d") - timedelta(days=2), "%Y-%m-%d")
    finish = datetime.strftime(datetime.strptime(today, "%Y-%m-%d") + timedelta(days=1), "%Y-%m-%d")
    print(it,finish)
    oanda = ond.API(environment='practice',
                    access_token='ce5f70d5af3563435fa23311d05314ea-98f884f4751f25ff622cfa2debfbb01e')
    data = oanda.get_history(instrument='EUR_GBP',  # our instrument
                                 start=it,  # start data
                                 end=finish,  # end date
                                 granularity=timeframe)  # minute bars  # 71
    df = pd.DataFrame(data['candles'])
            # print(pd.DataFrame(data['candles']))
    df['Date'] = pd.to_datetime(df.time)
    df.sort_values(by=['Date'])
    df['close'] = (df['closeBid'] + df['closeAsk']) / 2
    #print(df)
    print('collect() done')
    df['pct'] = df['close'].pct_change()
    return(df)

def parseWindowSet(df):

    m=len(df)
    window=10
    a = df['pct'][m:m - window-1:-1].values
    a = np.array(a) / np.max(np.fabs(a))
    aa = df['close'][m:m - window-1:-1].values
    aa = (np.array(aa) - np.mean(aa)) / np.std(aa)
    aaa = df['volume'][m:m - window-1:-1].values
    aaa = np.array(aaa) / np.max(np.fabs(aaa))
    a = np.concatenate((a, aaa))
    a = np.concatenate((a, aa))
    data = np.empty((0, window * 3), float)
    data = np.append(data, [a], axis=0)
    return data

def loadModels():
    modelCall = load_model('callModel.h5')
    modelPut = load_model('putModel.h5')
    print("models loaded")
    return modelCall, modelPut


def do(modelCall,modelPut):
    print("start ", datetime.now())
    df = collect(today=(datetime.strftime(datetime.today(), "%Y-%m-%d")))
    # print(df)


    window = parseWindowSet(df)
    print("windowset parsed ", datetime.now())
    #modelCall = load_model('callModel.h5')
    #modelPut = load_model('putModel.h5')
    # print(window)
    time.sleep(0.1)
    de = df['close'][len(df) - 1] - df['close'][len(df) - 2]
    callP = modelCall.predict(window[0:1])[0]
    putP = modelPut.predict(window[0:1])[0]

    call = callP[0] > 0.53

    put = putP[0] > 0.53

    priznC = -0.0002
    priznP = 0.0002

    ou = "trend: "
    if call and de < priznC:
        tr= "call"
        value=str(callP[0])
    elif put and de > priznP:
        tr= "put"
        value = str(putP[0])
    else:
        tr= "hold"
        value="-1"

    #---------test
    if (random.random()>0.5):
        tr="put"
    else:
        tr="hold"
    value="test"
    #---------test

    ou+=tr
    ou += "\nprice: " + str(df['close'].values[len(df) - 1])
    iTraderOut="position: "+tr+"\nid: id"+str(int(time.time()))+"\nvalue: "+value
    print("prediction done!")
    #f = open('event.ac', 'w')
    #f.write(ou)
    #f.close()
    f = open('../iTrader/iTrader.ac', 'w')
    f.write(iTraderOut)
    f.close()
    print('../iTrader/iTrader.ac was writеen:\n'+iTraderOut)
    return tr

