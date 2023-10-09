import requests
import pandas as pd
import plotly.express as px
from pyspark.sql import SparkSession
import json
import time
from IPython.display import clear_output

# Initialize Spark session
spark = SparkSession.builder.appName("MonsterDamageStream").getOrCreate()

# Initialize a DataFrame to store cumulative damages
cumulative_df = pd.DataFrame(columns=['country', 'total_damage'])
cumulative_df.set_index('country', inplace=True)

def fetch_and_update():
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
    grouped_df.set_index('country', inplace=True)

    # Update the cumulative damages
    for country, row in grouped_df.iterrows():
        if country in cumulative_df.index:
            cumulative_df.loc[country, 'total_damage'] += row['total_damage']
        else:
            cumulative_df.loc[country, 'total_damage'] = row['total_damage']
    
    # Sort by damage and take the top 7
    top_countries = cumulative_df.sort_values('total_damage', ascending=False).head(7)

    # Use Plotly Express for plotting
    fig = px.bar(top_countries, x=top_countries.index, y='total_damage', title='Top 7 Most Damaged Countries')
    fig.show()

while True:
    clear_output(wait=True)  # Clear the previous chart
    fetch_and_update()  # Fetch, update, and plot the new data
    time.sleep(10)  # Wait for 10 seconds before the next iteration
