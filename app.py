
import dash
import numpy as np
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
# from collections import defaultdict
import plotly.graph_objs as go

current_lines = []
xs = []
angle = 0

# NOTE: Dash runs in threads. So callbacks should not modify global variables, or they could get threads out of sync.

app = dash.Dash(__name__)
server = app.server # Adding for deployment


external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css", ]
for css in external_css:
    app.css.append_css({"external_url": css})

def makeSlider(id, min, max, step, value):
    return dcc.Slider(id=id, min=min, max=max, step=step, value=value, updatemode='drag')

ratio = 5

app.layout = html.Div([
    html.H2('LET\'S GET FOURIER!'),
    # dcc.Input(id='freq-in', value=1, type='int'),
    html.Div([
        html.Div([
            html.P('Wave 1 frequency:'),
            makeSlider('w1_freq', 1, 20, 0.5, ratio),
            html.P('Wave 1 shift:'),
            makeSlider('w1_shift', 0, 2*np.pi, 0.1, 0),
            html.P('Wave 1 amplitude:'),
            makeSlider('w1_amp', 0, 3, 0.1, 1),
        ], className="col-md-6 slides"),
        html.Div([
            html.P('Wave 2 frequency:'),
            makeSlider('w2_freq', 0.5, 20, 0.5, ratio * 2 ** (12/12)), # This should represent the perfect fifth.
            html.P('Wave 2 shift:'),
            makeSlider('w2_shift', 0, 2*np.pi, 0.1, 0),
            html.P('Wave 2 amplitude:'),
            makeSlider('w2_amp', 0, 3, 0.1, 1),
        ], className="col-md-6 slides")
    ], className="row"),
    # html.Button('Add to chart', id='btn'),
    html.Div(id='graph-out'),
    html.Div(id='graph2-out'),
    # html.Canvas(id='canv'),
    # dcc.Graph(id='live-graph', animate=True),
    # dcc.Interval(
    #     id='graph-update',
    #     interval=60
    # ),
])


# @app.callback(
#     Output('live-graph', 'figure'),
#     events=[Event('graph-update', 'interval')]
# )
# def update_live_graph():
#     # X.append(X[-1]+1)
#     # Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))
#     global angle
#     angle += 0.1
#     xs = np.linspace(0,5,50)
#     ys = np.linspace(0,5,50)
#     new_xs = [x * np.cos(angle) for x in xs]
#     new_ys = [y * np.sin(angle) for y in ys]
#
#     # Create the graph:
#     data = go.Line(
#         x=new_xs,
#         y=new_ys,
#         name='line',
#         # mode='lines+markers'
#     )
#
#     layout = go.Layout(
#     xaxis=dict(
#         range=[-5, 5]
#     ),
#     yaxis=dict(
#         range=[-5, 5]
#     )
#     )
#
#     # Send back the figure to our live-graph
#     return {'data': [data], 'layout': layout}




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
