#pymongo to connect to db
import pymongo

#probobly dont need
from flask import Flask, redirect,url_for,render_template, session
import plotly.graph_objects as go

#import flsk
from flask import Flask
from bson.objectid import ObjectId

#import bootstrap
#from flask.bootstrap import Bootstrap
#for now? import wtforms
#import open cv for picture color
import numpy as np
# for now import cv2

#import all the plotly stuff
import maptest
# import cone_draw

app = Flask(__name__)
#ootstrap = Bootstrap(app)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/formula_2020-05-17-19:54:34"#"mongodb://localhost:27017/formula_test"

mongo_uri = "mongodb://localhost:27017/"
client = pymongo.MongoClient(mongo_uri)
# print(client.list_database_names())
dbs = ["formula-db"]#formula_test
# print(db.list_collection_names())

#This happened probably because the MongoDB service isn't started. Follow the below steps to start it:
#Go to Control Panel and click on Administrative Tools.
#Double click on Services. A new window opens up.
#Search MongoDB.exe. Right click on it and select Start.


@app.route("/")
def home():
    # if "person" in session:
    #     return render_template("home.html",content = session["person"])
    return redirect(url_for("user"))
    #return render_template("home.html",content = [1,2,3,4,5]) #"Hellow world <h1> ! <h1>"

@app.route("/MainMenu")#thing between <> is passed to the page
def user():
    # session["person"] = name
    #address = wtforms.TextAreaField(u'Mailing Address', [wtforms.validators.optional(), wtforms.validators.length(max=200)])
    rows = []
    for db_name in dbs:
        db = client[db_name]
        collection = db.TechnionFormulaAV.Messages.GPSSensor
        daytime = (collection.find_one()["header"])["timestamp"]
        day =  daytime[0:10]
        time = daytime[11:23]

        row1 = "%s"%db_name
        row2 = "%s"%day
        row3 = "%s"%time
        row4 = "doooooo"
        row = [row1, row2, row3, row4]
        rows.append(row)
    return render_template("Main Menu.html",simulations = rows)

@app.route("/State/<db_name>")
def datab(db_name):
    # post_id = ObjectId("5ec16c5f801dc24573781066")
    maptest.mapout(db_name)
    # cone_draw.coneout()
    return render_template("State.html", Database = db_name)#,urlmap=maptest.url,urlcamera = cone_draw.url)#(collection.find_one()["header"])["timestamp"])#online_users=id,y = collection.find_one()["header"], g = (collection.find_one()["header"])["timestamp"])

@app.route("/admin")
def admin():
    return redirect(url_for("user", name = admin))#name of function to redirect to if function has parameters add after , 

@app.route("/State")
def State():
    maptest.mapout()
    # cone_draw.coneout()
    return render_template('State.html')
@app.route("/Control")
def Control():
    return render_template('Control.html')

if __name__ == "__main__":
    app.run(debug=True)