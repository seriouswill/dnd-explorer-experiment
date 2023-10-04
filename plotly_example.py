from confluent_kafka import Consumer, KafkaError
import plotly.graph_objs as go
import json

conf = {
    'bootstrap.servers': 'b-1.monstercluster1.6xql65.c3.kafka.eu-west-2.amazonaws.com:9092',  # Replace with your broker URLs
    'group.id': 'your_group_id',
    'auto.offset.reset': 'earliest',
}

consumer = Consumer(conf)

# List to collect structured messages
messages_list = []

def consume_message():
    consumer.subscribe(['monster-damage'])
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        # Convert message from JSON string to dictionary
        structured_msg = json.loads(msg.value().decode('utf-8'))
        messages_list.append(structured_msg)

        # Display updated visualization every 10 messages
        if len(messages_list) % 10 == 0:
            visualize_data()

def visualize_data():
    countries = [entry['country'] for entry in messages_list]
    percent_losses = [entry['percent_loss'] for entry in messages_list]

    fig = go.Figure(data=[go.Bar(x=countries, y=percent_losses)])
    fig.update_layout(title='Percent Population Loss by Country', 
                      xaxis=dict(title='Country'),
                      yaxis=dict(title='Percent Loss'))
    fig.show()

consume_message()
consumer.close()
