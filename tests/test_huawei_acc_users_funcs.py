import pytest
from tests.dummy_class import DummyConnection
from net_operations.lib.huawei.acc_users_funcs import get_huawei_domains
from net_operations.lib.huawei.acc_users_funcs import get_huawei_domain_info
from net_operations.lib.huawei.acc_users_funcs import get_huawei_bas_interfaces
from net_operations.lib.huawei.acc_users_funcs import get_huawei_bas_intf_info
from net_operations.lib.huawei.acc_users_funcs import get_huawei_radius_gr_info
from net_operations.lib.huawei.acc_users_funcs import get_huawei_total_users
from net_operations.lib.huawei.acc_users_funcs import get_hw_intf_with_statics


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


@pytest.fixture
def fx_huawei_bas_intf():
    bas_intf_dict = {
        'Eth-Trunk1.520': {'type': 'Layer2-subscriber', 'online': '973'},
        'Eth-Trunk1.540': {'type': 'Layer2-subscriber', 'online': '599'},
        'Eth-Trunk1.3652': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3653': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.6963878': {'type': 'Layer2-subscriber', 'online': '1'}
        }
    return bas_intf_dict


def test_get_huawei_bas_interfaces(fx_huawei_bas_intf):
    bases = get_huawei_bas_interfaces(dummy)
    assert fx_huawei_bas_intf == bases


@pytest.fixture
def fx_huawei_bas_intf_info():
    info = {'Eth-Trunk1.520': {
        "preauth_domain": "default0",
        "authen_domain": "dom_ipoe_main",
        "authen_method": "bind",
        "opt82": "On",
        "vrf": None}}
    return "Eth-Trunk1.520", info


def test_get_huawei_bas_intf_info(fx_huawei_bas_intf_info):
    fx_interface, fx_info = fx_huawei_bas_intf_info
    info = get_huawei_bas_intf_info(dummy, fx_interface)
    assert fx_info == info


@pytest.fixture
def fx_radius_conf_group():
    rad_conf = {
        "authen_servers": [
            {"ip": "10.0.0.151",
             "port": "1812",
             "weight": "100",
             "vrf": "BR_TECH"},
            {"ip": "10.0.0.152",
             "port": "1812",
             "weight": "50",
             "vrf": "BR_TECH"},
            {"ip": "10.0.0.153",
             "port": "1812",
             "weight": "0",
             "vrf": "BR_TECH"},
            {"ip": "10.0.0.140",
             "port": "1812",
             "weight": "0",
             "vrf": "BR_TECH"}
        ],
        "account_servers": [
            {"ip": "10.0.0.151",
             "port": "1813",
             "weight": "100",
             "vrf": "BR_TECH"},
            {"ip": "10.0.0.152",
             "port": "1813",
             "weight": "50",
             "vrf": "BR_TECH"},
            {"ip": "10.0.0.153",
             "port": "1813",
             "weight": "0",
             "vrf": "BR_TECH"}
        ],
        "src_interface": "LoopBack12",
        "call_station_id": "mac"
    }
    return "xrad-radius", rad_conf


def test_get_huawei_radius_gr_info(fx_radius_conf_group):
    fx_rsg_name, fx_result = fx_radius_conf_group
    result = get_huawei_radius_gr_info(dummy, fx_rsg_name)
    assert fx_result == result


@pytest.fixture
def fx_acc_user_ip_type():
    users_dict = {
        "ipv4": {
            "normal": "4",
            "rui_local": "4245",
            "rui_remote": "3835",
            "radius_auth": "7739",
            "no_auth": "345",
            "total": "8084"
        },
        "ipv6": {
            "normal": None,
            "rui_local": None,
            "rui_remote": None,
            "radius_auth": None,
            "no_auth": None,
            "total": None
        },
    }
    return users_dict


def test_get_huawei_total_users(fx_acc_user_ip_type):
    result = get_huawei_total_users(dummy)
    assert fx_acc_user_ip_type == result


@pytest.fixture
def fx_intf_with_statics():
    fx_intfs = ["Eth-Trunk1.3652", "Eth-Trunk1.3653"]
    with open('tests/fixtures/021.txt') as src:
        fx_output = src.read()
    return fx_intfs, fx_output


def test_get_hw_intf_with_statics(fx_intf_with_statics):
    fx_intfs, _ = fx_intf_with_statics
    result = get_hw_intf_with_statics(dummy, with_output=False)
    assert sorted(fx_intfs) == result
    result = get_hw_intf_with_statics(dummy, with_output=True)
    assert fx_intf_with_statics == result
