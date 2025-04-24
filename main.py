from flask import Flask, request
import os, random, time
from flask_mail import Mail, Message
import csv

time_prost = 30 #minute

sp_svob_fail = ["/login.html", "/reg.html", "/main.html"]

db_ip = [] #[[ip, time, [login, type]], ...]

db_registrat = {} #{ip : [password, tip, [...]], ...}

def update_time(ip):
    global db_ip
    while len(db_ip)>0 and db_ip[0][1] + time_prost*60*10e+9 < time.time_ns():
        db_ip.pop(0)
    for i in db_ip:
        if i[0] == ip:
            i[1] = time.time_ns()
            return True
    return False


name_csv = "./тестовые данные.csv"

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

#csv
with open(name_csv, "r", newline="") as file:
    reader_csv = csv.reader(file)
    dataCSV = []
    for i in reader_csv:
        if len(i) != 0:
            dataCSV.append(i)
    del reader_csv

dataCSV.pop(0)

#!!!!!! dataCSV !!!!!!


#sqlite

import sqlite3

db_connection = sqlite3.connect("./db_vol_part.db")
db_cursor = db_connection.cursor()

#таблица Профилей Волонтёров

db_cursor.execute('''
CREATE TABLE IF NOT EXISTS Volunteers (
id INTEGER PRIMARY KEY,
password TEXT NOT NULL,
uniquenumber INTEGER,
inn TEXT
)
''')
db_cursor.execute("CREATE INDEX IF NOT EXISTS ind_inn ON Volunteers (inn)")

db_cursor.execute('''
CREATE TABLE IF NOT EXISTS Partner (
id INTEGER PRIMARY KEY,
login TEXT NOT NULL,
email TEXT NOT NULL,
nameofcompanii TEXT NOT NULL,
password TEXT NOT NULL,
specteg TEXT NOT NULL
)
''')
db_cursor.execute("CREATE INDEX IF NOT EXISTS ind_login ON Partner (login)")
db_cursor.execute("CREATE INDEX IF NOT EXISTS ind_spectag ON Partner (specteg)")

db_connection.commit()

def addVolunteers(password, uniquenumber, inn):
    db_cursor.execute('INSERT INTO Volunteers (password, uniquenumber, inn) VALUES (?, ?, ?)', (password, uniquenumber, inn))
    db_connection.commit()
def addPartner(login, email, password):
    db_cursor.execute('INSERT INTO Partner (login, email, nameofcompanii, password, specteg) VALUES (?, ?, ?, ?, ?)', (login, email, "NoName", password, "None"))
    db_connection.commit()
def editVolunteers(inn, nameparam, value):
    db_cursor.execute('UPDATE Users SET ? = ? WHERE inn = ?', (nameparam, value, inn))
    db_connection.commit()
def editPartner(name_id, value_id, nameparam, value):
    db_cursor.execute('UPDATE Users SET ? = ? WHERE ? = ?', (nameparam, value, name_id, value_id))
    db_connection.commit()

def getByVolunteers(inn, param):
    db_cursor.execute('SELECT ? FROM Volunteers WHERE inn = ?', (param, inn))
    return cursor.fetchall()
def getByPartner(name_id, value_id, param):
    db_cursor.execute('SELECT ? FROM Partner WHERE ? = ?', (param, name_id, value_id))
    return db_cursor.fetchall()
def getVolunteers(inn):
    db_cursor.execute('SELECT * FROM Volunteers WHERE inn = ?', (inn))
    return db_cursor.fetchall()
def getPartner(param, name_id):
    db_cursor.execute('SELECT * FROM Partner WHERE ? = ?', (name_id, value_id))
    return db_cursor.fetchall()


def obrabotka(ip, dir):
    fl_name = "./test1/html"+dir
    fl_name.replace("%20", " ")
    if os.path.isfile(fl_name) and ".." not in fl_name:
        data = open(fl_name, "r").read()
        return True, data
    else:
        return False, ""




@app.route("/")
def main1():
    fl_name = "./test1/html/main.html"
    data = open(fl_name, "r").read()
    return data

# @app.route("/mail")
# def mail1():
#     send_code_to("slushatelnik@yandex.ru")

@app.route("/<dir>")
#----------------------
def prov(dir):
    if ("/"+dir == "/login.html?prov"):
        tip = request.headers.get("MyType")
        login = request.headers.get("MyLogin")
        password = request.headers.get("MyPassword")
        ip = request.remote_addr
        
        if not (isinstance(tip, str) and isinstance(login, str) and isinstance(password, str)):
            response.headers["MyState"] = "False"
            return response
        
        response = make_response("")
        response.headers["Content-Type"] = "text/plain"
        
        for i in range(len(db_ip)):
            if db_ip[i][0] == ip:
                db_ip.pop(i)
                break
        
        if tip == "Partner":
            rez = getByPartner("login", login, "password")
            if len(rez) == 0:
                response.headers["MyState"] = "False"
                return response
            elif password == rez[0][0]:
                response.headers["MyState"] = "True"
                db_ip.append([ip, time.time_ns(), [login, tip]])
                return response
            else:
                response.headers["MyState"] = "False"
                return response
        elif tip == "Volunteers":
            rez = getByPartner(login, "password")
            if len(rez) == 0:
                response.headers["MyState"] = "False"
                return response
            elif password == rez[0][0]:
                response.headers["MyState"] = "True"
                db_ip.append([ip, time.time_ns(), [login, tip]])
                return response
            else:
                response.headers["MyState"] = "False"
                return response
        else:
            response.headers["MyState"] = "False"
            return response
    elif ("/"+dir == "/reg.html?data"):
        tip = request.headers.get("MyType")
        ip = request.remote_addr
        if tip == "Volunteers":
            inn = request.headers.get("MyINN")
            password = request.headers.get("MyPassword")
            if not (isinstance(inn, str) and isinstance(password, str)):
                response.headers["MyState"] = "False"
                return response
            st = 0
            for i in len(range(dataCSV)):
                if inn == dataCSV[i][1]:
                    st = 1
                    break
            if st == 0:
                response.headers["MyState"] = "False"
                return response
            response = make_response("")
            response.headers["Content-Type"] = "text/plain"
            response.headers["MyState"] = "True"
            db_registrat[ip] = [password, tip, [inn]]
            return response
        elif tip == "Partner":
            login = request.headers.get("MyLogin")
            email = request.headers.get("MyEmail")
            password = request.headers.get("MyPassword")
            if not (isinstance(login, str) and isinstance(password, str) and isinstance(email, str)):
                response.headers["MyState"] = "False"
                return response
            response = make_response("")
            response.headers["Content-Type"] = "text/plain"
            response.headers["MyState"] = "True"
            db_registrat[ip] = [password, tip, [login, email]]
            return response
        else:
            response = make_response("")
            response.headers["Content-Type"] = "text/plain"
            response.headers["MyState"] = "False"
            return response
    elif ("/"+dir == "/reg.html?code"):
        tip = request.headers.get("MyType")
        ip = request.remote_addr
        
        response = make_response("")
        response.headers["Content-Type"] = "text/plain"
        
        if ip in db_registrat:
            if tip == db_registrat[ip][1]:
                code = request.headers.get("MyCode")
                if isinstance(code, str):
                    response.headers["MyState"] = "True"
                    #proverka koda
                    if tip == "Volunteers":
                        addVolunteers(db_registrat[ip][0], 0, db_registrat[ip][2][0])
                        return response
                    elif tip == "Partner":
                        addPartner(db_registrat[ip][2][0], db_registrat[ip][2][1], db_registrat[ip][0])
                        return response
        response.headers["MyState"] = "False"
        return response
                    
    elif ("/"+dir in sp_svob_fail):
        return open("./test1/html/"+dir, "r").read()
    else:
        ip = request.remote_addr
        st = update_time(ip)
        if st:
            for i in range(len(db_ip)):
                if db_ip[i][0] == ip:
                    db_ip[i][1] = time.time_ns()
                    break
            st, data = obrabotka(ip, "/"+dir)
            if st:
                return data;
            else:
                return open("./test1/html/main.html", "r").read()
        else:
            return open("./test1/html/main.html", "r").read()
#----------------------



app.run(debug=True, host = "127.0.0.1", port = 30000)
