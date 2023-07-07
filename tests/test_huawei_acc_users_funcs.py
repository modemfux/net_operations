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
        'Eth-Trunk1.136': {'type': 'Layer2-subscriber', 'online': '2'},
        'Eth-Trunk1.501': {'type': 'Layer2-subscriber', 'online': '708'},
        'Eth-Trunk1.503': {'type': 'Layer2-subscriber', 'online': '1867'},
        'Eth-Trunk1.505': {'type': 'Layer2-subscriber', 'online': '351'},
        'Eth-Trunk1.519': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.520': {'type': 'Layer2-subscriber', 'online': '973'},
        'Eth-Trunk1.540': {'type': 'Layer2-subscriber', 'online': '599'},
        'Eth-Trunk1.541': {'type': 'Layer2-subscriber', 'online': '747'},
        'Eth-Trunk1.542': {'type': 'Layer2-subscriber', 'online': '172'},
        'Eth-Trunk1.550': {'type': 'Layer2-subscriber', 'online': '543'},
        'Eth-Trunk1.571': {'type': 'Layer2-subscriber', 'online': '118'},
        'Eth-Trunk1.578': {'type': 'Layer2-subscriber', 'online': '1247'},
        'Eth-Trunk1.586': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.590': {'type': 'Layer2-subscriber', 'online': '337'},
        'Eth-Trunk1.593': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.597': {'type': 'Layer2-subscriber', 'online': '201'},
        'Eth-Trunk1.601': {'type': 'Layer2-subscriber', 'online': '4'},
        'Eth-Trunk1.603': {'type': 'Layer2-subscriber', 'online': '13'},
        'Eth-Trunk1.605': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.620': {'type': 'Layer2-subscriber', 'online': '4'},
        'Eth-Trunk1.640': {'type': 'Layer2-subscriber', 'online': '6'},
        'Eth-Trunk1.641': {'type': 'Layer2-subscriber', 'online': '2'},
        'Eth-Trunk1.642': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.650': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.659': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.662': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.663': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.664': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.665': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.667': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.668': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.669': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.670': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.671': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.672': {'type': 'Layer2-subscriber', 'online': '2'},
        'Eth-Trunk1.673': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.674': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.675': {'type': 'Layer2-subscriber', 'online': '4'},
        'Eth-Trunk1.676': {'type': 'Layer2-subscriber', 'online': '2'},
        'Eth-Trunk1.677': {'type': 'Layer2-subscriber', 'online': '7'},
        'Eth-Trunk1.678': {'type': 'Layer2-subscriber', 'online': '11'},
        'Eth-Trunk1.679': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.680': {'type': 'Layer2-subscriber', 'online': '5'},
        'Eth-Trunk1.684': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.685': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.686': {'type': 'Layer2-subscriber', 'online': '4'},
        'Eth-Trunk1.687': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.690': {'type': 'Layer2-subscriber', 'online': '6'},
        'Eth-Trunk1.692': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.693': {'type': 'Layer2-subscriber', 'online': '2'},
        'Eth-Trunk1.694': {'type': 'Layer2-subscriber', 'online': '2'},
        'Eth-Trunk1.695': {'type': 'Layer2-subscriber', 'online': '3'},
        'Eth-Trunk1.696': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.697': {'type': 'Layer2-subscriber', 'online': '3'},
        'Eth-Trunk1.698': {'type': 'Layer2-subscriber', 'online': '14'},
        'Eth-Trunk1.998': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.1999': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3000': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3020': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3600': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3601': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3631': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3645': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3651': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3652': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3653': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3655': {'type': 'Layer2-subscriber', 'online': '2'},
        'Eth-Trunk1.3656': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3661': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3665': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3666': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3675': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3676': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3677': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3684': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3685': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3686': {'type': 'Layer2-subscriber', 'online': '4'},
        'Eth-Trunk1.3687': {'type': 'Layer2-subscriber', 'online': '3'},
        'Eth-Trunk1.3698': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3699': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3708': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3715': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3724': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3725': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3726': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3729': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3731': {'type': 'Layer2-subscriber', 'online': '27'},
        'Eth-Trunk1.3736': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3756': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3761': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3784': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3823': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3839': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3844': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3845': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3848': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3860': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3865': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3874': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3886': {'type': 'Layer2-subscriber', 'online': '8'},
        'Eth-Trunk1.3887': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3890': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3896': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3899': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3903': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3917': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3929': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3931': {'type': 'Layer2-subscriber', 'online': '3'},
        'Eth-Trunk1.3938': {'type': 'Layer2-subscriber', 'online': '5'},
        'Eth-Trunk1.3945': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3957': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.3958': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3988': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.3989': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.4005': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.4025': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.4039': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.4095': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.5013950': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.5190129': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.5190184': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.5900099': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.6013950': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.6033010': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.6033809': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.6203743': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.6203766': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.6203857': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.6403773': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.6413002': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.6413006': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.6613673': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.6720863': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.6763716': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.6763745': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.6783011': {'type': 'Layer2-subscriber', 'online': '2'},
        'Eth-Trunk1.6783920': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.6813746': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.6853848': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.6853965': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.6923772': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.6933808': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.6943881': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.6953724': {'type': 'Layer2-subscriber', 'online': '1'},
        'Eth-Trunk1.6953908': {'type': 'Layer2-subscriber', 'online': '0'},
        'Eth-Trunk1.6953923': {'type': 'Layer2-subscriber', 'online': '1'},
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
