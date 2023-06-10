import getpass
from net_operations.lib.funcs import get_user_credentials
from net_operations.lib.funcs import encrypt_password, decrypt_password
from net_operations.lib.classes.NetFiles import NetFiles


class NetUser:
    _fs = NetFiles()

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
        self._fs.update_known_users(user_dict)
