#pymongo to connect to db
import pymongo

#probobly dont need
from flask import Flask, redirect,url_for,render_template, session
import plotly.graph_objects as go
import plotly.io as pio

#import flsk
from flask import Flask
from bson.objectid import ObjectId

import numpy as np

app = Flask(__name__)

mongo_uri = "mongodb://localhost:27017/"
client = pymongo.MongoClient(mongo_uri)

import json

def mapout(db_name):
    db = client[db_name]

    all_cone_messages = db.TechnionFormulaAV.Messages.ConeMap
    with open('fakeline.json') as json_file:
        all_path_messages = json.load(json_file)

    data_dict = {}

    for doc in all_cone_messages.find():
        # Extract the cone data and timestamp
        cones = doc["data"]["cones"]
        timestamp = doc["header"]["timestamp"]

        # Initialize lists to store the x and y values, and the color of the cones
        x_vals_blue = []
        y_vals_blue = []
        x_vals_yellow = []
        y_vals_yellow = []

        # Loop over each cone
        for cone in cones:
            # Append the x and y values to the appropriate lists
            if cone['type'] == 'Blue':
                x_vals_blue.append(cone["x"])
                y_vals_blue.append(cone["y"])
            else:  # Assuming the other type is 'Yellow'
                x_vals_yellow.append(cone["x"])
                y_vals_yellow.append(cone["y"])

        # Add the values to the dictionary
        data_dict[timestamp] = {"x_blue": x_vals_blue, "y_blue": y_vals_blue, 
                            "x_yellow": x_vals_yellow, "y_yellow": y_vals_yellow}
        

    # Define data attribute of figure with initial state of your traces.
    data=[
        go.Scatter(
            x=data_dict[list(data_dict.keys())[0]]["x_blue"], 
            y=data_dict[list(data_dict.keys())[0]]["y_blue"], 
            mode='markers', 
            name='Blue Cones', 
            marker=dict(size=10, color='blue')
        ),
        go.Scatter(
            x=data_dict[list(data_dict.keys())[0]]["x_yellow"], 
            y=data_dict[list(data_dict.keys())[0]]["y_yellow"], 
            mode='markers', 
            name='Yellow Cones', 
            marker=dict(size=10, color='yellow')
        ),
        go.Scatter(
            x=[0], y=[0], 
            mode="markers", 
            marker=dict(size=20, color="red"), 
            name="Car"
        )
    ]

    fig = go.Figure(data=data)

    # Create frames with updates for each timestamp
    frames = []
    for timestamp, data in data_dict.items():
        frame = go.Frame(
            data=[
                go.Scatter(
                    x=data["x_blue"], y=data["y_blue"]
                ),
                go.Scatter(
                    x=data["x_yellow"], y=data["y_yellow"]
                )
            ],
            name=timestamp
        )
        frames.append(frame)

    fig.frames = frames
    
    fig.data[0].visible = True
    fig.data[1].visible = True
    fig.data[2].visible = True

    # Create and add a slider
    steps = []
    for i in range(len(fig.frames)):
        step = dict(
            method="animate",
            args=[[fig.frames[i].name]],
            label=fig.frames[i].name[11:19]
        )
        steps.append(step)

    sliders = [dict(active=0, pad={"t": 1}, steps=steps)]


    fig.update_layout(
        hovermode="closest",
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 50, "redraw": False},
                                        "fromcurrent": True, "transition": {"duration": 30,
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
                "pad": {"r": 5, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }
        ],
        sliders=sliders
    )

    pio.write_html(fig, file='./static/cone_map.html',auto_play = False)
     
# mapout()


# Add images
#fig.show()
# @app.route("/")
# def home():
    
#     return render_template('State.html',url=url)


if __name__ == "__main__":
#     app.run(debug=True)
    mapout("formula-db")