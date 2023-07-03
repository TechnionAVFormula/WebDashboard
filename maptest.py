#pymongo to connect to db
import pymongo

#probobly dont need
from flask import Flask, redirect,url_for,render_template, session
import plotly.graph_objects as go
import plotly.io as pio

#import flsk
from flask import Flask
from bson.objectid import ObjectId

#generate url
import chart_studio
#import chart_studio.plotly as chart_studio
chart_studio.tools.set_credentials_file(username='tomer1577', api_key='nMc8DayOGiC9knDWxmhQ')


#import bootstrap
#from flask.bootstrap import Bootstrap
#import wtforms
#import open cv for picture color
import numpy as np
#import cv2
app = Flask(__name__)
#ootstrap = Bootstrap(app)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/formula_test"

mongo_uri = "mongodb://localhost:27017/"
client = pymongo.MongoClient(mongo_uri)
#client.list_database_names()
#optimal_route
import json
temp_fake_line = open("fakeline.json", 'r')
all_path_messages = json.load(temp_fake_line) #need to be dashboard messages.ControlDashbaord.optimal_route


def mapout(the_db='formula-db'):
    db = client[the_db]
    all_cone_messages = db.TechnionFormulaAV.Messages.ConeMap
    position=[]
    for obj in all_cone_messages.find():
        # print(obj)
        cone_array = (obj['data'])['cones']
        for cone in cone_array:
            position.append(cone['x'])
            position.append(cone['y'])

    start_of_time = 11
    end_of_time = 19
    #make list of timestamps
    timestampList = list(set([(obj['header'])['timestamp'][start_of_time:end_of_time] for obj in all_cone_messages.find()]))
    timestampList.sort()
    # make figure
    marker_data = {
        "data": [],
        "layout": {
            "xaxis": {"range": [min(position)-1, max(position)+1], "title": "X location"},
            "yaxis": {"range": [min(position)-1, max(position)+1], "title": "Y location"},
            "hovermode": "closest"
        },
        "frames": []
    }

    # fill in most of layout
    # marker_data["layout"]["xaxis"] = {"range": [min(position)-1, max(position)+1], "title": "X location"}
    # marker_data["layout"]["yaxis"] = {"range": [min(position)-1, max(position)+1], "title": "Y location"}
    # marker_data["layout"]["hovermode"] = "closest"
    duration = 300
    marker_data["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": duration, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": duration,
                                                                        "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 5, "t": 87},#should be less i think
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "time:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 100, "easing": "cubic-in-out"},#change 100 to 1 for reall time speed
        "pad": {"b": 1, "t": 40},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }

    line_data = marker_data.copy()
    
    #make data
    tmp =  ((all_cone_messages.find_one()['data'])['cones'])
    marker_data["data"] = [cone_frame(tmp,'Blue'), cone_frame(tmp,'Yellow')]

    #make frames:
    for timestamp in timestampList: 
        frame = {"data": [], "name": str(timestamp)}
        path_frame = {"data": [], "name": str(timestamp)}
        current_cone_message = [message for message in all_cone_messages.find() if timestamp == ((message['header'])['timestamp'])[start_of_time:end_of_time]]
        curr_msg = (((current_cone_message[0])['data'])['cones'])
        frame["data"] = [cone_frame(curr_msg,'Blue'), cone_frame(curr_msg,'Yellow')]
        
        marker_data["frames"].append(frame)
        slider_step = {"args": [
            [timestamp],
            {"frame": {"duration": duration, "redraw": False},#change duration
            "mode": "immediate",
            "transition": {"duration": duration}}
        ],
            "label": timestamp,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)


    marker_data["layout"]["sliders"] = [sliders_dict]
    line_data["layout"]["sliders"] = [sliders_dict]

    fig = go.Figure(marker_data)
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=20, color="red"), name="car"))
    pio.write_html(fig, file='./static/cone_map.html',auto_play = False), #auto_open = True)

def cone_frame(curr_msg,pointType):
    dataset_by_time_and_cone = [cone for cone in curr_msg if pointType == cone['type']]
    #insert get for path 
    xList = []
    yList =[]
    tList=[]
    for ob in dataset_by_time_and_cone:
        xList.append(ob['x'])
        yList.append(ob['y'])
        tList.append(ob.get('coneId',0))

    cone_data_dict = {
        "x": xList,
        "y": yList,
        "mode": "markers",
        "text":tList,
        "name": pointType,
        "marker": {
        "size": 10,
        "color": pointType,
        },
    }
    return cone_data_dict

if __name__ == "__main__":
#     app.run(debug=True)
    mapout()