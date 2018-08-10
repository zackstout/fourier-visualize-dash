
import pandas as pd
from textblob import TextBlob
import dash
import re
import numpy as np
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
from collections import defaultdict
# from flask import Flask
import os


app = dash.Dash(__name__)
server = app.server # Adding for deployment


app.layout = html.Div([
    html.H2('ahoy hoy'),
    # html.Div(children='''
    #     Speaker:
    # '''),
    dcc.Input(id='freq-in', value=1, type='int'),
    html.Button('Add to chart', id='btn'),
    html.Div(id='graph-out'),
    # dcc.Input(id='word-in', value='madness', type='text'),
    # html.Div(id='word-out', style={
    #     "color": "tomato",
    #     "text-align": "center",
    #     "font-family": "Georgia"
    # })
])

# Update the chart:
@app.callback(
    Output('graph-out','children'),
    [Input('freq-in', 'value')],
)
# Nice, needs to take in one parameter for each input, state (and event?):
def on_click(input_value):

    print(input_value)

    w = 10
    n = 200
    # n_ints = n/w
    xs = []
    ys = []
    for x in range(n):
        xs.append(x * w / n)
        ys.append(np.sin(int(input_value) * x * w / n))

    data = [{
        'x': xs,
        'y': ys,
        'type': 'line',
        'name': 'sine'
    }]

    # print(data[3])


    return dcc.Graph(
            id = 'whatev',
            figure = {
                'data': data,
                'layout': {
                    'title': 'HAMLET'
                }
            }
        )

if __name__ == '__main__':
    app.run_server(debug=True)
