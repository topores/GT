import oandapy as ond
from datetime import timedelta, datetime
import pandas as pd

def collect(start='2018-01-30',end = '2019-10-15'):
    a = ond.API(environment='practice',
                access_token='ce5f70d5af3563435fa23311d05314ea-98f884f4751f25ff622cfa2debfbb01e')
    print(dir(a))
    print('ond import successfull')
    timeframe = "M5"
    dates = []
    it = datetime.strptime(start, "%Y-%m-%d")
    finish = datetime.strptime(end, "%Y-%m-%d")
    while it < finish:
        dates.append(datetime.strftime(it, "%Y-%m-%d"))
        it += timedelta(days=14)
    dates.append(datetime.strftime(finish, "%Y-%m-%d"))
    oanda = ond.API(environment='practice',
                    access_token='ce5f70d5af3563435fa23311d05314ea-98f884f4751f25ff622cfa2debfbb01e')
    for i in range(0, len(dates) - 1):
        print(dates[i], dates[i + 1])
        data = oanda.get_history(instrument='EUR_GBP',  # our instrument
                                 start=dates[i],  # start data
                                 end=dates[i + 1],  # end date
                                 granularity=timeframe)  # minute bars  # 7
        print('data=', pd.DataFrame(data['candles']))
        if i <= 0:
            df = pd.DataFrame(data['candles'])
        else:
            df = pd.concat([df, pd.DataFrame(data['candles'])], ignore_index=True)
            print(i)
            # print(pd.DataFrame(data['candles']))
    df['Date'] = pd.to_datetime(df.time)
    df.sort_values(by=['Date'])
    df['close'] = (df['closeBid'] + df['closeAsk']) / 2
    print(df)
    print('collect() done')
    return(df)

import numpy as np
def cut(df,mode):
    df['pct'] = df['close'].pct_change()
    window = 10
    wi = window * 3
    di = np.zeros((len(df)))
    train_data = np.empty((0, wi), float)
    res_data = np.empty((0, 2), float)

    for i in range(wi, len(df) - 1):
        if (i % 100 == 0):
            print('collecting data: ' + str(i / len(df) * 100) + '% done')

        if mode > 0:
            cutCond = ((df['close'].values[i] - df['close'].values[i - 1]) > mode)
        elif mode < 0:
            cutCond = ((df['close'].values[i] - df['close'].values[i - 1]) < mode)
        else:
            cutCond=False

        if cutCond:
            try:
                di[i] = len(train_data)
                a = df['pct'][i:i - window:-1].values
                a = np.array(a) / np.max(np.fabs(a))
                aa = df['close'][i:i - window:-1].values
                aa = (np.array(aa) - np.mean(aa)) / np.std(aa)
                aaa = df['volume'][i:i - window:-1].values
                aaa = np.array(aaa) / np.max(np.fabs(aaa))
                if (df['close'].values[i] - df['close'].values[i - 1] > 0.0000):
                    if (df['close'].values[i + 1] - df['close'].values[i] < 0):
                        R = [1, 0]
                    elif (df['close'].values[i + 1] - df['close'].values[i] > 0):
                        R = [0, 1]
                    else:
                        R = [0.5, 0.5]
                elif (df['close'].values[i] - df['close'].values[i - 1] < -0.0000):
                    if (df['close'].values[i + 1] - df['close'].values[i] > 0):
                        R = [1, 0]
                    elif (df['close'].values[i + 1] - df['close'].values[i] < 0):
                        R = [0, 1]
                    else:
                        R = [0.5, 0.5]
                a = np.concatenate((a, aaa))
                a = np.concatenate((a, aa))
                train_data = np.append(train_data, [a], axis=0)
                res_data = np.vstack((res_data, [R]))

            except Exception as e:
                a = np.ones((window))
                aa = np.ones((window))
                aaa = np.ones((window))
                R = [0.5, 0.5]
                print("exception caught: ", e)
                pass
    return train_data,res_data,di

from keras.optimizers import SGD, Adam
from keras.losses import categorical_crossentropy
from keras.layers import Dropout, LSTM, BatchNormalization, LeakyReLU, Activation
import random
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
from keras.callbacks import Callback
from keras import regularizers
from keras.regularizers import l1, l2, l1_l2
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
def initModel():
    Units = 256
    model = Sequential()
    # model.add(LSTM(units=256, return_sequences=True, input_shape=(1, wi)))#, activity_regularizer=l2(0.0025)))
    # model.add(LSTM(units=256, return_sequences=False, input_shape=(1, wi)))#, activity_regularizer=l2(0.0025)))
    model.add(Dense(units=256 * 2, activation='relu', kernel_initializer='glorot_uniform'))
    model.add(Dropout(0.35))
    model.add(Dense(units=256, activation='relu', kernel_initializer='glorot_uniform'))
    # model.add(Dense(units=108, activation='relu'))


    # model.add(LSTM(units=106, return_sequences=False, input_shape=(1, Units, 60)))
    model.add(Dropout(0.35))
    model.add(Dense(units=2, activation='sigmoid'))
    model.add(Activation('softmax'))
    print('model built')
    return model

import time
import os
def train(model,train_data,res_data,epoch=20):
    try:
        os.mkdir('bestModels')
    except:
        pass

    adam = Adam(lr=0.0000007)
    model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

    checkpointName = ''
    Checkpoint = ModelCheckpoint(
        'bestModels/' + checkpointName + 'best-' + str(round(time.time() / 100)) + '{val_acc:.4f}',
        monitor='val_acc',
        save_best_only=True,
        period=10)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.9, patience=5, min_lr=0.000001, verbose=1)
    results = model.fit(train_data, res_data, nb_epoch=epoch, verbose=2, validation_split=0.15, batch_size=16, shuffle=False,
                        callbacks=[Checkpoint, reduce_lr])
    return model,results

def analyzeTrain(results):
    if (results.history['val_acc'][0]>0.5 or results.history['acc'][0]>0.506):
        flag=False
    else:
        flag=True
    return flag

def saveModel(model,title=''):
    model.save(title+'Model.h5')


def showResults(results):
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    history = results

    plt.figure()
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='best')
    plt.show()

    plt.figure()
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('acc')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='best')
    plt.show()


def predict(model,data):
    return model.predict(data)[0]

def smartCut(model,df,train_data,mode=0.48,Dmode=True,value=0.0005):
    tp, tn, fp, fn = 1, 1, 1, 1
    k = 1
    av = mode
    w, l = 0, 0
    maxl = 0
    martw = [0, 0, 0, 0, 0, 0, 0]
    pips = 0

    martl = [0, 0, 0, 0, 0, 0, 0]
    from keras.models import load_model
    # model=load_model("/content/bestModels/best-156746970.5273")
    for i in range(round(len(df) * 0.85), round(len(df) * 1) - 1):
        # print(model.predict(train_data[i:i+1]))
        j = int(di[i])
        if not j == 0:
            callP = model.predict(train_data[j:j + 1])[0][0] > model.predict(train_data[j:j + 1])[0][1]
            putP = model.predict(train_data[j:j + 1])[0][0] < model.predict(train_data[j:j + 1])[0][1]
            callP = True
            putP = True
            sig = model.predict(train_data[j:j + 1])[0][0] > av  # 0.56
            # k+=1
            # av=(av*k+model.predict(train_data[j:j+1])[0][0])/(k+1)
            # sig=True
            # sig=True
            # print(model.predict(train_data[j:j+1]))

            if Dmode and sig and callP and (df['close'].values[i] - df['close'].values[i - 1]) < -value:
                if (df['close'].values[i + 1] - df['close'].values[i]) > 0:
                    tp += 1
                elif (df['close'].values[i + 1] - df['close'].values[i]) < 0:
                    fp += 1

            elif Dmode and sig and putP and (df['close'].values[i] - df['close'].values[i - 1]) > value:
                pips += -(df['close'].values[i + 1] - df['close'].values[i]) - 0.00005
                if (df['close'].values[i + 1] - df['close'].values[i]) < 0:
                    tn += 1
                    if l < 6:
                        martw[l] = martw[l] + 1
                    l = 0

                elif (df['close'].values[i + 1] - df['close'].values[i]) > 0:
                    fn += 1
                    if l < 6:
                        martl[l] = martl[l] + 1
                    l += 1
                maxl = max(maxl, l)
            if (j % 100 == 0):
                print(j / len(train_data))  # ,av)
                print(((tp + tn) / (tp + tn + fp + fn)), tp, fp, tn, fn, "    ", maxl, " - ", martw, martl, "   pips =",
                      pips)


df=collect(start='2018-01-30',end = '2018-03-30')
prizn=0.0002
train_data,res_data,di=cut(df,prizn)



for i in range(20):
    model = initModel()
    model, results = train(model, train_data, res_data, epoch=1)
    if analyzeTrain(results):
        print(i)
        break
model, results = train(model, train_data, res_data, epoch=19)
if prizn>0:
    name="put"
elif prizn<=0:
    name="call"
saveModel(model,name)
showResults(results)
smartCut(model,df,train_data,mode=0.5,Dmode=True,value=-0.0004)
