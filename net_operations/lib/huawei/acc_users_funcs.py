import re


def check_hw_value(value, abscence='-'):
    return value if value != abscence else None


def get_huawei_domains(conn) -> dict:
    domains = {}
    output = conn.send_commands('display domain')
    reg = re.compile(r" +(\S+) +\S+ +\d+ +\d+ +(\d+)")
    for item in reg.finditer(output):
        name, online = item.groups()
        domains.update({name: {'online': online}})
    return domains


def get_huawei_domain_info(conn, domain) -> dict:
    command = f'display domain {domain}'
    output = conn.send_commands(command)
    r_authen_sch = r'Authentication-scheme-name +: +(\S+)'
    r_acct_sch = r'Accounting-scheme-name +: +(\S+)'
    r_author_sch = r'Authorization-scheme-name +: +(\S+)'
    r_online = r'Online-number +: +(\S+)'
    r_dns_ipv4 = r'DNS-IP-address +: +(\S+)'
    r_dns_ipv6 = r'DNS-IPV6-address +: +(\S+)'
    r_redirect = r'Web-URL +: +(\S+)'
    r_radius = r'RADIUS-server-template +: +(\S+)'
    r_tacacs = r'HWTACACS-server-template +: +(\S+)'
    r_ip_pool = r'IP-address-pool-name +: +(\S+)'
    r_nat_ug = r'User-group nat +: +(\S+), +.*'
    r_nat_inst = r'User-group nat +: +\S+, +(\S+),'
    regexps = [
        ("authen_scheme", r_authen_sch),
        ("account_scheme", r_acct_sch),
        ("author_scheme", r_author_sch),
        ("online", r_online),
        ("redirect_url", r_redirect),
        ("radius_server", r_radius),
        ("tacacs_server", r_tacacs),
        ("default_ip_pool", r_ip_pool),
        ("nat_user_group", r_nat_ug),
        ("nat_instance", r_nat_inst)
    ]
    info_dict = {}
    for key, regexp in regexps:
        reg = re.compile(regexp)
        if reg.search(output):
            info_dict[key] = check_hw_value(reg.search(output).group(1))
    reg4 = re.compile(r_dns_ipv4)
    reg6 = re.compile(r_dns_ipv6)
    for dns4 in reg4.finditer(output):
        dns = dns4.group(1)
        info_dict.setdefault('dns_ipv4', []).append(check_hw_value(dns))
    for dns6 in reg6.finditer(output):
        dns = dns6.group(1)
        info_dict.setdefault('dns_ipv6', []).append(check_hw_value(dns))
    return {domain: info_dict}


def get_huawei_bas_interfaces(conn) -> dict:
    r_bas_line = r'(\S+) +(\S+) +\S+ +(\d+)'
    bas_intf_dict = {}
    output = conn.send_commands('display bas-interface')
    for item in re.finditer(r_bas_line, output):
        bas, type_, online = item.groups()
        bas_intf_dict.update({bas: {'type': type_, 'online': online}})
    return bas_intf_dict


def get_huawei_bas_intf_info(conn, bas_intf) -> dict:
    r_preauth = r'Pre-authentication default domain +: +(\S+)'
    r_authen = r'Authentication default domain +: +(\S+)'
    r_authen_method = r'Authentication method +: +\[(\S+)\]'
    r_opt82 = r'Client option82 +: +(\S+)'
    r_vrf = r'Vpn Instance +: +(\S+)'
    basif_list = [
        (r_preauth, 'preauth_domain', None),
        (r_authen, 'authen_domain', None),
        (r_authen_method, 'authen_method', None),
        (r_opt82, 'opt82', None),
        (r_vrf, 'vrf', None),
    ]
    command = f'display bas-interface {bas_intf}'
    output = conn.send_commands(command)
    info_dict = {}
    for regexp, key, default in basif_list:
        searched = re.search(regexp, output)
        if searched:
            info_dict[key] = check_hw_value(searched.group(1))
        else:
            info_dict[key] = default
    return {bas_intf: info_dict}
