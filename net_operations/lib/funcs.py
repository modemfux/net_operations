from jinja2 import Environment, FileSystemLoader
from cryptography.fernet import Fernet
import pwd
import getpass
import os
import yaml
import json
import subprocess


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
            json.dump(coll, dst, indent=4)
        else:
            dst.write(str(coll))


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


def check_correct_type(data, type_):
    if not isinstance(data, type_):
        err = str(type(data))
        raise TypeError(f'This is not {type_}, but {err}')
