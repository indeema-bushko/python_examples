#!/usr/bin/env python3

import socket
import struct
import binascii
import time
import sys
import signal


sock = None


def signal_handler(sys_signal, frame):
    print('signal_handler: {}'.format(sys_signal))
    if sock:
        sock.close()
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    packer = struct.Struct('f f')

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 9999)

    while True:
        print('Start Loop... ');
        print('Waiting connection to the server ... {}'.format(server_address))
        connected = False
        while not connected:
            try:
                sock.connect(server_address)
                connected = True
            except Exception as e:
                pass

        print('Successfully connected to server ...')
        data_x = 0.0
        data_y = 0.0
        while True:
            data = (data_x, data_y)
            try:
                sock.sendall(packer.pack(*data))
                data_x += 0.01
                data_y += 0.01
                time.sleep(5)
                print('x: {0:.2f}, y: {0:.2f}'.format(data_x, data_y))
            except Exception as e:
                print(e)
                break


