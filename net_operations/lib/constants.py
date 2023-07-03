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

CONFIG_MODE = {
    'huawei': {
        'in': ['return', 'system-view'],
        'out': ['return']
    },
    'cisco': {
        'in': ['end', 'configure terminal'],
        'out': ['end']
    }
}

PAGINATION = {
    'huawei': {
        'on': ['return', 'screen-length {} temporary'],
        'off': ['return', 'screen-length 0 temporary']
    },
    'cisco': {
        'on': ['end', 'terminal length {}'],
        'off': ['end', 'terminal length 0']
    },
    'd-link': {
        'on': ['enable clipaging'],
        'off': ['disable clipaging']
    }
}

CX600_LICENSE = {
    'BRAS': {
        "LCX6BRAS09": {
            "type": "Resource",
            "description": "CX600 PPPoE/IPoE Function License for LPUI-240"
        },
        "LCX6BRAS08": {
            "type": "Resource",
            "description": "CX600 PPPoE/IPoE Function License for LPUI-120"
        },
        "LCX6BRAS07": {
            "type": "Resource",
            "description": "CX600 PPPoE/IPoE Function License for LPUI-101"
        },
        "LCX6BRAS06": {
            "type": "Resource",
            "description": "CX600 PPPoE/IPoE Function License for LPUI-51"
        },
        "LCX6BRAS05": {
            "type": "Resource",
            "description": "CX600 PPPoE/IPoE Function License for LPUF-240"
        },
        "LCX6BRAS04": {
            "type": "Resource",
            "description": "CX600 PPPoE/IPoE Function License for LPUF-120"
        },
        "LCX6BRAS03": {
            "type": "Resource",
            "description": "CX600 PPPoE/IPoE Function License for LPUF-101"
        },
        "LCX6BRAS02": {
            "type": "Resource",
            "description": "CX600 PPPoE/IPoE Function License for LPUF-51"
        },
        "LCX6BRAS01": {
            "type": "Resource",
            "description": "CX600 PPPoE/IPoE Function License for LPUF-40"
        },
        "LCX6BRAS00": {
            "type": "Resource",
            "description": "CX600 PPPoE/IPoE Function License for LPUF-21"
        },
        "LCX6BASUPG00": {
            "type": "Function",
            "description": "CX600 PPPoE/IPoE Function License"
        },
        "LCX6QS0100": {
            "type": "Resource",
            "description": "CX600 Subscribers Quantity(1k Subscribers)"
        }
    },
    'NAT': {
        "LCX6NAT6401": {
            "type": "Resource",
            "description": "CX600 NAT64 License for VSU Series Units"
        },
        "LCX6PCP01": {
            "type": "Resource",
            "description": "CX600 PCP license for VSU Series Units"
        },
        "LCX6DSLITE01": {
            "type": "Resource",
            "description": "CX600 DS-Lite Function License for VSU Series Units"
        },
        "LCX6L2NAT01": {
            "type": "Resource",
            "description": "CX600 L2NAT Function License for VSU Series Units"
        },
        "LCX64020G00": {
            "type": "Resource",
            "description": "CX600 20Gbps capacity License for VSU Series Units"
        },
        "LCX6DSLITEDS00": {
            "type": "Resource",
            "description": "CX600 DS-Lite License for VSUI-20-A"
        },
        "LCX6L2NATDS00": {
            "type": "Resource",
            "description": "CX600 L2NAT License for VSUI-20-A"
        },
        "LCX6NATDS00": {
            "type": "Resource",
            "description": "CX600 2M NAT Session License"
        },
    },
    'HA': {
        "LCX6MHAG00": {
            "type": "Function",
            "description": "CX600 Cross-chassis HAG Function License"
        }
    },
    'L3VPN': {
        "LCX6BTOA06": {
            "type": "Resource",
            "description": "CX600 L3VPN Function License for LPUF-240-B"
        },
        "LCX6BTOA05": {
            "type": "Resource",
            "description": "CX600 L3VPN Function License for LPUI-240-B"
        },
        "LCX6BTOA08": {
            "type": "Resource",
            "description": "CX600 L3VPN Function License for LPUF-120-B"
        },
        "LCX6BTOA07": {
            "type": "Resource",
            "description": "CX600 L3VPN Function License for LPUI-120-B"
        },
        "LCX6BTOA04": {
            "type": "Resource",
            "description": "CX600 L3VPN Function License for LPUI-101-B"
        },
        "LCX6BTOA03": {
            "type": "Resource",
            "description": "CX600 L3VPN Function License for LPUF-101-B"
        },
        "LCX6BTOA02": {
            "type": "Resource",
            "description": "CX600 L3VPN Function License for LPUI-51-B"
        },
        "LCX6BTOA01": {
            "type": "Resource",
            "description": "CX600 L3VPN Function License for LPUF-51-B"
        },
        "LCX6BTOA00": {
            "type": "Resource",
            "description": ("CX600 LPUF-40-B Upgrade to LPUF-40-A License"
                            "(L3VPN,Ability of MVPN,IPv6 Enhanced)")
        },
        "LCX6KBEN06": {
            "type": "Resource",
            "description": ("CX600 LPUF-21-B Upgrade to LPUF-21-A License"
                            "(IPv6,L3VPN,MVPN)")
        },
    }
}
