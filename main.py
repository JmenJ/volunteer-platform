from flask import Flask, request, make_response
import os, random, time, sys
from flask_mail import Mail, Message
import csv

print("\nLine: 6\n", file=sys.stderr)

time_prost = 30 #minute

sp_svob_fail = ["/login.html", "/reg.html"]

db_ip = [] #[[ip, time, [login, type]], ...]

db_registrat = {} #{ip : [password, tip, [...]], ...}

def update_time(ip):
    global db_ip
    print("\nLine: 18\n", db_ip, file=sys.stderr)
    while len(db_ip)>0 and db_ip[0][1] + time_prost*60*10e+9 < time.time_ns():
        print("\nLine: 20\n", len(db_ip), file=sys.stderr)
        db_ip.pop(0)
    for i in range(len(db_ip)):
        print("\nLine: 23\n", db_ip, file=sys.stderr)
        if db_ip[i][0] == ip:
            print("\nLine: 25\n", ip, file=sys.stderr)
            db_ip[i][1] = time.time_ns()
            print("\nLine: 27\n", db_ip[i], file=sys.stderr)
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
with open(name_csv, "r", newline="", encoding="utf-8") as file:
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

db_connection = sqlite3.connect("./db_vol_part.db", check_same_thread=False)
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
    return db_cursor.fetchall()
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
    print("\nLine: 124\n", file=sys.stderr)
    if (db_registrat[ip][1] == "Volunteers"):
        print("\nLine: 126\n", file=sys.stderr)
        if dir == "/main_vol.html":
            print("\nLine: 128\n", file=sys.stderr)
            fl_name = "./test1/html"+dir
            print("\nLine: 130\n", file=sys.stderr)
            return True, open(fl_name, "r").read()
        else:
            print("\nLine: 133\n", file=sys.stderr)
            return False, ""
    elif db_registrat[ip][1] == "Partner":
        print("\nLine: 136\n", file=sys.stderr)
        if dir == "/main_par.html":
            print("\nLine: 138\n", file=sys.stderr)
            fl_name = "./test1/html"+dir
            print("\nLine: 140\n", file=sys.stderr)
            return True, open(fl_name, "r").read()
        else:
            print("\nLine: 143\n", file=sys.stderr)
            return False, ""




@app.route("/")
def main1():
    fl_name = "./test1/html/login.html"
    data = open(fl_name, "r").read()
    return data

# @app.route("/mail")
# def mail1():
#     send_code_to("slushatelnik@yandex.ru")

@app.route("/<dir>")
def prov(dir):
    print("\nLine: 161\n", file=sys.stderr)
    global db_ip
    print("\nLine: 163\n", file=sys.stderr)
    if ("/"+dir == "/login.html_prov"):
        print("\nLine: 165\n", file=sys.stderr)
        tip = request.headers.get("MyType")
        login = request.headers.get("MyLogin")
        password = request.headers.get("MyPassword")
        ip = request.remote_addr
        print("\nLine: 170\n", file=sys.stderr)
        response = make_response("")
        response.headers["Content-Type"] = "text/plain"
        if not (isinstance(tip, str) and isinstance(login, str) and isinstance(password, str)):
            print("\nLine: 174\n", file=sys.stderr)
            response.headers["MyState"] = "False"
            return response
        
        for i in range(len(db_ip)):
            print("\nLine: 179\n", file=sys.stderr)
            if db_ip[i][0] == ip:
                print("\nLine: 181\n", file=sys.stderr)
                db_ip.pop(i)
                break
        
        if tip == "Partner":
            print("\nLine: 186\n", file=sys.stderr)
            rez = getByPartner("login", login, "password")
            print("\nLine: 188\n", file=sys.stderr)
            if len(rez) == 0:
                print("\nLine: 190\n", file=sys.stderr)
                response.headers["MyState"] = "False"
                return response
            elif password == rez[0][0]:
                print("\nLine: 194\n", file=sys.stderr)
                response.headers["MyState"] = "True"
                db_ip.append([ip, time.time_ns(), [login, tip]])
                print("\nLine: 197\n", file=sys.stderr)
                return response
            else:
                response.headers["MyState"] = "False"
                print("\nLine: 201\n", file=sys.stderr)
                return response
        elif tip == "Volunteers":
            print("\nLine: 204\n", file=sys.stderr)
            rez = getByVolunteers(login, "password")
            print("\nLine: 206\n", file=sys.stderr)
            if len(rez) == 0:
                print("\nLine: 208\n", file=sys.stderr)
                response.headers["MyState"] = "False"
                return response
            elif str(password) == rez[0][0]:
                print("\nLine: 212\n", file=sys.stderr)
                response.headers["MyState"] = "True"
                db_ip.append([ip, time.time_ns(), [login, tip]])
                print("\nLine: 215\n", file=sys.stderr)
                return response
            else:
                print("\nLine: 218\n", file=sys.stderr)
                response.headers["MyState"] = "False"
                return response
        else:
            print("\nLine: 222\n", file=sys.stderr)
            response.headers["MyState"] = "False"
            return response
    elif ("/"+dir == "/reg.html_data"):
        print("\nLine: 226\n", file=sys.stderr)
        tip = request.headers.get("MyType")
        ip = request.remote_addr
        print("\nLine: 229\n", file=sys.stderr)
        if tip == "Volunteers":
            print("\nLine: 231\n", file=sys.stderr)
            inn = request.headers.get("MyINN")
            password = request.headers.get("MyPassword")
            print("\nLine: 234\n", file=sys.stderr)
            if not (isinstance(inn, str) and isinstance(password, str)):
                response.headers["MyState"] = "False"
                print("\nLine: 237\n", file=sys.stderr)
                return response
            print("\nLine: 239\n", file=sys.stderr)
            st = 0
            for i in range(len(dataCSV)):
                print("\nLine: 242\n", file=sys.stderr)
                if inn == dataCSV[i][1]:
                    print("\nLine: 244\n", file=sys.stderr)
                    st = 1
                    break
            print("\nLine: 247\n", file=sys.stderr)
            if st == 0:
                print("\nLine: 249\n", file=sys.stderr)
                response.headers["MyState"] = "False"
                return response
            response = make_response("")
            response.headers["Content-Type"] = "text/plain"
            response.headers["MyState"] = "True"
            print("\nLine: 255\n", file=sys.stderr)
            db_registrat[ip] = [password, tip, [inn]]
            print("\nLine: 257\n", file=sys.stderr)
            return response
        elif tip == "Partner":
            print("\nLine: 260\n", file=sys.stderr)
            login = request.headers.get("MyLogin")
            email = request.headers.get("MyEmail")
            password = request.headers.get("MyPassword")
            print("\nLine: 264\n", file=sys.stderr)
            if not (isinstance(login, str) and isinstance(password, str) and isinstance(email, str)):
                response.headers["MyState"] = "False"
                print("\nLine: 267\n", file=sys.stderr)
                return response
            response = make_response("")
            response.headers["Content-Type"] = "text/plain"
            response.headers["MyState"] = "True"
            db_registrat[ip] = [password, tip, [login, email]]
            print("\nLine: 273\n", file=sys.stderr)
            return response
        else:
            response = make_response("")
            response.headers["Content-Type"] = "text/plain"
            response.headers["MyState"] = "False"
            return response
    elif ("/"+dir == "/reg.html_code"):
        print("\nLine: 281\n", file=sys.stderr)
        tip = request.headers.get("MyType")
        ip = request.remote_addr
        print("\nLine: 284\n", file=sys.stderr)
        response = make_response("")
        response.headers["Content-Type"] = "text/plain"
        print("\nLine: 287\n", file=sys.stderr)
        if ip in db_registrat:
            print("\nLine: 289\n", file=sys.stderr)
            if tip == db_registrat[ip][1]:
                print("\nLine: 291\n", file=sys.stderr)
                code = request.headers.get("MyCode")
                print("\nLine: 293\n", file=sys.stderr)
                if isinstance(code, str):
                    print("\nLine: 295\n", file=sys.stderr)
                    response.headers["MyState"] = "True"
                    #proverka koda
                    print("\nLine: 298\n", file=sys.stderr)
                    if tip == "Volunteers":
                        print("\nLine: 300\n", file=sys.stderr)
                        addVolunteers(db_registrat[ip][0], 0, db_registrat[ip][2][0])
                        db_ip.append([ip, time.time_ns(), [db_registrat[ip][2][0], tip]])
                        response.headers["MyState"] = "True"
                        print("\nLine: 304\n", file=sys.stderr)
                        return response
                    elif tip == "Partner":
                        print("\nLine: 307\n", file=sys.stderr)
                        addPartner(db_registrat[ip][2][0], db_registrat[ip][2][1], db_registrat[ip][0])
                        db_ip.append([ip, time.time_ns(), [db_registrat[ip][2][0], tip]])
                        response.headers["MyState"] = "True"
                        print("\nLine: 311\n", file=sys.stderr)
                        return response
        print("\nLine: 313\n", file=sys.stderr)
        response.headers["MyState"] = "False"
        return response
                    
    elif ("/"+dir in sp_svob_fail):
        print("\nLine: \n", file=sys.stderr)
        return open("./test1/html/"+dir, "r").read()
    else:
        print("\nLine: 321\n", file=sys.stderr)
        ip = request.remote_addr
        st = update_time(ip)
        print("\nLine: 324\n", file=sys.stderr)
        if st:
            print("\nLine: 326\n", file=sys.stderr)
            for i in range(len(db_ip)):
                print("\nLine: 328\n", file=sys.stderr)
                if db_ip[i][0] == ip:
                    print("\nLine: 330\n", file=sys.stderr)
                    db_ip[i][1] = time.time_ns()
                    print("\nLine: 332\n", file=sys.stderr)
                    break
            st, data = obrabotka(ip, "/"+dir)
            print("\nLine: 335\n", file=sys.stderr)
            if st:
                print("\nLine: 337\n", file=sys.stderr)
                return data;
            else:
                print("\nLine: 340\n", file=sys.stderr)
                return open("./test1/html/login.html", "r").read()
        else:
            print("\nLine: 343\n", file=sys.stderr)
            return open("./test1/html/login.html", "r").read()
#----------------------



app.run(debug=True, host = "127.0.0.1", port = 30000)
