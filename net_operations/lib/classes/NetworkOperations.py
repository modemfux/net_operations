import re
import paramiko
import time
import telnetlib
from net_operations.lib.funcs import get_user_credentials
from net_operations.lib.funcs import work_with_script_folder
from net_operations.lib.funcs import decrypt_password
from net_operations.lib.funcs import structured_file_to_data, get_known_data
from net_operations.lib.funcs import data_to_structured_file
from net_operations.lib.logger import own_logger
from net_operations.lib.classes.NetUser import NetUser


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
