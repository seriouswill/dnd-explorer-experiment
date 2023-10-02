from confluent_kafka import Consumer, KafkaError

conf = {
    'bootstrap.servers': 'b-1.monstercluster1.6xql65.c3.kafka.eu-west-2.amazonaws.com',  # Replace with your broker URLs
    'group.id': 'your_group_id',
    'auto.offset.reset': 'earliest',
}

consumer = Consumer(conf)

def consume_message():
    consumer.subscribe(['monster_damage'])
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

        print('Received message: {}'.format(msg.value().decode('utf-8')))

consume_message()
consumer.close()