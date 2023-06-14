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
            'display version slot 3': '13'
        }

        self.files = {
            '0': 'fixtures/dis_nat_inst.txt',
            '1': 'fixtures/dis_nat_inst_ni_main.txt',
            '2': 'fixtures/dis_nat_inst_ni_b2b_main.txt',
            '3': 'fixtures/dis_serv_loc.txt',
            '4': 'fixtures/dis_serv_loc_1.txt',
            '5': 'fixtures/dis_serv_inst_gr.txt',
            '6': 'fixtures/dis_serv_inst_gr_sig_main.txt',
            '7': 'fixtures/dis_nat_stat_payload.txt',
            '8': 'fixtures/dis_nat_stat_tab_sl_3_en_0.txt',
            '9': 'fixtures/dis_lic_res_usage.txt',
            '10': 'fixtures/dis_nat_sess_tab_size.txt',
            '11': 'fixtures/dis_elabel_brief.txt',
            '12': 'fixtures/dis_curr_conf_lic.txt',
            '13': 'fixtures/dis_ver_sl_3.txt'
        }

    def send_commands(self, commands_list):
        if not isinstance(commands_list, list):
            commands_list = [commands_list]
        result = ''
        for command in commands_list:
            filename = self.files[self.commands[command]]
            with open(filename) as src:
                mid = src.read()
            self.prompt = mid.split('\n')[-1]
            mid = mid.replace('\r\n', '\n').rstrip()
            result += mid
        return result
