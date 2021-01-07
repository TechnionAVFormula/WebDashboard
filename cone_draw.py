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
#get ability to use local images as backround
from PIL import Image
#import cv2
app = Flask(__name__)
#ootstrap = Bootstrap(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/formula_test"

mongo_uri = "mongodb://localhost:27017/"
client = pymongo.MongoClient(mongo_uri)
#client.list_database_names()
db = client.formula_test
db.list_collection_names()




all_messages = db.ConeInpictureTest
yellow_cones = []
blue_cones = []
position=[]
for obj in all_messages.find():
    id = (obj['header'])['id']
    cone_array = (obj['data'])['cones']
    for cone in cone_array:
        position.append(cone['x1'])
        position.append(cone['y1'])
        position.append(cone['x2'])
        position.append(cone['y2'])
        #if yellow
        if cone['type'] == "Yellow":
            yellow_cones.append((cone,id))
        else:
            blue_cones.append((cone,id))

def makedata(xList,yList,tList,pointType):
    data= {
        "x": xList,#list(dataset_by_time_and_cone[1]),
        "y": yList,
        "mode": 'lines+markers',#i think change to line here when car
        "text":tList,
        
        
        "name": pointType,
        "fill": "toself"
        # "marker": {
        #    "sizemode": "area",
        #    "sizeref": 200000,
        #    "size": list(dataset_by_year_and_cont["pop"])
        # },
    }
    return data

# for obj in yellow_cones:
#     print(obj['coneId'])

#make list of IDs
idstampList = list(range(2,200))
#make list of types of dots
types = ["Blue", "Yellow"]#, "Car"]    continents 
# make figure
fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

imagesList = []
for i in idstampList:
    if(i<10):
        stri = '00'+str(i)
    elif(i<100):
        stri='0'+str(i)
    else:
        stri = str(i)
    imagesList.append(dict(
            source= Image.open('c:/Users/tbita/OneDrive/Documents/formula/dashboard/ezgif/ezgif-frame-'+stri+'.jpg'),
            xref="x",
            yref="y",
            x=0,
            y=28,
            sizex=28,
            sizey=28,
            sizing="stretch",
            opacity=1,
            layer="below"))
# fill in most of layout
fig_dict["layout"]["xaxis"] = {"range": [min(position)-1, max(position)+1],"showgrid":False}
#fig_dict["layout"]["images"] = imagesList
fig_dict["layout"]["yaxis"] = {"range": [min(position)-1, max(position)+1],"showgrid":False}
fig_dict["layout"]["hovermode"] = "closest"
fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 1, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 1,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 1, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 1}}],
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
        "prefix": "time:",#is actually id for now
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 1, "easing": "cubic-in-out"},#change 100 to 1 for reall time speed
    "pad": {"b": 1, "t": 4},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

#data
#need to make 
def makeLists(xlist,ylist,tlist):
    xlist.append(ob['x1'])
    xlist.append(ob['x1'])
    xlist.append(ob['x2'])
    xlist.append(ob['x2'])
    xlist.append('None')
    ylist.append(ob['y1'])
    ylist.append(ob['y2'])
    ylist.append(ob['y2'])
    ylist.append(ob['y1'])
    ylist.append('None')

    tList.append(ob['coneId'])
time = min(idstampList)
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
        makeLists(xList,yList,tList)
    # print(xList)
    data_dict = makedata(xList,yList,tList,pointType) 
    
    #data_dict = go.Scatter(data_dict2)
    
    #print(type(data_dict))
    fig_dict["data"].append(data_dict)

#make frames:
# print(len(timestampList))
# print(len(set(timestampList)))
#print(idstampList)
i=0
for timestamp in idstampList:
    #print(i)
    #i = i+1
    frame = {"data": [], "name": str(timestamp), "layout": {}}
    frame["layout"]["images"] = []
    for pointType in types:
        current_message = [message for message in all_messages.find() if str(timestamp) == (str((message['header'])['id']))]
        #current_cones = (current_message['data'])['cones']
        # print()
        #print(current_message)
        # print()
        dataset_by_time_and_cone = [cone for cone in (((current_message[0])['data'])['cones']) if pointType == cone['type']]
        #print(dataset_by_time_and_cone)
        #print(type(dataset_by_time_and_cone[1]))
        xList = []
        yList =[]
        tList=[]
        for ob in dataset_by_time_and_cone:
            makeLists(xList,yList,tList)

        data_dict = makedata(xList,yList,tList,pointType)
        
        frame["data"].append(data_dict)
    frame["layout"]["images"].append(imagesList[i])
    i+=1
    fig_dict["frames"].append(frame)
    slider_step = {"args": [
        [timestamp],
        {"frame": {"duration": 1, "redraw": False},#change duration for real speed
         "mode": "immediate",
         "transition": {"duration": 1}}#and here
    ],
        "label": timestamp,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)

#print("stuk")
#print((fig_dict["frames"]))
fig_dict["layout"]["sliders"] = [sliders_dict]

fig = go.Figure(fig_dict)
pio.write_html(fig, file='../tomer_git/WebDashboard/static/picture_test.html',auto_play = False)#, auto_open=True)
#url=chart_studio.plotly.plot(fig, filename = 'picture_test',auto_open = False,render_mode = 'webgl')
#print(url)
#fig.show()


# @app.route("/")
# def home():
    
#     return render_template('State.html',url=url)


# if __name__ == "__main__":
#     app.run(debug=True)