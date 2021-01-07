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
import wtforms
#import open cv for picture color
import numpy as np
import cv2

#import all the plotly stuff
import maptest
import cone_draw

app = Flask(__name__)
#ootstrap = Bootstrap(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/formula_test"

mongo_uri = "mongodb://localhost:27017/"
client = pymongo.MongoClient(mongo_uri)
#client.list_database_names()
db = client.formula_test
db.list_collection_names()

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
    collection = db.TechnionFormulaAV.Messages.GPSSensor
    time = (collection.find_one()["header"])["timestamp"]
    time =  time[0:10]
    row1 = "%s"%time
    row2 = "hello"
    row3 = "thing"
    row4 = "doooooo"
    rows = [row1,row2,row3,row4]
    mulitiple = [rows,rows,rows,rows]
    return render_template("Main Menu.html", g = time,simulations = mulitiple)

@app.route("/State/<time>")
def datab(time):
    post_id = ObjectId("5ec16c5f801dc24573781066")
    collection = db.TechnionFormulaAV.Messages.GPSSensor
    id = (collection.find_one({"_id":post_id}))#["header"]
    maptest.mapout()
    cone_draw.coneout()
    return render_template("State.html", Date = time)#,urlmap=maptest.url,urlcamera = cone_draw.url)#(collection.find_one()["header"])["timestamp"])#online_users=id,y = collection.find_one()["header"], g = (collection.find_one()["header"])["timestamp"])

@app.route("/admin")
def admin():
    return redirect(url_for("user", name = admin))#name of function to redirect to if function has parameters add after , 

@app.route("/State")
def State():
    maptest.mapout()
    cone_draw.coneout()
    return render_template('State.html')

if __name__ == "__main__":
    app.run(debug=True)