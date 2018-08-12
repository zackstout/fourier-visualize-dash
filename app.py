
import dash
import numpy as np
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
# from collections import defaultdict

current_lines = []
xs = []

app = dash.Dash(__name__)
server = app.server # Adding for deployment

def makeSlider(id, min, max, step, value):
    return dcc.Slider(id=id, min=min, max=max, step=step, value=value, updatemode='drag')

app.layout = html.Div([
    html.H2('LET\'S GET FOURIER!'),
    # dcc.Input(id='freq-in', value=1, type='int'),
    html.Div([
        html.P('Wave 1 frequency:'),
        makeSlider('w1_freq', 1, 20, 0.5, 1),
        html.P('Wave 1 shift:'),
        makeSlider('w1_shift', 0, 2*np.pi, 0.1, 0),
        html.P('Wave 1 amplitude:'),
        makeSlider('w1_amp', 0, 3, 0.1, 1),
    ]),
    html.Div([
        html.P('Wave 2 frequency:'),
        makeSlider('w2_freq', 0.5, 20, 0.5, 0.5),
        html.P('Wave 2 shift:'),
        makeSlider('w2_shift', 0, 2*np.pi, 0.1, 0),
        html.P('Wave 2 amplitude:'),
        makeSlider('w2_amp', 0, 3, 0.1, 1),
    ]),
    # html.Button('Add to chart', id='btn'),
    html.Div(id='graph-out'),
    html.Div(id='graph2-out'),
    html.Div(id='dummy'),
    html.Canvas(id='canv')
])


# OK not sure what fixed this, but this is no longer needed:
# Band-aid fix for not really grokking async stuff here:
# And even still, we're depending on the other callbacks running in the right order:
# @app.callback(
#     Output('dummy', 'children'),
#     [Input('w1_freq', 'value'), Input('w1_shift', 'value'), Input('w2_freq', 'value'), Input('w2_shift', 'value')],
# )
# def on_change(val1, val2, val3, val4):
#     return html.P(val1)





# Update the first chart:
@app.callback(
    Output('graph-out','children'),
    [Input('w1_freq', 'value'), Input('w1_shift', 'value'), Input('w1_amp', 'value'), Input('w2_freq', 'value'), Input('w2_shift', 'value'), Input('w2_amp', 'value')],
)
def on_click(w1_freq, w1_shift, w1_amp, w2_freq, w2_shift, w2_amp):
    w = 10
    n = 500 # Controls the resolution
    ys = []
    y2s = []
    global xs

    xs = []

    for x in range(n):
        xs.append(x * w / n)
        ys.append(w1_amp * np.sin(w1_freq * x * w / n + w1_shift))
        y2s.append(w2_amp * np.sin(w2_freq * x * w / n + w2_shift)) # Wow, it automatically gives them different colors!

    global current_lines # Huh, we have to say 'global' here *and* when we read it..
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

    # Summed wave:
    summed_lines = {
        'x': xs,
        'y': [0] * len(xs), # Neat
        'type': 'line',
        'name': 'summed',
    }
    # Dot product:
    dotted_lines = {
        'x': xs,
        'y': [1] * len(xs),
        'type': 'line',
        'name': 'dotted',
    }

    for l in current_lines:
        for i, val in enumerate(l['y']):
            summed_lines['y'][i] += val
            dotted_lines['y'][i] *= val

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
