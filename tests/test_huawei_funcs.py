from tests.dummy_class import DummyConnection
from net_operations.lib.huawei_funcs import get_huawei_nat_configuration
from net_operations.lib.huawei_funcs import get_huawei_nat_physical_loc
from net_operations.lib.huawei_funcs import get_huawei_nat_payload_stats
from net_operations.lib.huawei_funcs import get_huawei_nat_summary_statistic
from net_operations.lib.huawei_funcs import get_huawei_nat_session_license
from net_operations.lib.huawei_funcs import get_huawei_nat_cards
import pytest


dummy = DummyConnection()


@pytest.fixture
def fx_nat_configuration():
    nat_conf = {
        'ni_main': {
            'alg': 'all',
            'ni_id': '1',
            'nat-pools': ['192.0.2.0 25'],
            'limits': {
                'tcp': '2048',
                'udp': '2048',
                'icmp': '50',
                'total': '2048'},
            'ports': {
                'port-range': '256',
                'ext-port-range': '320',
                'ext-times': '3'},
            'sig': 'sig_main'},
        'ni_b2b_main': {
            'alg': 'all',
            'ni_id': '2',
            'nat-pools': ['203.0.113.1 32'],
            'limits': {
                'tcp': '1280',
                'udp': '1280',
                'icmp': '50',
                'total': '1280'},
            'ports': {
                'port-range': '256',
                'ext-port-range': '512',
                'ext-times': '2'},
            'sig': 'sig_main'}
    }
    return nat_conf


def test_get_huawei_nat_configuration(fx_nat_configuration):
    test_suit = get_huawei_nat_configuration(dummy)
    assert fx_nat_configuration == test_suit


@pytest.fixture
def fx_phys_loc():
    phys_loc = {'1': {'cpu_id': '0',
                      'sig': 'sig_main',
                      'slot': '3',
                      'cpu_type': 'engine'}}
    return phys_loc


def test_get_huawei_nat_physical_loc(fx_phys_loc):
    test_suit = get_huawei_nat_physical_loc(dummy)
    assert fx_phys_loc == test_suit


@pytest.fixture
def fx_payload():
    payload = [{'cpu_id': '0',
                'cpu_type': 'engine',
                'curr_rx_bps': '3295278768',
                'curr_rx_mbps': '3142.623',
                'curr_rx_pps': '411826',
                'curr_tx_bps': '3292203384',
                'curr_tx_mbps': '3139.69',
                'curr_tx_pps': '409961',
                'hist_max_rx_bps': '9804699304',
                'hist_max_rx_bps_date': '2023-05-03 05:15:02',
                'hist_max_rx_mbps': '9350.49',
                'hist_max_rx_pps': '1451215',
                'hist_max_rx_pps_date': '2021-11-29 19:15:06',
                'hist_max_tx_bps': '9377485040',
                'hist_max_tx_bps_date': '2022-03-22 0',
                'hist_max_tx_mbps': '8943.067',
                'hist_max_tx_pps': '1447679',
                'hist_max_tx_pps_date': '2021-11-29 19:15:06',
                'slot': '3'}]
    return payload


def test_get_huawei_nat_payload_stats(fx_payload):
    test_suit = get_huawei_nat_payload_stats(dummy)
    assert fx_payload == test_suit


@pytest.fixture
def fx_summ_stat():
    summ_stat = {'1': {'max_session_date': '2022-06-08 09:48:00',
                       'max_session_qty': '1718823',
                       'max_user_date': '2021-11-26 02:16:02',
                       'max_user_qty': '7559',
                       'total_session': '219084'}}
    return summ_stat


def test_get_huawei_nat_summary_statistic(fx_phys_loc, fx_summ_stat):
    test_suit = get_huawei_nat_summary_statistic(dummy, fx_phys_loc)
    assert fx_summ_stat == test_suit


@pytest.fixture
def fx_nat_lic():
    nat_lic = {
        'distribution': {
            'per_cpu': [{'cpu_id': '0',
                         'cur_sess_qty': '4',
                         'slot': '3',
                         'cpu_type': 'engine'}],
            'total': {'free': '0',
                      'total': '4',
                      'used': '4'}},
        'license': {
            'total': '2',
            'used': '2'}
    }
    return nat_lic


def test_get_huawei_nat_session_license(fx_nat_lic):
    test_suit = get_huawei_nat_session_license(dummy)
    assert fx_nat_lic == test_suit


@pytest.fixture
def fx_nat_cards():
    cards = {'3': {'board': 'CR5DVSUF8010', 'bw_license': [], 'pics': []}}
    return cards


def test_get_huawei_nat_cards(fx_nat_cards):
    test_suit = get_huawei_nat_cards(dummy)
    assert fx_nat_cards == test_suit
