import socket
import time
import cpppo
import logging
from cpppo.server.enip import client

plc_ip_address = "192.168.1.137"

timeout = 5.0

logging.basicConfig(**cpppo.log_cfg)

tags = ["Test_DINT[0-3]=(DINT)0,1,2,3"]
while True:
    try:

        with client.connector(host=plc_ip_address, timeout=timeout ) as conn:
            operations = client.parse_operations(tags)
            failures, replies = conn.process(
                operations=operations, timeout=timeout)
        for rpy in replies:
            print(rpy)

    except Exception as exc:
        print("EtherNet/IP I/O Failed: %s" % (exc))
    time.sleep(0.1)
