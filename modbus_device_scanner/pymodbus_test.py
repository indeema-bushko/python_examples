from pymodbus.client.sync import ModbusSerialClient, ConnectionException

baud_rate = 19200
stop_bits = 2
parity = 'N'
serial_device = '/dev/ttyUSB0'
modbus_timeout = 1
data_bits = 8


if __name__ == '__main__':
    client = ModbusSerialClient(method='rtu', port=serial_device, timeout=modbus_timeout, bytesize=data_bits,
                                baudrate=baud_rate, stopbits=stop_bits, parity=str(parity))

    try:
        connected = client.connect()
    except ConnectionException as e:
        print('    Error connection: {}'.format(e))

    if connected:
        print ('SUCCESS connected to device: name {}'.format(serial_device))
        try:
            bytes_buffer = client.read_holding_registers(address=0, count=1, unit=7)
            assert (bytes_buffer.function_code < 0x80)
        except Exception as e:
            print ('    Exception: {}'.format(e))

        client.close()

    else:
        print ('FAILED to connect device: name {}'.format(serial_device))