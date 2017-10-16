from pymodbus.client.sync import ModbusSerialClient, ConnectionException
import glob
import json


def modbus_rtu_device_scanner(serial_devices=['/dev/ttyUSB0'], baud_rates=[9600, 19200]):
    """
    Scan list of serial devices on every possible configurations of speed (baud rate),
    parity and stop bits, to looking for modbus devices. by scanning range
    of possible ID's in range 1..247

    :param serial_devices: list of serial ports name {ttyUSB0, ttyUSB1, ttyUSBx}
    :param baud_rates: list of available baud rates (port speed)
    :return: list of serial ports configuration like {method, port, baudrate, bytesize, parity, stopbits. timeout, modbus_ids[]}
    and list with ID's of founded modbus devices in range 1..247.
    """
    serial_device_config_list = {}

    modbus_timeout = 1

    for serial_device in serial_devices:
        for baud_rate in baud_rates:
            for parity in ['N', 'E', 'O']:
                serial_device_config = {}
                data_bits = 8
                stop_bits = 2 if parity == 'N' else 1

                # Save current scanned serial port configuration.
                serial_device_config.update({
                    'method': 'rtu',
                    'port': str(serial_device),
                    'baudrate': baud_rate,
                    'parity': str(parity),
                    'bytesize': data_bits,
                    'stopbit': stop_bits,
                    'timeout': modbus_timeout
                })

                print ('Scan serial device: {}'.format(serial_device_config))

                client = ModbusSerialClient(method='rtu', port=str(serial_device), timeout=modbus_timeout, bytesize=data_bits,
                                            baudrate=baud_rate, stopbits=stop_bits, parity=str(parity))

                modbus_devices_id = []

                try:
                    connected = client.connect()
                except ConnectionException as e:
                    print('    Error connection: {}'.format(e))

                if connected:
                    print ('SUCCESS connected to device: name {}'.format(serial_device))
                    for i in range(1, 248):
                        try:
                            bytes_buffer = client.read_holding_registers(address=0, count=1, unit=i)
                            assert (bytes_buffer.function_code < 0x80)
                            modbus_devices_id.append(i)
                            print ('    Found modbus device with ID: {}, read bytes: {}'.format(i, bytes_buffer))
                        except Exception as e:
                            print ('    Except id: {}, exception: {}'.format(i, e))

                        client.close()

                    if bool(modbus_devices_id):
                        serial_device_config.update({'modbus_ids': modbus_devices_id})
                        serial_device_config_list.update({str(serial_device): serial_device_config})

                else:
                    print ('FAILED to connect device: name {}'.format(serial_device))
                    continue

    return json.dumps(serial_device_config_list)


if __name__ == '__main__':
    serial_devices = glob.glob('/dev/ttyUSB[0-9]*')
    print ('Device names : ' + str(serial_devices))
    # modbus_rtu_device_scanner(serial_devices=serial_devices)
    print('Result: ' + str(modbus_rtu_device_scanner()))


