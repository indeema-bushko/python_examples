#!/usr/bin/env python3

import binascii
import socket
import struct
import signal

# unpacker = struct.Struct('I 2s f')
unpacker = struct.Struct('f f')

sock = None


def signal_handler(sys_signal, frame):
    print('signal_handler: {}'.format(sys_signal))
    if sock:
        sock.close()
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 9999)
    sock.bind(server_address)
    sock.listen(1)

    client_sock, client_address = sock.accept()
    print('Waiting for a connection')

    while True:
        try:
            data = client_sock.recv(unpacker.size)
            print('received {!r}'.format(binascii.hexlify(data)))

            unpacked_data = unpacker.unpack(data)
            print('x: {0:.2f}, y: {0:.2f}'.format(unpacked_data[0], unpacked_data[1]))
        finally:
            pass
