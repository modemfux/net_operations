import re
import paramiko
import time
import telnetlib
from net_operations.lib.logger import own_logger
from net_operations.lib.classes.NetUser import NetUser
from net_operations.lib.classes.NetDevices import NetDevices
from net_operations.lib.constants import CONFIG_MODE, PAGINATION


class NetOperations:
    connection_type = None

    def __init__(self, ip, vendor, user=None, **dev_info):
        self.device = NetDevices(ip, vendor, **dev_info)
        self.device.save_device()
        self.ip = self.device.device_ip
        if not user:
            self.user = NetUser()
            users = self.user.get_all_known_users()
            users_prompt = [f'{i + 1} - {users[i]}'
                            for i in range(min(9, len(users)))]
            users_prompt.insert(0, '0 - Create/update user')
            print('There are some options:')
            print('\n'.join(users_prompt))
            choice = int(input('Choose your option for user (digit only): '))
            if choice == 0:
                self.user.create_new_user()
            else:
                self.user.fetch_user_data(users[choice - 1])

    def execute_initial_commands(self):
        init_commands = self.device.get_device_initial_commands()
        f_dict = {'ssh': self.send_ssh_commands,
                  'telnet': self.send_telnet_commands}
        executor = f_dict[self.connection_type]
        if init_commands:
            executor(init_commands)

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
                self.connection_type = 'ssh'
                self.execute_initial_commands()
            except Exception as error:
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
        self.connection_type = None
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
            self.connection_type = 'telnet'
            self.execute_initial_commands()
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

    def send_telnet_commands(self, commands_list, waittime=1):
        if not isinstance(commands_list, list):
            commands_list = [commands_list]
        output = ''
        for command in commands_list:
            output += self.send_telnet_command(command, waittime)
        return output

    def telnet_close(self):
        self.connection.close()
        own_logger.info(f'Telnet connection to {self.ip} is closed.')
        print(f'Telnet connection to {self.ip} is closed.')
        self.connection_type = None

    # Universal methods
    def establish_connection(self):
        try:
            self.establish_ssh_connection()
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

    def close(self):
        self.connection.close()
        self.connection_type = None
        own_logger.info(f'Connection to {self.ip} is closed.')
        print(f'Connection to {self.ip} is closed.')
        self.connection_type = None

    def send_commands(self, *args, **kwargs):
        commands_func_dict = {'telnet': self.send_telnet_commands,
                              'ssh': self.send_ssh_commands}
        return commands_func_dict[self.connection_type](*args, **kwargs)

    def enter_config_mode(self, quiet=False):
        commands = CONFIG_MODE[self.device.device_vendor]['in']
        if commands:
            output = self.send_commands(commands)
        else:
            output = ("This vendor isn't supported or "
                      "don't have specialized config mode")
            print(output)
        if not quiet:
            return output

    def exit_config_mode(self, quiet=False):
        commands = CONFIG_MODE[self.device.device_vendor]['out']
        if commands:
            output = self.send_commands(commands)
        else:
            output = ("This vendor isn't supported or "
                      "don't have specialized config mode")
            print(output)
        if not quiet:
            return output

    def enable_pagination(self, lines=80, quiet=False):
        raw_commands = PAGINATION[self.device.device_vendor]['on']
        commands = [item.format(lines) if '{' in item else item
                    for item in raw_commands]
        output = self.send_commands(commands)
        if not quiet:
            return output

    def disable_pagination(self, lines=80, quiet=False):
        commands = PAGINATION[self.device.device_vendor]['off']
        output = self.send_commands(commands)
        if not quiet:
            return output

    def send_config_commands(self, *args, **kwargs):
        output = self.enter_config_mode()
        output = self.send_commands(*args, **kwargs)
        output += self.exit_config_mode()
        return output

    # Context manager's functions
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()
        own_logger.info(f'Connection to {self.ip} is closed.')
        print(f'Connection to {self.ip} is closed.')
        self.connection_type = None

    def __str__(self):
        if not self.connection_type:
            str_net_ops = (f'NetOperations object. Connected to {self.ip} '
                           f'via {self.connection_type}')
        else:
            str_net_ops = 'NetOperations object'
        return str_net_ops
