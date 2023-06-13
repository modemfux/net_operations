import pytest
from net_operations.lib.funcs import is_ip_address, check_availability_via_ping


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
