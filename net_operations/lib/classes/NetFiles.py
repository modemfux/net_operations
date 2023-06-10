import os
from net_operations.lib.constants import INITIAL_COMMANDS
from net_operations.lib.funcs import structured_file_to_data
from net_operations.lib.funcs import data_to_structured_file, check_correct_type


class NetFiles:
    def __init__(self):
        config_dir = os.getenv('HOME') + '/.config'
        own_dir = config_dir + '/net_operations'
        state = os.path.exists(own_dir)
        self.logfile = f'{own_dir}/net_operations.log'
        self.userfile = f'{own_dir}/known_users.yaml'
        self.devices = f'{own_dir}/known_devices.yaml'
        self.initial = f'{own_dir}/initial_commands.yaml'
        self._base_inventory = {
            'directories': [config_dir, own_dir],
            'files': {
                'log': {
                    'dst_filename': self.logfile,
                    'coll': '',
                    'format': 'text'},
                'users': {
                    'dst_filename': self.userfile,
                    'coll': {},
                    'format': 'yaml'},
                'devices': {
                    'dst_filename': self.devices,
                    'coll': {},
                    'format': 'yaml'},
                'initial_commands': {
                    'dst_filename': self.initial,
                    'coll': INITIAL_COMMANDS,
                    'format': 'yaml'}}}
        if not state:
            # Check existence of local config directories
            for directory in self._base_inventory['directories']:
                if not os.path.exists(directory):
                    os.mkdir(directory)
            # Check existence of local config files
            for file in self._base_inventory['files'].values():
                if not os.path.exists(file['dst_filename']):
                    data_to_structured_file(**file)
        self.config_dir = own_dir

    def clear_log(self):
        with open(self.logfile, 'w') as f:
            f.write('')

    def reset_known_users(self):
        data_to_structured_file(
            {}, self._base_inventory['files']['users'])

    def reset_known_devices(self):
        data_to_structured_file(
            {}, self._base_inventory['files']['devices'])

    def reset_initial_commands(self):
        data_to_structured_file(
            {}, self._base_inventory['files']['initial_commands'])

    def get_known_devices(self):
        return structured_file_to_data(self.devices)

    def get_known_users(self):
        return structured_file_to_data(self.userfile)

    def get_current_initial_commands(self):
        return structured_file_to_data(self.initial)

    def get_log(self):
        return structured_file_to_data(self.logfile)

    def _update_conf_file(self, filename, new_data, data_type=dict):
        f_dict = {dict: dict.update, list: list.extend}
        check_correct_type(new_data, data_type)
        data = structured_file_to_data(filename)
        if data_type in f_dict.keys():
            f_dict[data_type](data, new_data)
        else:
            data += new_data
        data_to_structured_file(data, filename)
        print(f'{filename} was updated.')

    def update_known_users(self, new_user_data):
        self._update_conf_file(self.userfile, new_user_data)

    def update_known_device(self, new_device_data):
        self._update_conf_file(self.userfile, new_device_data)

    def update_initial_commands(self, new_data):
        self._update_conf_file(self.userfile, new_data)
