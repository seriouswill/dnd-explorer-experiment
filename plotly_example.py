from confluent_kafka import Consumer, KafkaError
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import json
from dash.dependencies import Output, Input

# Kafka Configuration
conf = {
    'bootstrap.servers': 'b-1.monstercluster1.6xql65.c3.kafka.eu-west-2.amazonaws.com:9092',
    'group.id': 'your_group_id',
    'auto.offset.reset': 'earliest',
}

consumer = Consumer(conf)
consumer.subscribe(['monster-damage'])

# Dash Configuration
app = dash.Dash(__name__, external_stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"])

app.layout = html.Div([
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(
        id='graph-update',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    ),
])

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph(n):
    global consumer

    messages_list = []
    for _ in range(10):  # Collect 10 messages
        msg = consumer.poll(1.0)
        if msg is not None and not msg.error():
            structured_msg = json.loads(msg.value().decode('utf-8'))
            messages_list.append(structured_msg)

    countries = [entry['country'] for entry in messages_list]
    percent_losses = [entry['percent_loss'] for entry in messages_list]

    fig = go.Figure(data=[go.Bar(x=countries, y=percent_losses)])
    fig.update_layout(title='Percent Population Loss by Country',
                      xaxis=dict(title='Country'),
                      yaxis=dict(title='Percent Loss'))
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
