#!/usr/bin/python
import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
from pool_filler import filler, most_common
from datetime import datetime
from time import sleep
import logging
log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)
import random



X = deque(maxlen=30)
Y = deque(maxlen=1000)
X.append(datetime.now().strftime('%H:%M'))
Y.append(0)
bucket = [0]
t = 0
counter = 0

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(children='Pool Level'),
    dcc.Graph(id='live-data', animate=False),
    dcc.Interval(
        id='graph-update',
        interval=1000
    )
])

@app.callback(Output('live-data', 'figure'),
            events = [Event('graph-update', 'interval')])

def update_graph():
    global X
    global Y
    global bucket
    global t
    global counter
    
    state, t, bucket, clock = filler(bucket, t)
    if t == 0 and clock != None:
        
        
    
    current_day = datetime.now().strftime('%m-%d')  
    

    
    X.append()
    Y.append(filler_state)
    """
    if counter == 6:
        counter = 0
        f = open('level_hist.txt',"a+")
        f.write('{}: Level Stat: {}\n'.format(datetime.now().strftime('%Y-%m-%d %H:%M'), filler_state))
        f.close()
    else:
        counter += 1
    """
    
    data = go.Bar(
        x = list(),
        y = list(),
        name = 'Level',
        width = 0.5
        
    )
    print(ran_num)
    #return {'data':[data], 'layout': go.Layout(xaxis = dict(range=[min(X), max([len(X)])]),
    #                                           yaxis = dict(range=[min([-1]), max([1])]))}
    #layout = go.Layout()
    #return {'data':trace, 'layout': layout}

    
    return {
        'data': [data], 
        'layout': go.Layout(
            xaxis = dict(
            range=[0,9]
            ),
            yaxis = dict(
                range=[0,9]
            )
        )}
    
"""
def gernerate_table(dataframe, max_rows=200):
    return html.Table(
        # Header
        [html.Tr()]
    )
""" 



if __name__ == '__main__':
    app.run_server(debug=True, host='192.168.7.205')
    