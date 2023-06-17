import os
import pytest
import yaml
import tempfile
from cryptography.fernet import Fernet
from net_operations.lib.funcs import is_ip_address, check_availability_via_ping
from net_operations.lib.funcs import get_extension, decrypt_password
from net_operations.lib.funcs import check_correct_type
from net_operations.lib.funcs import data_to_structured_file
from net_operations.lib.funcs import structured_file_to_data
from net_operations.lib.funcs import generate_from_template


@pytest.fixture
def fix_is_ip():
    ip_right = '127.0.0.1'
    ip_wrong1 = '1.2.A.4'
    ip_wrong2 = '1.1.1'
    ip_wrong3 = '256.0.1.1'
    ip_wrong4 = '127.0.0. 1'
    ip_wrong5 = [1, 2, 3]
    return (ip_right, [ip_wrong1, ip_wrong2, ip_wrong3, ip_wrong4, ip_wrong5])


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


@pytest.fixture
def fx_dict():
    sample_dict = {
        'first': {
            '1': [1, 2, 3],
            '2': 'Sample!'},
        'second': ['A', 'B', 'C']}
    return sample_dict


def test_data_to_structured_file(fx_dict):
    with open('tests/fixtures/sample_dict.json') as src:
        json_sample = src.read()
    with open('tests/fixtures/sample_dict.yaml') as src:
        yaml_sample = src.read()
    with open('tests/fixtures/sample_dict.txt') as src:
        txt_sample = src.read()
    test = [('json', json_sample), ('yaml', yaml_sample), ('txt', txt_sample)]
    with tempfile.TemporaryDirectory() as tmp:
        for format_, example in test:
            with tempfile.NamedTemporaryFile(mode='w+', dir=tmp) as f:
                data_to_structured_file(fx_dict, f.name, format=format_)
                with open(f.name) as src:
                    assert src.read() == example


@pytest.fixture
def fx_struct_to_data():
    sample_dict = {
        'first': {
            '1': [1, 2, 3],
            '2': 'Sample!'},
        'second': ['A', 'B', 'C']}
    txt = ("{'first': {'1': [1, 2, 3], '2': 'Sample!'},"
           " 'second': ['A', 'B', 'C']}")
    data = [
        ('tests/fixtures/sample_dict.json', sample_dict, True),
        ('tests/fixtures/sample_dict.yaml', sample_dict, True),
        ('tests/fixtures/sample_dict.txt', txt,  True),
        ('tests/fixtures/sample_dict.yml', None, False)
    ]
    return data


def test_structured_file_to_data(fx_struct_to_data):
    for filename, result, state in fx_struct_to_data:
        if state:
            assert structured_file_to_data(filename) == result
        else:
            with pytest.raises(Exception) as excinfo:
                path, name = os.path.split(filename)
                err_message = f'There is no such file as "{name}" in "{path}"'
                structured_file_to_data(filename)
                assert err_message == str(excinfo.value)


# @pytest.fixture
# def fx_generate_report():
#     with open('tests/fixtures/sample_report_dict.yml') as src:
#         src_dict = yaml.safe_load(src)
#     full_dict = {
#         'template_path': 'tests/fixtures/sample_report_template.jinja2',
#         'src_data': src_dict}
#     return full_dict
# 
# 
# def test_generate_from_template(fx_generate_report):
#     with open('tests/fixtures/sample_report_example.md') as src:
#         example = src.read()
#     assert example == generate_from_template(**fx_generate_report)
