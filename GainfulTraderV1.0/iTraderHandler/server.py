from http.server import BaseHTTPRequestHandler,HTTPServer
import datetime
import cgi
try:
    import telebot
    token = '554253191:AAFDkj6jfMdq3LJ0HgkI2wk3CxmgP5OL7-M'
    bot = telebot.TeleBot(token)
    CHANNEL_NAME = '@moneygunforme'
except:
    print("tg is not availableß")

def handleGet(path):
    a=path.find("errcode")
    b=path.find("spot")
    c = path.find("position")
    d=path.find("balance")
    e=path.find("state")
    S="time: "+str(datetime.datetime.now())+" \n"
    if (a!=-1):
        S=path[a:len(path)]
    elif (b!=-1 and c!=-1 and d!=-1):
        S += path[2:len(path)].replace('&',', \n')
    else:
        S="no paraeters send"
    try:

        bot.send_message(CHANNEL_NAME, S)
        print("data sent to bot")
    except:
        print("telegram is not Available")
    print("---new data received--\n")
    print(S)
    print("\n")
    return "string resieved: "+S

def handlePost(vars):
    print(vars)


class HttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        a=self.path
        #print(self.path)
        S=handleGet(a)

        self.send_response(200)
        self.send_header('content-type','text/html')
        self.end_headers()
        self.wfile.write(S.encode('utf-8'))
        print("get request done, time:", datetime.datetime.now())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        handlePost(post_data)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("POST!")

serv = HTTPServer(("localhost",8000),HttpProcessor)
print ("Web Server running on port %s" % 8080)
serv.serve_forever()
