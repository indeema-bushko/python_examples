from zeroconf_example.service_listener import ZeroConfListener
from zeroconf_example.storage_interface import StorageInterface, RedisStorageInterface
from zeroconf import Zeroconf, ServiceBrowser, ServiceInfo
import socket
import json


class ZeroConfServiceManager(object):

    SERVICE_UNIQUE_ID = 'unique_id'
    SERVICE_NAME = 'name'
    ADDRESS = 'host'
    PORT = 'port'
    WEIGHT = 'weight'
    PRIORITY = 'priority'

    _zero_conf = Zeroconf()
    _zero_conf_listener = None
    _zero_conf_browser = None
    _service_info = None

    _service_name = 'ecobox'
    _address = '127.0.0.1'
    _port = 12345
    _weight = 0
    _priority = 0

    _storage_interface = None

    def __init__(self):
        pass

    @classmethod
    def configure_service(cls, **kwargs):

        if ZeroConfServiceManager.SERVICE_NAME in kwargs:
            cls._service_name = kwargs[ZeroConfServiceManager.SERVICE_NAME]
        if ZeroConfServiceManager.ADDRESS in kwargs:
            cls._address = kwargs[ZeroConfServiceManager.ADDRESS]
        if ZeroConfServiceManager.PORT in kwargs:
            cls._port = kwargs[ZeroConfServiceManager.PORT]
        if ZeroConfServiceManager.WEIGHT in kwargs:
            cls._weight = kwargs[ZeroConfServiceManager.WEIGHT]
        if ZeroConfServiceManager.PRIORITY in kwargs:
            cls._priority = kwargs[ZeroConfServiceManager.PRIORITY]

    @classmethod
    def start_service(cls, property_list=dict()):
        """
        Initialize ZeroConf service set.
        Set callback listener.
        Start service browser.
        Register service.
        Add storage interface implementation to save service in to REDIS db.
        :return:
        """
        cls._zero_conf = Zeroconf()

        # Initialise ZeroConf listener, start browsing for service.
        cls._zero_conf_listener = ZeroConfListener()
        cls._zero_conf_browser = ServiceBrowser(cls._zero_conf, '_http._tcp.local.', cls._zero_conf_listener) #_test._tcp

        # Set storage interface for ZeroConf listener.
        # An implementation of storage interface based on Redis db.
        cls._storage_interface = RedisStorageInterface()
        cls._zero_conf_listener.set_storage_interface(cls._storage_interface)

        # Service registration.
        # _service_info = ServiceInfo(type_="_http._tcp.local.",
        #                             name="{}._http._tcp.local.".format(cls._service_name),
        #                             address=socket.inet_aton(cls._address),
        #                             port=cls._port,
        #                             weight=0,
        #                             priority=0,
        #                             properties=property_list)
        #
        # cls._zero_conf.register_service(_service_info)
        # cls._service_info = cls._zero_conf.get_service_info(type_=_service_info.type, name=_service_info.name)

    @classmethod
    def stop_service(cls):
        """
        Unregister all services, close Zeroconf.
        :return:
        """
        if cls._zero_conf and isinstance(cls._zero_conf, Zeroconf):
            cls._zero_conf.unregister_all_services()
            cls._zero_conf_listener = None
            cls._zero_conf.close()
        if cls._storage_interface and isinstance(cls._storage_interface, StorageInterface):
            if cls._service_info:
                _service_info_dict = ZeroConfListener.serialize_service_info(cls._service_info)
                cls._storage_interface.remove_service_info(_service_info_dict)

    @classmethod
    def get_service_info(cls):
        return cls._service_info

    @classmethod
    def get_services_list(cls):
        if isinstance(cls._storage_interface, StorageInterface):
            return cls._storage_interface.get_service_list()
        return None


if __name__ == "__main__":

    properties = dict()
    properties['my_custom_property'] = 'my-custom-value'

    config = dict()
    config[ZeroConfServiceManager.SERVICE_NAME] = 'cool_service'
    config[ZeroConfServiceManager.ADDRESS] = "127.0.0.1"
    config[ZeroConfServiceManager.PORT] = 12345
    config[ZeroConfServiceManager.PRIORITY] = 0
    config[ZeroConfServiceManager.WEIGHT] = 0

    ZeroConfServiceManager.configure_service(**config)
    ZeroConfServiceManager.start_service(property_list=properties)

    try:
        input("Press enter to exit...\n")
    finally:
        ZeroConfServiceManager.stop_service()
