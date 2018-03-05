#!/usr/bin/python

import logging
import socket
import sys
from time import sleep

from zeroconf import ServiceInfo, Zeroconf

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    # add custom properties
    port = 12345
    service = 'MyService'
    properties = {'ip_address': '8.8.8.8'}

    info = ServiceInfo(type_="_http._tcp.local.",
                       name="Service name._http._tcp.local.",
                       address=socket.inet_aton("127.0.0.1"),
                       port=port,
                       weight=0,
                       priority=0,
                       properties=properties)

    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf = Zeroconf()
    zeroconf.register_service(info)
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()

