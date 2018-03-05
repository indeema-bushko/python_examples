import abc
from redis import Redis


class StorageInterface:

    metaclass = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def add_service_info(self, service_info):
        pass

    @abc.abstractmethod
    def remove_service_info(self, service_info):
        pass

    @abc.abstractmethod
    def get_service_list(self):
        return None


class RedisStorageInterface(StorageInterface):

    PORT = 'port'
    HOST = 'host'

    def __init__(self, container='zc', **kwargs):
        self.host = 'localhost'
        self.port = 6379
        self.container = container

        if RedisStorageInterface.PORT in kwargs:
            self.port = int(kwargs[RedisStorageInterface.PORT])
        if RedisStorageInterface.HOST in kwargs:
            self.host = kwargs[RedisStorageInterface.HOST]

        self.redis_connection = Redis(host=self.host, port=self.port, db=0)

    def remove_service_info(self, service_info):
        if self.redis_connection:
            return self.redis_connection.lrem(name=self.container, value=service_info, num=0)
        return None

    def add_service_info(self, service_info):
        if self.redis_connection:
            self.remove_service_info(service_info=service_info)
            return self.redis_connection.rpush(self.container, service_info)
        return None

    def get_service_list(self):
        return None