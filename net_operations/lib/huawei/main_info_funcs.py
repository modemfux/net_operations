import re


def get_hw_license_list(conn):
    output = conn.send_commands(['display license'])
    r_lic = (r"(?P<name>\S+) +(?P<type>Function|Resource) +"
             r"(?P<qty>\S+) +(?P<description>(?:\S+ ?)+)")
    reg = re.compile(r_lic)
    licenses = []
    for item in reg.finditer(output):
        lic_dict = item.groupdict()
        if lic_dict.get('qty').lower() == 'yes':
            lic_dict['qty'] = '1'
        licenses.append(lic_dict)
    return licenses
