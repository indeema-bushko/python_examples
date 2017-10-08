#!/usr/bin/python

from zeroconf import ServiceBrowser, Zeroconf


class ZeroConfListener(object):

    zeroconf_instance = None

    def __init__(self):
        if not self.zeroconf_instance:
            self.zeroconf_instance = Zeroconf();

        self.service_browser = ServiceBrowser(self.zeroconf_instance, "_http._tcp.local.", self)

    def remove_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print ("Remove Service: {0} properties: {1}".format(name, info))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Add Service: {0} properties: {1}".format(name, info))

    def close(self):
        if not self.zeroconf_instance:
            self.zeroconf_instance.close()


if __name__ == "__main__":
    print ('Start ZeroConfListener listener...')
    zero_conf_listener = ZeroConfListener()
    try:
        input("Press enter to exit...\n\n")
    finally:
        zero_conf_listener.close()


