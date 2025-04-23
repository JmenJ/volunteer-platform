from flask import Flask
import os, random
from flask_mail import Mail, Message

app = Flask(__name__, static_folder="./test1/assets")

app.config['MAIL_USE_TLS'] = True
app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 587

mail = Mail(app)

def send_code_to(ml):
    msg = Message(subject = "Ресурсный центр поддержки добровольчества", sender="rcpd@mail.ru", recipients=[ml])
    i = random.randint(0, 99999999)
    msg.body = "Код подтверждения: " + "0"*(8 - len(str(i))) + str(i)
    mail.send(msg)

@app.route("/")
def main1():
    fl_name = "./test1/html/main.html"
    data = open(fl_name, "r").read()
    return data

@app.route("/mail")
def mail1():
    send_code_to("slushatelnik@yandex.ru")

@app.route("/<dir>")
def prov(dir):
    fl_name = "./test1/html/"+dir
    fl_name.replace("%20", " ")
    print(fl_name)
    if os.path.isfile(fl_name) and ".." not in fl_name:
        data = open(fl_name, "r").read()
    else:
        data = dir + " Not found!"
    return data


app.run(debug=True, host = "127.0.0.1", port = 30000)
