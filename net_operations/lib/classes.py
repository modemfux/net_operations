import os
import logging
import paramiko
import getpass
import time
from Exscript import Account
from Exscript.protocols import Telnet
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
                own_logger.info(f'Connection to {self.ip} via SSH established.')
                print(f'Connection to {self.ip} via SSH established.')
                self._conn = 'ssh'
            except Exception:
                self._ssh_failed = True
                own_logger.error(f"There are some problems "
                                 f"with connection to {self.ip}. "
                                 "Check device's parameters.")

    def send_ssh_command(self, command, waittime=1, recv_val=20000):
        for_send = (command + '\n').encode()
        self.connection.send(for_send)
        time.sleep(waittime)
        result = self.connection.recv(recv_val)
        result = result.decode().replace('\r\n', '\n')
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
        account = Account(name=username, password=password)
        try:
            self.connection = Telnet()
            self.connection.connect(self.ip)
            self.connection.login(account)
            own_logger.info(f'Connection to {self.ip} via Telnet established.')
            self._conn = 'telnet'
        except Exception as error:
            own_logger.error(f'Some error occured while connecting via Telnet'
                             f'to {self.ip}. Error is: {error}')
            self.connection.close()
            self._telnet_failed = True
            raise Exception(error)

    def send_telnet_command(self, command, waittime=0.5):
        for_send = (command + '\r\n')
        self.connection.execute(for_send)
        time.sleep(waittime)
        result = self.connection.response
        result = result.replace('\r\n', '\n')
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
