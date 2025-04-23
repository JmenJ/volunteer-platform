from flask import Flask
import os

app = Flask(__name__, static_folder="./test1/assets")

@app.route("/")
def main1():
    fl_name = "./test1/html/main.html"
    data = open(fl_name, "r").read()
    return data

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
