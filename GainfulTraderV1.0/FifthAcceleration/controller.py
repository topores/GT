import  subprocess

import datetime
import os
import online
import iTelegramer

def setTar():
    now=datetime.datetime.now()
    delta = 5 - (now.minute % 5)
    delta = 1
    now=now+datetime.timedelta(minutes=delta)
    target = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0, 0)
    return target


target=setTar()
callModel,putModel = online.loadModels()
online.do(callModel,putModel)
now0=datetime.datetime.now()
while True:
    now = datetime.datetime.now()
    #target=now
    #os.system('clear')
    #print("time: ",datetime.datetime.now(),", waiting for:",target)
    if now>=target:
        target+=datetime.timedelta(minutes=1)
        print("now - ",now,"; target - ", target)
        #subprocess.call('python3 /Users/davydov_rostislav/PycharmProjects/FifthAcceleraton/online.py',shell=True)
        online.do(callModel,putModel)
        print("online.do() done!,time: "+str(datetime.datetime.now()))
        #subprocess.call('python3 /Users/davydov_rostislav/PycharmProjects/FifthAcceleraton/iTelegramer.py', shell=True)
        iTelegramer.do()
    if (datetime.datetime.now()>(now0+datetime.timedelta(seconds=1))):
        now0=datetime.datetime.now()
        print("time: ", now0, ", waiting for:", target)

