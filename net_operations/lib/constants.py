NAT_CARDS_CX600 = {
    'CR5DVSUF8010': {
        'cpus': {
            'cpu0': {
                'cpu_id': '0',
                'cpu_type': 'engine',
                'nat_bw_lic': False,
                'default_bw': 20
                }
            },
        'pics': {
            'pic0': {
                'cpu_id': '0',
                'cpu_type': 'card',
                'default_bw': 40
                }
            }
        },
    'CR5DVSUFD010': {
        'cpus': {
            'cpu0': {
                'cpu_id': '0',
                'cpu_type': 'engine',
                'nat_bw_lic': False,
                'default_bw': 20
                },
            'cpu1': {
                'cpu_id': '1',
                'cpu_type': 'engine',
                'nat_bw_lic': False,
                'default_bw': 20
                }
            },
        'pics': {
            'pic0': {
                'cpu_id': '0',
                'cpu_type': 'card',
                'default_bw': 40
                },
            'pic1': {
                'cpu_id': '1',
                'cpu_type': 'card',
                'default_bw': 40
                }
            }
        }
    }

INITIAL_COMMANDS = {
   'huawei': [
       'screen-length 0 temporary',
       'screen-width 512',
       'Y'
   ],
   'cisco': [
       'terminal length 0',
       'terminal width 512'
   ],
   'd-link': [
       'disable clipaging'
   ]
}
