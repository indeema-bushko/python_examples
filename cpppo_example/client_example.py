from __future__ import print_function
from cpppo.server.enip import client
import time

host = "192.168.1.137"
tags = [ "Test_DINT[0-0]" ]

# with client.connector( host=host ) as conn:
#     for index,descr,op,reply,status,value in conn.pipeline(
#             operations=client.parse_operations( tags ), depth=2 ):
#         print( "%s: %20s: %s" % ( time.ctime(), descr, value ))
#
# with client.connector(host=host) as conn:
#     req = conn.write("Test_DINT[0]", data=[255])
#     assert conn.readable(timeout=1.0), "Failed to receive reply"
#     req = next(conn)


timeout = 5.0

with client.connector(host=host) as conn:
    while True:
        try:
            data = [22, 33, 44]
            req = conn.write("Tset_DINT",elements=len(data), data=data, tag_type=client.enip.DINT.tag_type)

            rpy, ela = client.await(conn, timeout=timeout)
            print('reply : {}'.format(rpy))
        except AssertionError:
            print
            "Response timed out!! Tearing Connection and Reconnecting!!!!!"
            break
        except AttributeError:
            print
            "Tag J1_pos not written:::Will try again::"
            break