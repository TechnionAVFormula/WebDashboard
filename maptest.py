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
app.config["MONGO_URI"] = "mongodb://localhost:27017/formula_test"

mongo_uri = "mongodb://localhost:27017/"
client = pymongo.MongoClient(mongo_uri)
#client.list_database_names()
db = client.formula_test
db.list_collection_names()



def mapout():
    all_messages = db.TechnionFormulaAV.Messages.ConeMap
    yellow_cones = []
    blue_cones = []
    position=[]
    car =[]
    for obj in all_messages.find():
        time = (obj['header'])['timestamp']
        cone_array = (obj['data'])['cones']
        for cone in cone_array:
            position.append(cone['x'])
            position.append(cone['y'])
            #if yellow
            if cone['type'] == "Yellow":
                yellow_cones.append((cone,time))
            else:
                blue_cones.append((cone,time))

    # for obj in yellow_cones:
    #     print(obj['coneId'])
    start_of_time = 11
    end_of_time = 19
    #make list of timestamps
    timestampList = []  #year
    for obj in all_messages.find():
        time = (obj['header'])['timestamp']
        #time.split("T")[0]
        time = time[start_of_time:end_of_time]
        timestampList.append(time)

    timestampList=list(set(timestampList))
    timestampList.sort()
    #make list of types of dots
    types = ["Blue", "Yellow"]#, "Car"]    continents 

    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # fill in most of layout
    fig_dict["layout"]["xaxis"] = {"range": [min(position)-1, max(position)+1], "title": "X location"}
    fig_dict["layout"]["yaxis"] = {"range": [min(position)-1, max(position)+1], "title": "Y location"}
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["updatemenus"] = [
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

    #data
    #need to make 
    time = min(timestampList)
    for pointType in types:
        
        tmp =  ((all_messages.find_one()['data'])['cones'])
        dataset_by_time_and_cone = [cone for cone in tmp if pointType == cone['type']]
        
        # for obj in tmp:
        #     color = obj['type']
        #     if(color == pointType):
        #         dataset_by_time_and_cone.append(obj)
        

        xList = []
        yList =[]
        tList=[]
        for ob in dataset_by_time_and_cone:
            xList.append(ob['x'])
            yList.append(ob['y'])
            tList.append(ob['coneId'])

        data_dict = {
            "x": xList,#list(dataset_by_time_and_cone[1]),
            "y": yList,
            "mode": "markers",#i think change to line here when car
            "text":tList,
            
            # "marker": {
            #    "sizemode": "area",
            #    "sizeref": 200000,
            #    "size": list(dataset_by_year_and_cont["pop"])
            # },
            "name": pointType
        }
        fig_dict["data"].append(data_dict)

    #make frames:
    # print(len(timestampList))
    # print(len(set(timestampList)))

    for timestamp in timestampList:
        #print(i)
        #i = i+1
        frame = {"data": [], "name": str(timestamp)}
        for pointType in types:
            current_message = [message for message in all_messages.find() if timestamp == ((message['header'])['timestamp'])[start_of_time:end_of_time]]
            #current_cones = (current_message['data'])['cones']
            # print()
            # print(current_message)
            # print()
            dataset_by_time_and_cone = [cone for cone in (((current_message[0])['data'])['cones']) if pointType == cone['type']]
            #print(dataset_by_time_and_cone)
            #print(type(dataset_by_time_and_cone[1]))
            xList = []
            yList =[]
            tList=[]
            for ob in dataset_by_time_and_cone:
                xList.append(ob['x'])
                yList.append(ob['y'])
                tList.append(ob['coneId'])

            data_dict = {
                "x": xList,
                "y": yList,
                "mode": "markers",
                "text":tList,
                "name": pointType
            }
            
            #print(data_dict)
            frame["data"].append(data_dict)
        
        fig_dict["frames"].append(frame)
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
    fig_dict["layout"]["sliders"] = [sliders_dict]

    fig = go.Figure(fig_dict)
    pio.write_html(fig, file='../tomer_git/WebDashboard/static/cone_map.html',auto_play = False)#, auto_open=True)
#end of map out



# mapout()


# Add images
#fig.show()
# @app.route("/")
# def home():
    
#     return render_template('State.html',url=url)


# if __name__ == "__main__":
#     app.run(debug=True)