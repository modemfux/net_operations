import pytest
import yaml
from cryptography.fernet import Fernet
from net_operations.lib.funcs import is_ip_address, check_availability_via_ping
from net_operations.lib.funcs import get_extension, decrypt_password
from net_operations.lib.funcs import check_correct_type


@pytest.fixture
def fix_is_ip():
    ip_right = '127.0.0.1'
    ip_wrong1 = '1.2.A.4'
    ip_wrong2 = '1.1.1'
    ip_wrong3 = '256.0.1.1'
    ip_wrong4 = '127.0.0. 1'
    return (ip_right, [ip_wrong1, ip_wrong2, ip_wrong3, ip_wrong4])


def test_is_ip_address(fix_is_ip):
    right, wrong_list = fix_is_ip
    assert is_ip_address(right)
    for wrong_ip in wrong_list:
        assert not is_ip_address(wrong_ip)


def test_check_availability_via_ping():
    assert check_availability_via_ping('127.0.0.1')
    assert not check_availability_via_ping('239.255.255.255')
    with pytest.raises(Exception) as excinfo:
        check_availability_via_ping('127.0.0')
        assert 'Wrong IP format' == str(excinfo.value)


def test_get_extension():
    assert get_extension('test1.yaml') == 'yaml'
    assert get_extension('test.2.json') == 'json'
    assert get_extension('test3') is None


@pytest.fixture
def fx_stored_user():
    with open('tests/fixtures/sample_stored_user.yaml') as src:
        user_dict = yaml.safe_load(src)
    key = user_dict['cisco']['key'].encode()
    enc_password = user_dict['cisco']['password'].encode()
    decryptor = Fernet(key)
    password = decryptor.decrypt(enc_password).decode()
    return password, user_dict['cisco']


def test_decrypt_password(fx_stored_user):
    password, user_dict = fx_stored_user
    key = user_dict['key']
    enc_password = user_dict['password']
    assert password == decrypt_password(key, enc_password)


def test_check_correct_type():
    err_message = "This is not <class 'list'>, but <class 'dict'>"
    assert check_correct_type({}, dict) is None
    with pytest.raises(TypeError) as excinfo:
        check_correct_type({}, list)
        assert err_message == str(excinfo.value)
