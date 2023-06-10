import re
import os
import logging
import paramiko
import getpass
import time
import telnetlib
from net_operations.lib.constants import INITIAL_COMMANDS
from net_operations.lib.funcs import get_user_credentials
from net_operations.lib.funcs import work_with_script_folder
from net_operations.lib.funcs import encrypt_password, decrypt_password
from net_operations.lib.funcs import structured_file_to_data, get_known_data
from net_operations.lib.funcs import data_to_structured_file


# Logging config
own_folder = work_with_script_folder()
logfile = own_folder + '/net_operations.log'
own_logger = logging.getLogger(__name__)
own_logger.setLevel(logging.INFO)
own_handler = logging.FileHandler(logfile, mode='a')
own_format = logging.Formatter("%(asctime)s >> %(levelname)s: %(message)s")
own_handler.setFormatter(own_format)
own_logger.addHandler(own_handler)


class NetFiles:
    def __init__(self):
        config_dir = os.getenv('HOME') + '/.config/'
        own_dir = config_dir + 'net_operations'
        state = os.path.exists(own_dir)
        if not state:
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
        data_to_structured_file(self._base_inventory['files']['users'])

    def reset_known_devices(self):
        data_to_structured_file(self._base_inventory['files']['devices'])

    def reset_initial_commands(self):
        data_to_structured_file(
            self._base_inventory['files']['initial_commands'])

    def get_known_devices(self):
        return structured_file_to_data(self.devices)

    def get_known_users(self):
        return structured_file_to_data(self.userfile)

    def get_current_initial_commands(self):
        return structured_file_to_data(self.initial)

    def update_known_users(self, new_user_data):
        if not isinstance(new_user_data, dict):
            err_type = str(type(new_user_data))
            raise TypeError(f'This is not dict, but {err_type}')
        data = self.get_known_users()
        data.update(new_user_data)
        data_to_structured_file(data)
        print(f'{self.userfile} was updated.')

    def update_known_device(self, new_device_data):
        if not isinstance(new_device_data, dict):
            err_type = str(type(new_device_data))
            raise TypeError(f'This is not dict, but {err_type}')
        data = self.get_known_devices()
        data.update(new_device_data)
        data_to_structured_file(data)
        print(f'{self.devices} was updated.')

    def update_initial_commands(self, new_data):
        if not isinstance(new_data, dict):
            err_type = str(type(new_data))
            raise TypeError(f'This is not dict, but {err_type}')
        data = self.get_known_users()
        data.update(new_data)
        data_to_structured_file(data)
        print(f'{self.devices} was updated.')


# Class for user's credential operations
class NetUser:
    def __init__(self, username=None, password=None):
        if any((not username, not password)):
            username, password = get_user_credentials()
        self.username = username
        self._key, self.password = encrypt_password(password)

    def get_unenc_password(self):
        return decrypt_password(self._key, self.password)

    def update_password(self, new_pass=None):
        if not new_pass:
            new_pass = getpass.getpass('Enter your new password: ')
        self._key, self.password = encrypt_password(new_pass)

    def save_user(self):
        user_dict = {self.username: {'key': self._key,
                                     'password': self.password}}
        filename = work_with_script_folder() + '/known_users.yaml'
        if os.path.exists(filename):
            data = structured_file_to_data(filename)
        else:
            data = {}
        data.update(user_dict)
        data_to_structured_file(data, filename)


# Class for device management
class NetDevice:
    _dir = NetFiles()
    devices = _dir.get_known_devices()

    def __init__(self, ip, vendor):
        self.ip = ip
        self.vendor = vendor
        self.device = {self.ip: {'vendor': self.vendor}}


class NetworkOperations:
    # Base section
    _known_devices = get_known_data('known_devices.yaml')
    _conn = None
    _ssh_failed = False
    _telnet_failed = False
    _vendors = {
        'huawei': ['screen-length 0 temporary', 'screen-width 512', 'Y'],
        'cisco': ['terminal length 0', 'terminal width 512']
    }

    def get_known_devices(self):
        self._known_devices = get_known_data('known_devices.yaml')

    def save_known_devices(self, filepath='default'):
        if filepath == 'default':
            filepath = work_with_script_folder() + '/' + 'known_devices.yaml'
        data_to_structured_file(self._known_devices, filepath)
        own_logger.info(f'{filepath} updated.')

    def get_known_user_information(self, name, filepath='default'):
        if filepath == 'default':
            filepath = work_with_script_folder() + '/' + 'known_users.yaml'
        data = structured_file_to_data(filepath)
        return data.get(name, None) if data else None

    def get_known_device_information(self, ip):
        return self._known_devices.get(ip, None)

    def __init__(self, ip, username=None,
                 password=None, vendor=None, conn_type='ssh'):
        vendors = ['cisco', 'huawei']
        questions = {
            'vendor': f'Укажите вендора из списка поддерживаемых {vendors}: ',
            'conn_type': 'Укажите тип подключения (SSH, Telnet): '}
        self.ip = ip
        saved_credentials = self.get_known_user_information(username)
        self.device = {self.ip: {'vendor': vendor.lower(),
                                 'conn_type': conn_type}}
        for key, value in self.device.items():
            if value is None:
                question = questions[key]
                self.device[key] = input(f'{question}').lower()
        if saved_credentials:
            print(f'Найдены сохраненные данные о пользователе {username}.')
            choice = input('Вы хотите их использовать? [Y/n]: ').lower()
            if choice in ['', 'y']:
                key = saved_credentials['key']
                password = saved_credentials['password']
                password = decrypt_password(key, password)
            else:
                username, password = get_user_credentials()
        else:
            username, password = get_user_credentials()
        user_data = {'username': username, 'password': password}
        # create NetUser instance with our user credentials, write them to file
        self.user = NetUser(**user_data)
        self.user.save_user()
        own_logger.info(f'User\'s {username} credentials added to known_users')
        # Update information about known devices
        self._known_devices.update(self.device)
        self.save_known_devices()

# SSH Connection methods section
    def establish_ssh_connection(self):

        password = self.user.get_unenc_password()
        username = self.user.username
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
        try:
            client.connect(
                hostname=self.ip,
                username=username,
                password=password,
                timeout=30.0)
            connection_state = True
        except Exception as error:
            own_logger.error(f'Some error occured while connecting '
                             f'to {self.ip} via SSH. Error is: {error}')
            self._ssh_failed = True
            raise Exception(error)
        if connection_state:
            try:
                self.connection = client.invoke_shell(width=256)
                self.connection.send('\r\n')
                output = self.connection.recv(20000)
                output = output.decode().replace('\r\n', '\n')
                self.prompt = output.split('\n')[-1]
                own_logger.info(f'Connection to {self.ip} via SSH established.')
                print(f'Connection to {self.ip} via SSH established.')
                self._conn = 'ssh'
            except Exception as error:
                self._ssh_failed = True
                own_logger.error(f"There are some problems "
                                 f"with connection to {self.ip}. "
                                 "Check device's parameters.")
                raise Exception(error)

    def send_ssh_command(self, command, waittime=1, recv_val=20000):
        for_send = (command + '\n').encode()
        self.connection.send(for_send)
        time.sleep(waittime)
        result = self.connection.recv(recv_val)
        result = result.decode().replace('\r\n', '\n')
        self.prompt = result.split('\n')[-1]
        own_logger.info(f'Command {command} executed on device {self.ip}')
        return result

    def send_ssh_commands(self, commands_list, waittime=1, recv_val=20000):
        if not isinstance(commands_list, list):
            commands_list = [commands_list]
        output = ''
        for command in commands_list:
            output += self.send_ssh_command(command, waittime, recv_val)
        return output

    def ssh_close(self):
        self.connection.close()
        own_logger.info(f'SSH connection to {self.ip} is closed.')
        print(f'SSH connection to {self.ip} is closed.')

# Telnet Connection methods section
    def establish_telnet_connection(self):
        password = self.user.get_unenc_password()
        username = self.user.username
        reg_login = [b'[Uu]ser.*[Nn]ame', b'[Ll]ogin']
        reg_password = [b'[Pp]ass.*[Ww]ord']
        reg_prompt = [b'[>#]', b']']
        reg_wrong = r'([Ee]rror|[Ww]rong|[Ii]nvalid)'

        def to_bytes(func):
            def inner(arg):
                res_arg = str(arg) + '\n'
                return func(res_arg.encode())
            return inner

        try:
            output = ''
            self.connection = telnetlib.Telnet(self.ip)
            self.connection.write = to_bytes(self.connection.write)
            out_login = self.connection.expect(reg_login)
            output += out_login[-1].decode()
            self.connection.write(username)
            out_password = self.connection.expect(reg_password)
            output += out_password[-1].decode()
            self.connection.write(password)
            time.sleep(5)
            output += self.connection.read_very_eager().decode()
            if re.search(reg_wrong, output):
                err_message = f'Wrong login or password for device {self.ip}.'
                own_logger.error(err_message)
                raise Exception(err_message)
            self.connection.write('')
            out_prompt = self.connection.expect(reg_prompt)
            output += out_prompt[-1].decode()
            output = output.replace('\r\n', '\n')
            self.prompt = output.split('\n')[-1]
            own_logger.info(f'Connection to {self.ip} via Telnet established')
            print(f'Connection to {self.ip} via Telnet established')
            self._conn = 'telnet'
        except Exception as error:
            own_logger.error(f'Some error occured while connecting via Telnet'
                             f'to {self.ip}. Error is: {error}')
            raise Exception(error)

    def send_telnet_command(self, command, waittime=1):
        self.connection.write(command)
        time.sleep(waittime)
        result = self.connection.read_very_eager().decode()
        result = result.replace('\r\n', '\n')
        self.prompt = result.split('\n')[-1]
        own_logger.info(f'Command {command} executed on device {self.ip}')
        return result

    def send_telnet_commands(self, commands_list):
        if not isinstance(commands_list, list):
            commands_list = [commands_list]
        output = ''
        for command in commands_list:
            output += self.send_telnet_command(command)
        return output

    def telnet_close(self):
        self.connection.close()
        own_logger.info(f'Telnet connection to {self.ip} is closed.')
        print(f'Telnet connection to {self.ip} is closed.')
        self._conn = None

    # Universal methods
    def establish_connection(self):
        vendor = self.device[self.ip]['vendor']
        try:
            self.establish_ssh_connection()
            self.connection_state = True
        except Exception as error:
            message = f'SSH connection to {self.ip} is unavailable now.'
            own_logger.error(message)
            own_logger.error(f'SSH failed due to:\n{error}')
            print(message)
            try:
                self.establish_telnet_connection()
                self.connection_state = True
            except Exception as error:
                message = f'Telnet connection to {self.ip} is unavailable now.'
                own_logger.error(message)
                print(message)
                own_logger.error(f'Telnet failed due to:\n{error}')
                raise Exception(error)
        if self.connection_state and vendor in self._vendors:
            self.send_commands(self._vendors[vendor])

    def close(self):
        self.connection.close()
        own_logger.info(f'Connection to {self.ip} is closed.')
        print(f'Connection to {self.ip} is closed.')
        self._conn = None

    def send_commands(self, *args, **kwargs):
        commands_func_dict = {'telnet': self.send_telnet_commands,
                              'ssh': self.send_ssh_commands}
        return commands_func_dict[self._conn](*args, **kwargs)

    def send_config_commands(self, *args, **kwargs):
        output = self.enter_config_mode()
        output = self.send_commands(*args, **kwargs)
        output += self.exit_config_mode()
        return output

    def enable_pagination(self, lines=48, quiet=False):
        lines = str(lines)
        vendor = {'huawei': ['return', f'screen-length {lines} temporary'],
                  'cisco': ['end', f'terminal length {lines}']}
        commands = vendor[self.device[self.ip]['vendor']]
        output = self.send_commands(commands)
        if not quiet:
            return output

    def disable_pagination(self, quiet=False):
        vendor = {'huawei': ['return', 'screen-length 0 temporary'],
                  'cisco': ['end', 'terminal length 0']}
        commands = vendor[self.device[self.ip]['vendor']]
        output = self.send_commands(commands)
        if not quiet:
            return output

    def enter_config_mode(self, quiet=False):
        vendor = {'huawei': ['return', 'system-view'],
                  'cisco': ['end', 'configure terminal']}
        commands = vendor[self.device[self.ip]['vendor']]
        output = self.send_commands(commands)
        if not quiet:
            return output

    def exit_config_mode(self, quiet=False):
        vendor = {'huawei': ['return'],
                  'cisco': ['end']}
        commands = vendor[self.device[self.ip]['vendor']]
        output = self.send_commands(commands)
        if not quiet:
            return output

# Context manager's function
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()
        own_logger.info(f'Connection to {self.ip} is closed.')
        print(f'Connection to {self.ip} is closed.')
        self._conn = None
