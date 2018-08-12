
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
    html.Div(id='dummy'),
    html.Canvas(id='canv')
])


# Band-aid fix for not really grokking async stuff here:
# And even still, we're depending on the other callbacks running in the right order:
@app.callback(
    Output('dummy', 'children'),
    [Input('freq-in', 'value')],
)
def on_change(input_value):
    return html.P(input_value)



# @app.callback(
#     Output('canv', 'style'),
#     [Input('graph2-out', 'children')],
# )
# def on_change2(input_value):
#     return {'background-color': 'green'};



# Update the first chart:
@app.callback(
    Output('graph-out','children'),
    [Input('freq-in', 'value')],
)
def on_click(input_value):
    if (input_value == ''):
        return
    w = 10
    n = 500 # Controls the resolution
    ys = []
    y2s = []
    global xs

    xs = []
    
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
        'name': 'sine1'
    }, {
        'x': xs,
        'y': y2s,
        'type': 'line',
        'name': 'sine2'
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


# Update the second (cumulative) chart:
@app.callback(
    Output('graph2-out','children'),
    # Oh but this is also no good, because the values get recalculate inside of other callback...
    [Input('graph-out', 'children')], # We also changed this, though I think the global change was the effective one. In fact, changing it to watch the graph-1 change messed it up!
)
# Uh oh, this ran first... Fixed with global -- and new, alpha callback.
def on_change(val):
    global current_lines
    global xs

    # print('LENGTH ', len(xs)) # Yep, this is it, xs are never getting cleared out.

    summed_lines = {
        'x': list(filter(lambda x: x != 0, xs)), # Haha, well at least the extraneous lines are horizontal now...
        'y': [0] * len(xs), # Neat
        'type': 'line',
        'name': 'summed',
        # 'connectgaps': False
    }
    # Dot product:
    dotted_lines = {
        'x': list(filter(lambda x: x != 0, xs)), # Haha, well at least the extraneous lines are horizontal now...
        'y': [1] * len(xs), # Neat
        'type': 'line',
        'name': 'dotted',
        # 'connectgaps': False
    }

    for l in current_lines:
        for i, val in enumerate(l['y']):
            summed_lines['y'][i] += val
            dotted_lines['y'][i] *= val

    # summed_lines['y'] = summed_lines['y'][summed_lines['y'].index(0) : ]

    return dcc.Graph(
            id = 'whatev2',
            figure = {
                'data': [summed_lines, dotted_lines], # Don't forget this must be an array
                'layout': {
                    'title': 'Summed Waves'
                }
            }
        )


if __name__ == '__main__':
    app.run_server(debug=True)
