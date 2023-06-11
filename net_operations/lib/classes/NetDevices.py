import copy
from pprint import pprint
from net_operations.lib.classes.NetFiles import NetFiles


class NetDevices:
    _fs = NetFiles()

    def __init__(self, ip, vendor, **kwargs):
        self.device_ip = ip
        self.device_vendor = vendor.lower()
        self.device = {ip: {'vendor': vendor}}
        if kwargs:
            self.device[ip].update(**kwargs)
        self._fs.update_known_device(self.device)

    def get_device_info(self):
        return self.device[self.device_ip]

    def save_device(self):
        self._fs.update_known_device(self.device)

    def change_device_ip(self, new_ip, save=True):
        new_info = copy.deepcopy(self.get_device_info())
        self.device = {new_ip: new_info}
        self.device_ip = new_ip
        if save:
            self.save_device()

    def update_device_information(self, save=True, **kwargs):
        self.device[self.device_ip].update(**kwargs)
        self.device_vendor = self.device[self.device_ip]['vendor']
        if save:
            self.save_device()

    def get_all_known_devices(self, output=False):
        devices = self._fs.get_known_devices()
        if output:
            pprint(devices)
        return devices

    def get_device_initial_commands(self):
        commands = self._fs.get_current_initial_commands()
        return commands.get(self.device_vendor, None)
