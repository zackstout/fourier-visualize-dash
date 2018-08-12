
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
    html.H2('LET\'S GET FOURIER!'),
    # dcc.Input(id='freq-in', value=1, type='int'),
    html.Div([
        html.P('Wave 1 frequency:'),
        dcc.Slider(
        id='w1_freq',
        min=1,
        max=20,
        step=0.5,
        value=1,
        ),
        html.P('Wave 1 shift:'),
        dcc.Slider(
        id='w1_shift',
        min=0,
        max=2*np.pi,
        step=0.1,
        value=0,
        ),
    ]),
    html.Div([
        html.P('Wave 2 frequency:'),
        dcc.Slider(
        id='w2_freq',
        min=0.5,
        max=20,
        step=0.5,
        value=0.5,
        ),
        html.P('Wave 2 shift:'),
        dcc.Slider(
        id='w2_shift',
        min=0,
        max=2*np.pi,
        step=0.1,
        value=0,
        ),
    ]),
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
    [Input('w1_freq', 'value'), Input('w1_shift', 'value'), Input('w2_freq', 'value'), Input('w2_shift', 'value')],
)
def on_change(val1, val2, val3, val4):
    return html.P(val1)



# @app.callback(
#     Output('canv', 'style'),
#     [Input('graph2-out', 'children')],
# )
# def on_change2(input_value):
#     return {'background-color': 'green'};



# Update the first chart:
@app.callback(
    Output('graph-out','children'),
    [Input('w1_freq', 'value'), Input('w1_shift', 'value'), Input('w2_freq', 'value'), Input('w2_shift', 'value')],
)
def on_click(w1_freq, w1_shift, w2_freq, w2_shift):
    # if (input_value == ''):
    #     return
    w = 10
    n = 500 # Controls the resolution
    ys = []
    y2s = []
    global xs

    xs = []

    for x in range(n):
        xs.append(x * w / n)
        ys.append(np.sin(w1_freq * x * w / n + w1_shift))
        y2s.append(np.sin(w2_freq * x * w / n + w2_shift)) # Wow, it automatically gives them different colors!

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
# @app.callback(
#     Output('graph2-out','children'),
#     # Oh but this is also no good, because the values get recalculate inside of other callback...
#     [Input('graph-out', 'children')], # We also changed this, though I think the global change was the effective one. In fact, changing it to watch the graph-1 change messed it up!
# )
# # Uh oh, this ran first... Fixed with global -- and new, alpha callback.
# def on_change(val):
#     global current_lines
#     global xs
#
#     # print('LENGTH ', len(xs)) # Yep, this is it, xs are never getting cleared out.
#
#     summed_lines = {
#         'x': list(filter(lambda x: x != 0, xs)), # Haha, well at least the extraneous lines are horizontal now...
#         'y': [0] * len(xs), # Neat
#         'type': 'line',
#         'name': 'summed',
#         # 'connectgaps': False
#     }
#     # Dot product:
#     dotted_lines = {
#         'x': list(filter(lambda x: x != 0, xs)), # Haha, well at least the extraneous lines are horizontal now...
#         'y': [1] * len(xs), # Neat
#         'type': 'line',
#         'name': 'dotted',
#         # 'connectgaps': False
#     }
#
#     for l in current_lines:
#         for i, val in enumerate(l['y']):
#             summed_lines['y'][i] += val
#             dotted_lines['y'][i] *= val
#
#     # summed_lines['y'] = summed_lines['y'][summed_lines['y'].index(0) : ]
#
#     return dcc.Graph(
#             id = 'whatev2',
#             figure = {
#                 'data': [summed_lines, dotted_lines], # Don't forget this must be an array
#                 'layout': {
#                     'title': 'Summed Waves'
#                 }
#             }
#         )


if __name__ == '__main__':
    app.run_server(debug=True)
