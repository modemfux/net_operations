import getpass
import subprocess
import os


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
    home_dir = os.getenv('HOME') + '/'
    if os.path.exists(home_dir):
        brases_dir = home_dir + '.brases'
        if not os.path.exists(brases_dir):
            os.mkdir(brases_dir)
        return brases_dir


def get_user_credentials():
    '''
    Asks user's login and password, then returns them as tuple.
    '''
    default_username = os.getlogin()
    username = input(f'Enter your username [{default_username}]: ')
    if not username:
        username = default_username
    password = None
    while not password:
        password = getpass.getpass('Enter your password: ')
    return username, password

