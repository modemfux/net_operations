from jinja2 import Environment, FileSystemLoader
from cryptography.fernet import Fernet
import pwd
import getpass
import os
import yaml
import json
import subprocess
from net_operations.lib.constants import INITIAL_COMMANDS


def is_ip_address(ip):
    if not isinstance(ip, str):
        ip = str(ip)
    sp = ip.split('.')
    check_dict = {
        'four_octets': len(sp) == 4,
        'all_digits': all(map(lambda x: x.isdigit(), sp))
    }
    if check_dict['all_digits']:
        check_dict['correct_numbers'] = all(
            map(lambda x: int(x) in range(0, 256), sp)
        )
    else:
        check_dict['correct_numbers'] = False
    return all(check_dict.values())


def check_availability_via_ping(ip):
    if not is_ip_address(ip):
        print('Вы ввели некорректный IP-адрес.')
        raise Exception('Wrong IP format')
    unavailable = bool(
        subprocess.run(
            f'ping -c 2 -n -W 1 {ip}',
            stdout=subprocess.DEVNULL,
            shell=True).returncode
        )
    return not unavailable


def work_with_script_folder():
    config_dir = os.getenv('HOME') + '/.config/'
    own_dir = config_dir + 'net_operations'
    state = os.path.exists(own_dir)
    if not state:
        logfile = f'{own_dir}/net_operations.log'
        userfile = f'{own_dir}/known_users.yaml'
        devices = f'{own_dir}/known_devices.yaml'
        initial = f'{own_dir}/initial_commands.yaml'
        inventory = {
            'directories': [config_dir, own_dir],
            'files': [
                {'dst_filename': logfile,
                 'coll': '',
                 'format': 'text'},
                {'dst_filename': userfile,
                 'coll': {},
                 'format': 'yaml'},
                {'dst_filename': devices,
                 'coll': {},
                 'format': 'yaml'},
                {'dst_filename': initial,
                 'coll': INITIAL_COMMANDS,
                 'format': 'yaml'}]}
        # Check existence of local config directories
        for directory in inventory['directories']:
            if not os.path.exists(directory):
                os.mkdir(directory)
        # Check existence of local config files
        for file in inventory['files']:
            if not os.path.exists(file['dst_filename']):
                data_to_structured_file(**file)
    return own_dir


def get_user_credentials():
    '''
    Asks user's login and password, then returns them as tuple.
    '''
    try:
        default_username = os.getlogin()
    except Exception:
        uid = os.getuid()
        default_username = pwd.getpwuid(uid).pw_name
    username = input(f'Enter your username [{default_username}]: ')
    if not username:
        username = default_username
    password = None
    while not password:
        password = getpass.getpass('Enter your password: ')
    return username, password


def get_extension(name):
    return name.split('.')[-1] if '.' in name else None


def data_to_structured_file(coll, dst_filename, format='yaml'):
    with open(dst_filename, 'w') as dst:
        if format == 'yaml':
            yaml.safe_dump(coll, dst)
        elif format == 'json':
            json.dump(coll, dst)
        else:
            dst.write(coll)


def structured_file_to_data(src_filename):
    actions = {
        'json': json.load,
        'yml': yaml.safe_load,
        'yaml': yaml.safe_load
        }
    if not os.path.exists(src_filename):
        path, name = os.path.split(src_filename)
        raise Exception(f'There is no such file as "{name}" in "{path}"')
    else:
        ext = get_extension(src_filename)
        with open(src_filename) as src:
            return actions[ext](src) if actions.get(ext) else src.read()


def decrypt_password(key, encrypted_password):
    decryptor = Fernet(str(key).encode())
    return decryptor.decrypt(str(encrypted_password).encode()).decode()


def encrypt_password(raw_password):
    key = Fernet.generate_key()
    encryptor = Fernet(key)
    encrypted_password = encryptor.encrypt(raw_password.encode())
    return key.decode(), encrypted_password.decode()


def get_remote_device_data(device={}):
    # Get known routers informations
    memory_file = work_with_script_folder() + '/known_routers.yaml'
    if os.path.exists(memory_file):
        with open(memory_file) as src:
            known_routers = yaml.safe_load(src)
    else:
        known_routers = {}

    if not device.get('ip'):
        ip = input('Не хватает параметра ip. Введите его: ')
        device['ip'] = ip

    if known_routers.get(ip):
        user = known_routers[ip]['username']
        key = known_routers[ip]['key']
        password = decrypt_password(key, known_routers[ip]['password'])
        print(f'Для адреса {ip} есть сохраненные данные для '
              f'пользователь {user}.')
        choice = input('Хотите воспользоваться ими?[Y/n]: ').lower()
        if choice in ['', 'y']:
            device['username'] = user
            device['password'] = password
            return device

    known_routers[ip] = {}
    username = input('Не хватает параметра username. Введите его: ')
    password = getpass('Не хватает параметра password. Введите его: ')
    device['username'] = username
    device['password'] = password
    known_routers[ip]['username'] = username
    key, enc_pass = encrypt_password(password)
    known_routers[ip]['key'] = key
    known_routers[ip]['password'] = enc_pass
    with open(memory_file, 'w') as dst:
        yaml.safe_dump(known_routers, dst)
    return device


def get_known_data(src_file):
    filename = work_with_script_folder() + '/' + src_file
    return structured_file_to_data(filename) if os.path.exists(filename) else {}


def generate_from_template(template_path, src_data):
    path, file = os.path.split(template_path)
    if path == '':
        path = '.'
    env = Environment(lstrip_blocks=True,
                      trim_blocks=True,
                      loader=FileSystemLoader(path))
    template = env.get_template(file)
    result = template.render(src_data)
    return result
