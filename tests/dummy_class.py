class DummyConnection:
    '''
    Dummy class for testing
    '''
    def __init__(self):
        self.commands = {
            "display nat instance": "000.txt",
            "display nat instance ni_main": "001.txt",
            "display nat instance ni_b2b_main": "002.txt",
            "display service-location": "003.txt",
            "display service-location 1": "004.txt",
            "display service-instance-group": "005.txt",
            "display service-instance-group sig_main": "006.txt",
            "display nat statistics payload": "007.txt",
            "display nat statistics table slot 3 engine 0": "008.txt",
            "display license resource usage": "009.txt",
            "display nat session-table size": "010.txt",
            "display elabel brief": "011.txt",
            "display current-conf conf license": "012.txt",
            "display version slot 3": "013.txt",
            "display domain": "014.txt",
            "display domain dom_ipoe_main": "015.txt",
            "display bas-interface": "016.txt",
            "display bas-interface Eth-Trunk1.520": "017.txt",
            "display radius-server configuration group xrad-radius": "018.txt",
            "display access-user ip-type ipv4 summary": "019.txt",
            "display access-user ip-type ipv6 summary": "020.txt",
            "display static-user": "021.txt",
            "display version": "022.txt",
            "display accounting-scheme acct_rad": "023.txt",
            "display access-user domain dom_ipoe_main summary": "024.txt",
            "display authentication-scheme auth_rad": "025.txt",
            "display cpu-usage sorted": "026.txt",
            "display cpu-usage sorted slave": "027.txt",
            "display cpu-usage slot 1": "028.txt",
            "display cpu-usage slot 2": "029.txt",
            "display cpu-usage slot 3": "030.txt",
            "display cur conf user-interface": "031.txt",
            "display device 1": "032.txt",
            "display device 2": "033.txt",
            "display device 3": "034.txt",
            "display device 4": "035.txt",
            "display device 5": "036.txt",
            "display device 6": "037.txt",
            "display device 7": "038.txt",
            "display device 8": "039.txt",
            "display device 9": "040.txt",
            "display device 10": "041.txt",
            "display elabel optical-module brief": "042.txt",
            "display esn": "043.txt",
            "display eth-trunk": "044.txt",
            "display eth-trunk sub-interface": "045.txt",
            "display interface Eth-Trunk1": "046.txt",
            "display interface Eth-Trunk2": "047.txt",
            "display interface GigabitEthernet2/1/0": "048.txt",
            "display interface GigabitEthernet1/1/0": "049.txt",
            "display interface GigabitEthernet1/1/1": "050.txt",
            "display interface GigabitEthernet2/1/1": "051.txt",
            "display license": "052.txt",
            "display license esn": "053.txt",
            "display lldp neighbor brief": "054.txt",
            "display lldp neighbor interface GigabitEthernet1/1/0": "055.txt",
            "display lldp neighbor interface GigabitEthernet1/1/1": "056.txt",
            "display lldp neighbor interface GigabitEthernet2/1/0": "057.txt",
            "display lldp neighbor interface GigabitEthernet2/1/1": "058.txt",
            "display memory-usage": "059.txt",
            "display memory-usage slave": "060.txt",
            ("display radius-server packet ip-address 10.0.0.151 "
             "vpn-instance BR_TECH accounting"): "061.txt",
            ("display radius-server packet ip-address 10.0.0.151 "
             "vpn-instance BR_TECH authentication"): "062.txt",
            ("display radius-server packet ip-address 10.0.0.151 "
             "vpn-instance BR_TECH coa"): "063.txt",
            "display remote-backup-profile": "064.txt",
            "display remote-backup-profile b2b_test_gray": "065.txt",
            "display remote-backup-profile rbp_b2b": "066.txt",
            "display remote-backup-profile rbp_main": "067.txt",
            "display remote-backup-profile rbp_vlan4054": "068.txt",
            "display remote-backup-service": "069.txt",
            "display remote-backup-service rbs_main": "070.txt",
            "display saved-configuration configuration": "071.txt",
            "display service-policy cache": "072.txt",
            "display service-policy configuration name redirect": "074.txt",
            ("display service-policy configuration name "
             "trusted_no_pay"): "075.txt",
            "display service-group configuration": "076.txt",
            "display ssh server status": "077.txt",
            "display static-user ip-address 203.0.113.110": "078.txt",
            "display static-user ip-address 203.0.113.195": "079.txt",
            "display static-user ip-address 203.0.113.196": "080.txt",
            "display telnet server status": "081.txt",
            "display value-added-service policy": "082.txt",
            "display value-added-service policy unlim_24_36mbps": "083.txt",
            "display value-added-service policy redirect": "084.txt",
            "display ip vpn-instance": "085.txt",
            "display ip vpn-instance BR_CORE_OAM interface": "086.txt",
            "display ip vpn-instance BR_OAM interface": "087.txt",
            "display ip vpn-instance BR_TECH interface": "088.txt",
            "display ip vpn-instance NETFLOW interface": "089.txt",
            "display bas-interface Eth-Trunk1.540": "090.txt",
            "display bas-interface Eth-Trunk1.3652": "091.txt",
            "display bas-interface Eth-Trunk1.3653": "092.txt",
            "display bas-interface Eth-Trunk1.6963878": "093.txt"
        }

        self.ip = '127.0.0.1'

    def send_commands(self, commands_list, *args, **kwargs):
        if not isinstance(commands_list, list):
            commands_list = [commands_list]
        result = ''
        if args or kwargs:
            pass
        for command in commands_list:
            filename = "tests/fixtures/" + self.commands[command]
            with open(filename) as src:
                mid = src.read()
            self.prompt = mid.split('\n')[-1]
            mid = mid.replace('\r\n', '\n').rstrip()
            result += mid
        return result
