import socket
import time
import sys
from cpppo.server.enip import client


def print_help():
    print('Missing command line arguments:')
    print(' [host] example: host=127.0.0.1, default value is local host')
    print(' (tag_name) example: tag_name=INT')
    print(' (tag_value) example: tag_value=255')
    print(' (tag_name) example: tag_name=Test_DINT, defined by user')


def tag_type_from_string(type_name):
    """
    Convert cpppo type represented as a string int to cpppo type
    :param type_name: BOOL, USINT, SINT, UINT, INT, WORD, UDINT, DWORD, DINT, REAL...
    :return: an integer value
    """
    if 'INT' == type_name:
        return client.enip.INT.tag_type
    elif 'SINT' == type_name:
        return client.enip.SINT.tag_type
    elif type_name == 'DINT':
        return client.enip.DINT.tag_type
    elif 'BOOL' == type_name:
        return client.enip.BOOL.tag_type
    elif 'USINT' == type_name:
        return client.enip.USINT.tag_type
    elif 'DWORD' == type_name:
        return client.enip.DWORD.tag_type
    elif 'REAL' == type_name:
        return client.enip.REAL.tag_type


def value_from_string(value, tag_type):
    """
    Convert command line argument in to real value depend on CIP type
    :param type_name:
    :return:
    """
    if client.enip.INT.tag_type == tag_type or client.enip.SINT.tag_type == tag_type \
            or client.enip.DINT.tag_type == tag_type or client.enip.USINT.tag_type == tag_type:
        return int(value)
    elif client.enip.DINT.tag_type == tag_type:
        return bool(value)
    elif client.enip.DWORD.tag_type == tag_type or client.enip.REAL.tag_type == tag_type:
        return float(value)


def write_tag_value(host, tag_name, type, tag_value, timeout=10.0):
    """
    Write Tag
    :param host: Device host address
    :param tag_name: Tag name, define by user
    :param tag_type: Type of the tag regarding to cpppo library
    :param tag_value: Value to write
    :param timeout: Client response timeout
    :return: True is successfully otherwise False
    """
    print(' - write_tag::write_tag_value: host: {}, tag_name: {}, tag_type: {}, tag_value: {}, timeout: {}'
          .format(host, tag_name, type, tag_value, timeout))
    try:
        with client.connector(host=host, timeout=timeout) as conn:
            data = [tag_value]
            request = conn.write(tag_name, elements=len(data), data=data, tag_type=type)
            reply, ela = client.await(conn, timeout=timeout)
            print(' - reply: {}'.format(reply))
    except AssertionError:
        print(" - Response timed out!! Tearing Connection and Reconnecting!!!!!")
        return False
    except AttributeError:
        print(" - Tag J1_pos not written:::Will try again::")
        return False
    except socket.error as e:
        print(" - Couldn't send command: {}".format(e))
        return False
    return True


if __name__ == '__main__':
    """
    _host - PLC host address
    _port - CIP protocol port,tag default is 44818
    _tag_name - example "Test_DINT[0]"
    _tag_value - depend on tag type
    _tag_type_name - possible value - BOOL, USINT, SINT, UINT, INT, WORD, UDINT, DWORD, DINT, REAL...
    """
    _host = "192.168.1.137"
    _port = 44818
    _tag_name = None
    _tag_value = None
    _tag_type = None
    _timeout = 5.0

    if len(sys.argv) < 2:
        print_help()
        exit(1)

    for i in range(1, len(sys.argv)):
        if 'host=' in sys.argv[i]:
            _host = str(sys.argv[i]).replace('host=', '')
        elif 'tag_name=' in sys.argv[i]:
            _tag_name = str(sys.argv[i]).replace('tag_name=', '')
        elif 'tag_type_name' in sys.argv[i]:
            _tag_type = tag_type_from_string(str(sys.argv[i]).replace('tag_type_name=', ''))
        elif 'tag_value' in sys.argv[i]:
            _tag_value = str(sys.argv[i]).replace('tag_value=', '')

    if not _tag_type or not _tag_name or not _tag_value:
        print_help()
        sys.exit(1)

    value = value_from_string(value=_tag_value, tag_type=_tag_type)

    write_tag_value(host=_host, tag_name=_tag_name, type=_tag_type, tag_value=value)

    print(' - write_tag::main end')

