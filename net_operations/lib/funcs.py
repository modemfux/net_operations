from net_operations.lib.os_functions import work_with_script_folder
from cryptography.fernet import Fernet
import getpass
import os
import yaml
import json


def get_extension(name):
    return name.split('.')[-1] if '.' in name else None


def data_to_structured_file(coll, dst_filename, format='yaml'):
    with open(dst_filename, 'w') as dst:
        if format == 'yaml':
            yaml.safe_dump(coll, dst)
        elif format == 'json':
            json.dump(coll, dst)


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
    known_data = structured_file_to_data(filename)
    return known_data
