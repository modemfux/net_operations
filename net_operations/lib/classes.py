import os
import logging
import paramiko
import getpass
import time
# import telnetlib
from datetime import datetime
from net_operations.lib.os_functions import check_availability_via_ping
from net_operations.lib.os_functions import get_user_credentials
from net_operations.lib.os_functions import work_with_script_folder
from net_operations.lib.funcs import encrypt_password, decrypt_password
from net_operations.lib.funcs import structured_file_to_data, get_known_data
from net_operations.lib.funcs import data_to_structured_file


# Logging config
logfile = str(datetime.now()).replace(':', '.').replace(' ', '_') + '.log'
own_folder = work_with_script_folder()
logfile = own_folder + logfile
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

    def get_known_devices(self):
        self._known_devices = get_known_data('known_devices.yaml')

    def save_known_devices(self, filepath='default'):
        if filepath == 'default':
            filepath = work_with_script_folder + '/' + 'known_devices.yaml'
        data_to_structured_file(self._known_devices, filepath)
        own_logger.info(f'{filepath} updated.')

    def get_known_user_information(self, name, filepath='default'):
        if filepath == 'default':
            filepath = work_with_script_folder + '/' + 'known_users.yaml'
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
        self.device = {self.ip: {'vendor': vendor, 'conn_type': conn_type}}
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

        device_state = check_availability_via_ping(self.ip)

        if not device_state:
            own_logger.error(f"Device {self.ip} isn't reachable.")
            raise Exception(f"Device {self.ip} isn't reachable.")
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
        except TimeoutError as error:
            own_logger.error(f'Connection to {self.ip} is {error}')
            print(f'Connection to {self.ip} is {error}')
            connection_state = False
            raise TimeoutError
        except Exception as error:
            own_logger.error(f'Some error occured while connecting '
                             f'to {self.ip}. Error is: {error}')
            raise Exception(error)
        if connection_state:
            try:
                self.connection = client.invoke_shell()
                print(f'Connection to {self.ip} established.')
            except Exception:
                own_logger.exception(f"There are some problems "
                                     f"with connection to {self.ip}. "
                                     "Check device's parameters.")

    def send_ssh_command(self, command, waittime=0.5, recv_val=10000):
        for_send = (command + '\n').encode()
        self.connection.send(for_send)
        time.sleep(waittime)
        result = self.connection.recv(recv_val)
        result = result.replace('\r\n', '\n')
        return result.decode()

    def send_ssh_commands(self, commands_list):
        if not isinstance(commands_list, list):
            commands_list = [commands_list]
        output = ''
        for command in commands_list:
            output += self.send_ssh_command(command)
        return output

    def ssh_close(self):
        self.connection.close()
        own_logger.info(f'SSH connection to {self.ip} is closed.')
        print(f'SSH connection to {self.ip} is closed.')

# Telnet Connection methods section
#    def establish_telnet_connection(self):
#        return telnetlib

# Context manager's function
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()
        own_logger.info(f'Connection to {self.ip} is closed.')
        print(f'Connection to {self.ip} is closed.')
