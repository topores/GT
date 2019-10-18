import telebot
import datetime

class bot(object):
    def __init__(self):
        try:
            token = '907888307:AAHY-BUv_xdxt_q1Nqz_M3HxNLQde-umEWI'
            self.bot = telebot.TeleBot(token)
            self.CHANNEL_NAME = '@moneygunforme'
        except Exception as e:
            print("!!!Error creating botManger",e)
        pass

    def sendMessage(self,S):
        try:
            self.bot.send_message(self.CHANNEL_NAME,S)
        except Exception as e:
            print("catched:",e,"\n",S)

def do():
    b=bot()
    f=open("event.ac","r")
    for line in f:
        r=line.find('trend:')
        if r>=0:
            tr=line[r+7:len(line)]
            print(tr)
        r = line.find('price:')
        if r >= 0:
            pr = line[r + 7:len(line)]
            print(pr)
    mess="prediction: "+str(tr)+"\n" \
                        "price: "+str(pr)+"\n"+"\n" \
                        "---system info---" +"\n"\
                        "now:"+str(datetime.datetime.now())+"\n"
    b.sendMessage(mess)
    print("message: \n"+ mess)
    print("sent")