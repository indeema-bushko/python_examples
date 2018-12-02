#!/usr/bin/python3
"""
Kafka Producer: as simple as possible example implementation of producer.
"""

from kafka import KafkaProducer
import time
from array import array

if __name__ == '__main__':
    print('{} {}'.format(__name__, __doc__))

    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    count = 0
    while True:
        msg = 'Message: {}'.format(count)
        producer.send('sample', bytes(msg, 'utf8'))
        time.sleep(5)
        count += 1