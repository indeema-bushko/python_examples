#!/usr/bin/python3
from zeroconf import ServiceBrowser, Zeroconf
from zeroconf_example.storage_interface import StorageInterface
import socket
import json


class ZeroConfListener(object):

    _storage_interface = None

    @classmethod
    def set_storage_interface(cls, storage_interface):
        if storage_interface and isinstance(storage_interface, StorageInterface):
            cls._storage_interface = storage_interface

    @classmethod
    def remove_service(cls, zeroconf, type, name):
        service_info = zeroconf.get_service_info(type, name)
        print ('{} -> Remove Service: {} properties: {}'.format(cls.__name__, name, service_info))
        if cls._storage_interface and isinstance(cls._storage_interface, StorageInterface):
            _service_info_dict = ZeroConfListener.serialize_service_info(service_info)
            cls._storage_interface.remove_service_info(service_info=_service_info_dict)

    @classmethod
    def add_service(cls, zeroconf, type, name):
        service_info = zeroconf.get_service_info(type, name)
        print('{} -> Add service: {}'.format(cls.__name__, service_info))
        if cls._storage_interface and isinstance(cls._storage_interface, StorageInterface):
            _service_info_dict = ZeroConfListener.serialize_service_info(service_info)
            cls._storage_interface.add_service_info(service_info=_service_info_dict)

    @staticmethod
    def serialize_service_info(service_info):
        """
        Convert ServiceInfo object to python dictionary.
        :return:
        """
        if not service_info:
            return None
        _service_info_dict = service_info.__dict__
        _service_info_dict['address'] = socket.inet_ntoa(_service_info_dict['address'])
        _service_info_dict.pop('text', None)

        properties = dict()
        for key, value in service_info.properties.items():
            properties[key.decode('utf-8')] = value.decode('utf-8')
        _service_info_dict['_properties'] = properties
        return _service_info_dict


if __name__ == "__main__":
    print ('ZeroConfListener -> Start listener...')

    zero_conf = Zeroconf()
    zero_conf_listener = ZeroConfListener()
    browser = ServiceBrowser(zero_conf, "_http._tcp.local.", zero_conf_listener)

    try:
        input("Press enter to exit...\n\n")
    finally:
        zero_conf.close()


