from confluent_kafka import Producer
import json
import time
import random

# Define the producer
producer = Producer(
    bootstrap_servers='b-1.monstercluster1.6xql65.c3.kafka.eu-west-2.amazonaws.com:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sample store locations and product IDs for our simulation
store_locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio']
products = [f"P{str(i).zfill(5)}" for i in range(1, 101)]  # Product IDs from P00001 to P00100

while True:
    # Simulate a transaction
    transaction = {
        "store_location": random.choice(store_locations),
        "time_of_purchase": str(time.strftime('%Y-%m-%d %H:%M:%S')),  # current time
        "product_ID": random.choice(products),
        "transaction_amount": random.randint(1, 1000) * (-1 if random.random() < 0.05 else 1)  # 5% chance for negative values
    }

    # Send the transaction to our Kafka topic
    producer.send('retail_transactions', value=transaction)

    # Sleep for a random time between 1 to 3 seconds to simulate real-time transaction arrival
    time.sleep(random.uniform(1, 3))
