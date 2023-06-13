class DummyConnection:
    '''
    Dummy class for testing
    '''
    def __init__(self):
        self.outs = {
            'display nat instance': '',
            'display nat instance ni_main': '',
            'display service-location': '',
            'display service-location 1': '',
            'display service-instance-group': '',
            'display service-instance-group sig_main': '',
            'display nat statistics payload': '',
            'display nat statistics table slot 3 engine 0': '',
            'display license resource usage': '',
            'display nat session-table size': '',
            'display elabel brief': '',
            'display current-conf conf license': '',
            'display version slot 3': ''
        }

    def send_commands(self, commands_list):
        if not isinstance(commands_list, list):
            commands_list = [commands_list]
        result = ''
        for command in commands_list:
            result += self.outs[command]
        return result
