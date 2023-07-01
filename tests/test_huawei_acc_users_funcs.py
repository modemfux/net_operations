import pytest
from tests.dummy_class import DummyConnection
from net_operations.lib.huawei.acc_users_funcs import get_huawei_domains
from net_operations.lib.huawei.acc_users_funcs import get_huawei_domain_info


dummy = DummyConnection()


@pytest.fixture
def fx_huawei_domains():
    domains = {
        'default0': {'online': '0'},
        'default1': {'online': '0'},
        'default_admin': {'online': '1'},
        'ipoe': {'online': '0'},
        'business_2m': {'online': '0'},
        'ipoe_public_ha': {'online': '0'},
        'ipoe_ha': {'online': '0'},
        'dom_titan_1': {'online': '27'},
        'dom_titan_2': {'online': '0'},
        'b2b_test': {'online': '0'},
        'ipv6_test': {'online': '0'},
        'dom_ipoe_main': {'online': '7860'},
        'b2b_gray': {'online': '117'},
        'dom_ipoe_main_public_ha': {'online': '0'},
        'dom_b2b_ipoe_main': {'online': '3'},
        'ipoe-radius-test': {'online': '0'},
        'dom_ipoe_white_no_auth': {'online': '46'},
    }
    return domains


def test_get_huawei_domains(fx_huawei_domains):
    domains = get_huawei_domains(dummy)
    assert fx_huawei_domains == domains


@pytest.fixture
def fx_huawei_domain_info():
    dom_name = 'dom_ipoe_main'
    info = {
        'dom_ipoe_main': {
            "authen_scheme": "auth_rad",
            "account_scheme": "acct_rad",
            "author_scheme": None,
            "online": "7863",
            "redirect_url": "http://192.0.2.254/",
            "radius_server": "xrad-radius",
            "tacacs_server": None,
            "default_ip_pool": "pool_nat_01",
            "nat_user_group": "ug_nat_ha",
            "nat_instance": "ni_main",
            "dns_ipv4": ["8.8.8.8", "8.8.4.4"],
            "dns_ipv6": [None, None]
        }
    }
    return dom_name, info


def test_get_huawei_domain_info(fx_huawei_domain_info):
    domain, reference = fx_huawei_domain_info
    info = get_huawei_domain_info(dummy, domain)
    assert reference == info
