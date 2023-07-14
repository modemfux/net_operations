# Remarks

## BAS Report

```python
final_dict = {
    "total_users": {
        "ipv4": {
            "normal": "100",
            "rui_local": "500",
            "rui_remote": "400",
            "radius_auth": "900",
            "no_auth": "100",
            "total": "1000"
        },
        "ipv6": {
            "normal": "0",
            "rui_local": "0",
            "rui_remote": "0",
            "radius_auth": "0",
            "no_auth": "0",
            "total": "0"
        }
    },
    "licenses": [
        {
            "name": "LCX6QS0100",
            "description": "CX600 Subscribers Quantity(1k Subscribers)",
            "type": "Resource",
            "qty": "10"
        },
        {
            "name": "LCX6BASUPG00",
            "description": "CX600 PPPoE/IPoE Function License",
            "type": "Function",
            "qty": "1"
        }
    ],
    "bas_interfaces": [
        {
            "name": "Eth-Trunk1.505",
            "preauth_domain": "dom_zappa",
            "authen_domain": "dom_ipoe_main",
            "authen_method": "bind",
            "vrf": "GRT",
            "static_qty": "0",
            "rbp_name": "rbp_main"
        },
        {
            "name": "Eth-Trunk1.520",
            "preauth_domain": "-",
            "authen_domain": "dom_ipoe_main",
            "authen_method": "bind",
            "vrf": "GRT",
            "static_qty": "0"
        }
    ],
    "domains_info": [
        {
            "name": "dom_ipoe_main",
            "online": "1000",
            "authen_scheme": "authen_xrad",
            "account_scheme": "acct_xrad",
            "radius_server": "xrad-radius",
            "redirect_url": "http://8.8.8.8",
            "default_ip_pool": "pool_nat",
            "nat_user_group": "ug_main",
            "nat_instance": "ni_main"
        }
    ],
    "radius_info": [
        {
            "authen_servers": [
                {
                    "ip": "10.0.0.151",
                    "port": "1812",
                    "weight": "100",
                    "vrf": "BR_TECH"
                },
                {
                    "ip": "10.0.0.152",
                    "port": "1812",
                    "weight": "50",
                    "vrf": "BR_TECH"
                },
                {
                    "ip": "10.0.0.153",
                    "port": "1812",
                    "weight": "0",
                    "vrf": "BR_TECH"
                },
                {
                    "ip": "10.0.0.140",
                    "port": "1812",
                    "weight": "0",
                    "vrf": "BR_TECH"
                }
            ],
            "account_servers": [
                {
                    "ip": "10.0.0.151",
                    "port": "1813",
                    "weight": "100",
                    "vrf": "BR_TECH"
                },
                {
                    "ip": "10.0.0.152",
                    "port": "1813",
                    "weight": "50",
                    "vrf": "BR_TECH"
                },
                {
                    "ip": "10.0.0.153",
                    "port": "1813",
                    "weight": "0",
                    "vrf": "BR_TECH"
                }
            ],
            "src_interface": "LoopBack12",
            "call_station_id": "mac",
            "name": "xrad-radius"
        }
    ]
}
```

### BAS License table's columns width

- License = 13
- Description = 49
- Type = 8
- Qty = 5

### BAS interfaces table's columns width

- BAS Interface = 21
- Preauthentication domain = 26
- Authentication domain = 26
- Method = 8
- GRT/VRF = 17
- RBP = 15
- Static users qty = 18
