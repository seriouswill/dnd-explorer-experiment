from flask import Flask, jsonify
from confluent_kafka import Consumer, KafkaError

app = Flask(__name__)

conf = {
    'bootstrap.servers': 'b-1.monstercluster1.6xql65.c3.kafka.eu-west-2.amazonaws.com:9092',
    'group.id': 'your_group_id',
    'auto.offset.reset': 'earliest',
}
consumer = Consumer(conf)
consumer.subscribe(['monster-damage'])

@app.route('/get_messages', methods=['GET'])
def get_messages():
    messages = []
    
    for _ in range(10):  # Fetch 10 messages per request, adjust as necessary
        msg = consumer.poll(1.0)
        if msg is None:
            break
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                return jsonify({'error': str(msg.error())}), 500
        messages.append(msg.value().decode('utf-8'))
    
    return jsonify(messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
