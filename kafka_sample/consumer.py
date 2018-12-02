#!/usr/bin/python3
"""
Kafka Consumer: as simple as possible example implementation of consumer.
"""

from kafka import KafkaConsumer

if __name__ == '__main__':
    print('{} {} '.format(__name__, __doc__))

    consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                             auto_offset_reset='earliest',
                             consumer_timeout_ms=1000)
    consumer.subscribe(['sample'])

    while True:
        for message in consumer:
            print('{}'.format(message))

    consumer.close()
