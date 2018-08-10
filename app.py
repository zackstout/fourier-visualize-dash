
import pandas as pd
from textblob import TextBlob
import dash
import re
import numpy as np
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
from collections import defaultdict
import os

current_lines = []
xs = []

app = dash.Dash(__name__)
server = app.server # Adding for deployment

app.layout = html.Div([
    html.H2('ahoy hoy'),
    dcc.Input(id='freq-in', value=1, type='int'),
    # html.Button('Add to chart', id='btn'),
    html.Div(id='graph-out'),
    html.Div(id='graph2-out'),
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

def on_click(input_value):
    if (input_value == ''):
        return
    # print(input_value)
    w = 10
    n = 200
    ys = []
    y2s = []
    global xs

    for x in range(n):
        xs.append(x * w / n)
        ys.append(np.sin(int(input_value) * x * w / n))
        y2s.append(np.sin(int(input_value)/2 * x * w / n)) # Wow, it automatically gives them different colors!

    global current_lines # Huh, we have to say it here and when we read it..
    # Draw wave and its half-frequency brother:
    current_lines = [{
        'x': xs,
        'y': ys,
        'type': 'line',
        'name': 'sine'
    }, {
        'x': xs,
        'y': y2s,
        'type': 'line',
        'name': 'sine'
    }]

    return dcc.Graph(
            id = 'whatev',
            figure = {
                'data': current_lines,
                'layout': {
                    'title': 'Waves'
                }
            }
        )


@app.callback(
    Output('graph2-out','children'),
    [Input('freq-in', 'value')], # We also changed this, though I think the global change was the effective one. In fact, changing it to watch the graph-1 change messed it up!
)
# Uh oh, this ran first... Fixed with global
def on_change(val):
    global current_lines
    global xs
    # print(current_lines)
    summed_lines = {
        'x': xs,
        'y': [0] * len(xs), # Neat
        'type': 'line',
        'name': 'summed_sines'
    }

    for l in current_lines:
        for i, val in enumerate(l['y']):
            summed_lines['y'][i] += val

    print(summed_lines['y'])

    return dcc.Graph(
            id = 'whatev2',
            figure = {
                'data': [summed_lines],
                'layout': {
                    'title': 'Summed Waves'
                }
            }
        )







if __name__ == '__main__':
    app.run_server(debug=True)
