import getpass
from net_operations.lib.funcs import get_user_credentials
from net_operations.lib.funcs import encrypt_password, decrypt_password
from net_operations.lib.classes.NetFiles import NetFiles


class NetUser:
    _fs = NetFiles()

    def __init__(self, username=None, password=None):
        if username is None and password is None:
            self.username = username
            self.password = password
        else:
            if any((not username, not password)):
                username, password = get_user_credentials()
            self.username = username
            self._key, self.password = encrypt_password(password)

    def create_new_user(self, save=True):
        username, password = get_user_credentials()
        self.username = username
        self._key, self.password = encrypt_password(password)
        if save:
            self.save_user()

    def get_unenc_password(self):
        return decrypt_password(self._key, self.password)

    def update_password(self, new_pass=None):
        if not new_pass:
            new_pass = getpass.getpass('Enter your new password: ')
        self._key, self.password = encrypt_password(new_pass)

    def save_user(self):
        user_dict = {self.username: {'key': self._key,
                                     'password': self.password}}
        self._fs.update_known_users(user_dict)

    def get_all_known_users(self, only_name=True):
        users = self._fs.get_known_users()
        return list(users.keys()) if only_name else users

    def fetch_user_data(self, username):
        data = self.get_all_known_users(only_name=False).get(username, None)
        if data:
            self.username = username
            self.password = data['password']
            self._key = data['key']
        else:
            raise KeyError(f'No such user as {username}')

    def __str__(self):
        return self.username
