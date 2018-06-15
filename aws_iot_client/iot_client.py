#!/usr/bin/python3

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import signal
import sys
from subprocess import call, PIPE, check_output
import random

from aws_iot_client.aws_iot_config import *


def custom_callback(client, userdata, message):
    print("- custom_callback: client: {}, userData: {}, message: {}".format(client, userdata, message))


def custom_message_callback(message):
    print('- customMessageCallback: topic: {}, payload: {}'.format(message.topic, message.payload))


def ack_callback(mid, data):
    pass
    # print('- ack_callback: mid: {}, data: {}\n'.format(mid, data))


def custom_pub_ack_callback(mid):
    print("\nReceived packet id: {}".format(mid))


def exit_handler(sys_signal, frame):
    sys.exit(0)


def get_machine_unique_id():
    cmd = 'dmidecode -t 4 | grep ID | sed \'s/.*ID://;s/ //g\''
    return check_output('echo TempPass123 | sudo -S {}'.format(cmd), shell=True).decode('utf-8')


if __name__ == '__main__':
    print('\nAWS IoT Client...')
    print(' - root CA pem file: {}'.format(root_ca_file))
    print(' - cert pem file : {}'.format(cert_file))
    print(' - key pem file : {}'.format(key_file))
    print(' - aws iot host : {}'.format(aws_iot_host))
    print(' - aws iot thing : {}'.format(aws_iot_thing_name))
    print(' - aws client id: {}'.format(aws_iot_client_id))

    # Handle Sys exit signal.
    signal.signal(signalnum=signal.SIGINT, handler=exit_handler)

    iot_client = None

    # Initialize AWS IoT client
    iot_client = AWSIoTMQTTClient(clientID=aws_iot_client_id)
    iot_client.configureEndpoint(hostName=aws_iot_host, portNumber=aws_iot_port)
    iot_client.configureCredentials(CAFilePath=root_ca_file, KeyPath=key_file, CertificatePath=cert_file)

    # Infinite offline Publish queueing
    iot_client.configureOfflinePublishQueueing(-1)

    # Draining 2 Hz
    iot_client.configureDrainingFrequency(2)

    # Connection/Disconnection time out seconds
    iot_client.configureConnectDisconnectTimeout(10)

    # MQTT Operation time out seconds
    iot_client.configureMQTTOperationTimeout(5)
    iot_client.onMessage = custom_message_callback

    iot_client.connect()
    iot_client.subscribeAsync(topic='testTopic/testMessage', QoS=1, ackCallback=ack_callback,
                              messageCallback=custom_callback)

    print('\nUID: {}'.format(get_machine_unique_id()))
    print('\n')
    count = 0
    while True:
        msg = input('Device Power Consumption (W) : ')
        if msg is not None:
            if msg == 'exit':
                break
            else:
                iot_client.publishAsync('sensor_1/temperature', str(msg), 1, ackCallback=custom_pub_ack_callback)
                count += 1
        time.sleep(2)

