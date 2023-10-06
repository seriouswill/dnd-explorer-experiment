import requests
import pandas as pd
import plotly.express as px
from pyspark.sql import SparkSession
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import json
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Initialize Spark session
spark = SparkSession.builder.appName("MonsterDamageStream").getOrCreate()

cumulative_df = pd.DataFrame(columns=["country", "total_damage"])

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph(n):
    global cumulative_df
    
    # Read from the endpoint
    response = requests.get('http://18.133.251.249:5000/get_messages')
    messages = response.json()

    # Convert each JSON string in the list to a dictionary
    messages_dict_list = [json.loads(msg) for msg in messages]

    # Convert the list of dictionaries to a DataFrame
    df = spark.createDataFrame(pd.DataFrame(messages_dict_list))

    # Sum the damage by country
    grouped_df = df.groupBy("country").agg({"damage": "sum"}).withColumnRenamed("sum(damage)", "total_damage").toPandas()

    # Update the cumulative dataframe
    for index, row in grouped_df.iterrows():
        if row["country"] in cumulative_df["country"].values:
            cumulative_df.loc[cumulative_df["country"] == row["country"], "total_damage"] += row["total_damage"]
        else:
            cumulative_df = pd.concat([cumulative_df, pd.DataFrame([row])], ignore_index=True)

    # Convert 'total_damage' column to float before calling nlargest
    cumulative_df['total_damage'] = cumulative_df['total_damage'].astype(float)

    # Get the top 5 countries by damage
    top_countries = cumulative_df.nlargest(5, 'total_damage')
    
    fig = px.bar(top_countries, x='country', y='total_damage', title='Top 5 Damaged Countries')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
