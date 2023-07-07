class DummyConnection:
    '''
    Dummy class for testing
    '''
    def __init__(self):
        self.commands = {
            'display nat instance': '0',
            'display nat instance ni_main': '1',
            'display nat instance ni_b2b_main': '2',
            'display service-location': '3',
            'display service-location 1': '4',
            'display service-instance-group': '5',
            'display service-instance-group sig_main': '6',
            'display nat statistics payload': '7',
            'display nat statistics table slot 3 engine 0': '8',
            'display license resource usage': '9',
            'display nat session-table size': '10',
            'display elabel brief': '11',
            'display current-conf conf license': '12',
            'display version slot 3': '13',
            'display domain': '14',
            'display domain dom_ipoe_main': '15',
            'display bas-interface': '16',
            'display bas-interface Eth-Trunk1.520': '17',
            'display radius-server configuration group xrad-radius': '18',
            'display access-user ip-type ipv4 summary': '19',
            'display access-user ip-type ipv6 summary': '20',
            'display static-user': '21'
        }

        self.files = {
            '0': 'tests/fixtures/dis_nat_inst.txt',
            '1': 'tests/fixtures/dis_nat_inst_ni_main.txt',
            '2': 'tests/fixtures/dis_nat_inst_ni_b2b_main.txt',
            '3': 'tests/fixtures/dis_serv_loc.txt',
            '4': 'tests/fixtures/dis_serv_loc_1.txt',
            '5': 'tests/fixtures/dis_serv_inst_gr.txt',
            '6': 'tests/fixtures/dis_serv_inst_gr_sig_main.txt',
            '7': 'tests/fixtures/dis_nat_stat_payload.txt',
            '8': 'tests/fixtures/dis_nat_stat_tab_sl_3_en_0.txt',
            '9': 'tests/fixtures/dis_lic_res_usage.txt',
            '10': 'tests/fixtures/dis_nat_sess_tab_size.txt',
            '11': 'tests/fixtures/dis_elabel_brief.txt',
            '12': 'tests/fixtures/dis_curr_conf_lic.txt',
            '13': 'tests/fixtures/dis_ver_sl_3.txt',
            '14': 'tests/fixtures/dis_domain.txt',
            '15': 'tests/fixtures/dis_domain_dom_ipoe_main.txt',
            '16': 'tests/fixtures/dis_bas_interface.txt',
            '17': 'tests/fixtures/dis_bas_interface_et1520.txt',
            '18': 'tests/fixtures/dis_radius_server_conf_group_xrad_radius.txt',
            '19': 'tests/fixtures/dis_acc_users_ip_type_ipv4.txt',
            '20': 'tests/fixtures/dis_acc_users_ip_type_ipv6.txt',
            '21': 'tests/fixtures/dis_static_user.txt'
        }

        self.ip = '127.0.0.1'

    def send_commands(self, commands_list, *args, **kwargs):
        if not isinstance(commands_list, list):
            commands_list = [commands_list]
        result = ''
        if args or kwargs:
            pass
        for command in commands_list:
            filename = self.files[self.commands[command]]
            with open(filename) as src:
                mid = src.read()
            self.prompt = mid.split('\n')[-1]
            mid = mid.replace('\r\n', '\n').rstrip()
            result += mid
        return result
