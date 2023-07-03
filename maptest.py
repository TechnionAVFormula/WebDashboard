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
db = client["formula-db"]
#optimal_route
import json
temp_fake_line = open("fakeline.json", 'r')


def mapout(db_name):
    db = client[db_name]

    all_cone_messages = db.TechnionFormulaAV.Messages.ConeMap
#    all_path_messages = json.load(temp_fake_line) #need to be dashboard messages.ControlDashbaord.optimal_route
    yellow_cones = []
    blue_cones = []
    position=[]
    car =[]
    for obj in all_cone_messages.find():
        # print(obj)
        time = (obj['header'])['timestamp']
        cone_array = (obj['data'])['cones']
        for cone in cone_array:
            position.append(cone['x'])
            position.append(cone['y'])
            #if yellow
            if cone['type'] == "Yellow":
                yellow_cones.append((cone,time))
            else:
                print("in blue")
                blue_cones.append((cone,time))

    start_of_time = 11
    end_of_time = 19
    #make list of timestamps
    timestampList = []  #year
    for obj in all_cone_messages.find():
        time = (obj['header'])['timestamp']
        #time.split("T")[0]
        time = time[start_of_time:end_of_time]
        timestampList.append(time)

    timestampList=list(set(timestampList))
    timestampList.sort()
    #make list of types of dots
    types = ["Blue", "Yellow"]#, "Car"]    continents 

    # make figure
    marker_data = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # fill in most of layout
    marker_data["layout"]["xaxis"] = {"range": [min(position)-1, max(position)+1], "title": "X location"}
    marker_data["layout"]["yaxis"] = {"range": [min(position)-1, max(position)+1], "title": "Y location"}
    marker_data["layout"]["hovermode"] = "closest"
    marker_data["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": False},
                                    "fromcurrent": True, "transition": {"duration": 300,
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
    #data
    #need to make 
    time = min(timestampList)
    for pointType in types:#check if this is the thing being printed
        # print("in type ", pointType)
        tmp =  ((all_cone_messages.find_one()['data'])['cones'])
        dataset_by_time_and_cone = [cone for cone in tmp if pointType == cone['type']]
        
        # for obj in tmp:
        #     color = obj['type']
        #     if(color == pointType):
        #         dataset_by_time_and_cone.append(obj)
        
        # print(dataset_by_time_and_cone)
        xList = []
        yList =[]
        tList=[]
        for ob in dataset_by_time_and_cone:
            xList.append(ob['x'])
            yList.append(ob['y'])
            tList.append(ob.get('coneId',0))

        data_dict = {
            "x": xList,#list(dataset_by_time_and_cone[1]),
            "y": yList,
            "mode": "markers",#i think change to line here when car
            "text":tList,
            "name": pointType,
            
            "marker": {
               "size": 10,
               "color": pointType,
            },
        }
        marker_data["data"].append(data_dict)

    #make frames:

    for timestamp in timestampList: #shouldnt be here if have other one?
        #print(i)
        #i = i+1
        frame = {"data": [], "name": str(timestamp)}
        path_frame = {"data": [], "name": str(timestamp)}
        for pointType in types:
            current_cone_message = [message for message in all_cone_messages.find() if timestamp == ((message['header'])['timestamp'])[start_of_time:end_of_time]]
            # current_path_message = [message for message in all_path_messages.find() if timestamp == ((message['header'])['timestamp'])[start_of_time:end_of_time]]
            
            dataset_by_time_and_cone = [cone for cone in (((current_cone_message[0])['data'])['cones']) if pointType == cone['type']]
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
            path_data_dict = {# don t forget to add 00 at start
                "x": xList,#################change to path place
                "y": yList,################## chang to path place
                "mode": "line",
                "text":"going",
                "name":"planned path"
            }
            
            #print(data_dict)
            frame["data"].append(cone_data_dict)
            # path_frame["data"].append(path_data_dict)
            
        
        marker_data["frames"].append(frame)
        # line_data["frames"].append(path_frame)
        slider_step = {"args": [
            [timestamp],
            {"frame": {"duration": 300, "redraw": False},#change duration
            "mode": "immediate",
            "transition": {"duration": 300}}
        ],
            "label": timestamp,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)

    #print("stuk")
    #print((fig_dict["frames"]))
    marker_data["layout"]["sliders"] = [sliders_dict]
    line_data["layout"]["sliders"] = [sliders_dict]

    fig = go.Figure(marker_data)#remove marker_Data!!!!!!!???marker_data
    # fig.add_trace(marker_data)
    # fig.add_trace(line_data)
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers", marker=dict(size=20, color="red"), name="car"))
    pio.write_html(fig, file='./static/cone_map.html',auto_play = False)
#end of map out"C:\Users\tbita\OneDrive\Documents\formula\dashboard\tomer_git\WebDashboard\static\cone_map.html"



# mapout()


# Add images
#fig.show()
# @app.route("/")
# def home():
    
#     return render_template('State.html',url=url)


if __name__ == "__main__":
#     app.run(debug=True)
    mapout()