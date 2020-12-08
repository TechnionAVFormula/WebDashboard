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
    return render_template("home.html",content = [1,2,3,4,5]) #"Hellow world <h1> ! <h1>"

@app.route("/MainMenu")#thing between <> is passed to the page
def user():
    # session["person"] = name
    #address = wtforms.TextAreaField(u'Mailing Address', [wtforms.validators.optional(), wtforms.validators.length(max=200)])
    collection = db.TechnionFormulaAV.Messages.GPSSensor
    time = (collection.find_one()["header"])["timestamp"]
    time =  time[0:10]
    return render_template("Main Menu.html", g = time)

@app.route("/<time>")
def datab(time):
    post_id = ObjectId("5ec16c5f801dc24573781066")
    collection = db.TechnionFormulaAV.Messages.GPSSensor
    id = (collection.find_one({"_id":post_id}))#["header"]
    return render_template("State.html", Date = time)#(collection.find_one()["header"])["timestamp"])#online_users=id,y = collection.find_one()["header"], g = (collection.find_one()["header"])["timestamp"])

@app.route("/admin")
def admin():
    return redirect(url_for("user", name = admin))#name of function to redirect to if function has parameters add after , 
@app.route("/map")
def map():
    fig = go.Figure(go.Scattermapbox(
        mode = "markers+lines",
        lon = [10, 20, 30],
        lat = [10, 20,30],
        marker = {'size': 10}))

    fig.add_trace(go.Scattermapbox(
        mode = "markers+lines",
        lon = [-50, -60,40],
        lat = [30, 10, -20],
        marker = {'size': 10}))

    fig.update_layout(
        margin ={'l':0,'t':0,'b':0,'r':0},
        mapbox = {
            'center': {'lon': 10, 'lat': 10},
            'style': "stamen-terrain",
            'center': {'lon': -20, 'lat': -20},
            'zoom': 1})

    fig.show()
#image = cv2.imread('images(1).jpg',cv2.IMREAD_COLOR)
#@app.route("/image")
#def images():
#    return cv2.imshow('image',image)

if __name__ == "__main__":
    app.run(debug=True)