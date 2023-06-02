import copy
import re


def get_huawei_nat_configuration(conn) -> dict:

    '''
    Get from Huawei CX device with VSUF Service cards
    information about configured nat instances.
    Returns dict like this:
    {'ni_main':
        {'ni_id': '1',
         'nat-pools': ['81.23.175.0/25'],
         'limits':
            {'tcp': '2048',
             'udp': '2048',
             'icmp': '50',
             'total': '2048'},
         'ports':
            {'port-range': '256',
             'ext-port-range': '320',
             'ext-times': '3'},
         'sig': 'sig_main'
         },
     'ni_b2b_main':
        {'ni_id': '2',
         'nat-pools': ['85.140.40.251/32'],
         'limits':
            {'tcp': '1280',
             'udp': '1280',
             'icmp': '50',
             'total': '1280'},
         'ports':
            {'port-range': '256',
             'ext-port-range': '512',
             'ext-times': '2'},
    'sig': 'sig_main'
        }
    }
    '''

    # RegExps definitions
    reg_instance = r'nat instance (\S+) id (\d+)'
    reg_address = (r'section \d+ ((?:\d+[.]){3}(?:\d+)) mask '
                   r'(\d+(?:[ ]|(?:(?:\r)?\n))|(?:(?:\d+[.]){3}(?:\d+)))')
    reg_limits = r'nat session-limit (\S+) (\d+)'
    reg_ports = (r'port-range (\d+) '
                 r'(?:extended-port-range (\d+))?(?: extended-times (\d+))?')
    reg_sig = r'service-instance-group (\S+)'

    soft_nat_info = {}

    # output to search list of nat instances
    output = conn.send_commands(['display nat instance'])

    # for each nat instance filling data in soft_nat_info
    for item in re.finditer(reg_instance, output):
        ni_name, ni_id = item.groups()
        soft_nat_info[ni_name] = {'ni_id': ni_id}
        ni_out = conn.send_commands([f'display nat instance {ni_name}'])
        iter_add = re.finditer(reg_address, ni_out)
        if iter_add:
            add_groups = [f'{gr.group(1)}/{gr.group(2).rstrip()}'
                          for gr in iter_add]
            soft_nat_info[ni_name]['nat-pools'] = add_groups
        iter_limit = re.finditer(reg_limits, ni_out)
        if iter_limit:
            limits = {lim.group(1): lim.group(2) for lim in iter_limit}
            soft_nat_info[ni_name]['limits'] = limits
        search_ports = re.search(reg_ports, ni_out)
        if search_ports:
            pr, epr, et = search_ports.groups()
            soft_nat_info[ni_name]['ports'] = {'port-range': pr,
                                               'ext-port-range': epr,
                                               'ext-times': et}
        sig = re.search(reg_sig, ni_out)
        if sig:
            soft_nat_info[ni_name]['sig'] = sig.group(1)

    return soft_nat_info


def get_huawei_nat_physical_loc(conn) -> dict:

    '''
    Get from Huawei CX information about relationships between
    physical service VSUF cards and service-instance-locations.
    Return dict like this:
    {'1':
        {'id': '0',
         'sig': 'sig_main',
         'slot': '3',
         'type': 'engine'}
    }
    '''

    # RegExps definitions
    reg_ph_loc = r'Location slot ID: +(\S+) +(engine|card) ID: +(\S+)'
    reg_sl = r'service-location (\S+)'
    reg_sig = r'service-instance-group (\S+)'

    phys_nat_location = {}
    output = conn.send_commands(['display service-location'])

    for item in re.finditer(reg_sl, output):
        loc = item.group(1)
        check = conn.send_commands([f'display service-location {loc}'])
        phys = re.search(reg_ph_loc, check)
        if phys:
            slot, type_, id_ = phys.groups()
            phys_nat_location[loc] = {'slot': slot,
                                      'type': type_,
                                      'id': id_,
                                      'sig': None}

    sig_output = conn.send_commands(['display service-instance-group'])

    for sig_phy in re.finditer(reg_sig, sig_output):
        command = f'display service-instance-group {sig_phy.group(1)}'
        sig_loc_out = conn.send_commands([command])
        sig_loc_item = re.search(reg_sl, sig_loc_out)
        if sig_loc_item:
            number = sig_loc_item.group(1)
            phys_nat_location[number]['sig'] = sig_phy.group(1)

    return phys_nat_location


def get_huawei_nat_payload_stats(conn) -> list:

    '''
    Get from Huawei CX statistic information about NAT payload
    splitted by physical locations.
    Returns list like this:
    {'1':
    }
    '''

    # Defining regexps
    main = r'slot: +(?P<slot_num>\d+) (?P<type>card|engine): +(?P<type_num>\d+)'
    rx_pps = r'.*current receive packet speed\(pps\): +(?P<curr_rx_pps>\S+)'
    rx_bps = r'.*current receive packet bit speed\(bps\): +(?P<curr_rx_bps>\S+)'
    tx_pps = r'.*current transmit packet speed\(pps\): +(?P<curr_tx_pps>\S+)'
    tx_bps = (r'.*current transmit packet bit speed\(bps\):'
              r' +(?P<curr_tx_bps>\S+)')
    max_rx_pps = (r'.*historical maximum receive packet speed\(pps\):'
                  r' +(?P<hist_max_rx_pps>\S+)')
    mrp_date = (r'.*historical maximum receive packet speed time:'
                r' +(?P<hist_max_rx_pps_date>\S+ \S+)')
    max_rx_bps = (r'.*historical maximum receive packet bit speed\(bps\):'
                  r' +(?P<hist_max_rx_bps>\S+)')
    mrb_date = (r'.*historical maximum receive packet bit speed time:'
                r' +(?P<hist_max_rx_bps_date>\S+ \S+)')
    max_tx_pps = (r'.*historical maximum transmit packet speed\(pps\):'
                  r' +(?P<hist_max_tx_pps>\S+)')
    mtp_date = (r'.*historical maximum transmit packet speed time:'
                r' +(?P<hist_max_tx_pps_date>\S+ \S+)')
    max_tx_bps = (r'.*historical maximum transmit packet bit speed\(bps\):'
                  r' +(?P<hist_max_tx_bps>\S+)')
    mtb_date = (r'.*historical maximum transmit packet bit speed time:'
                r' +(?P<hist_max_tx_bps_date>\S+ \S)')
    reg_list = [
        rx_pps, rx_bps, rx_bps, tx_pps, tx_bps, max_rx_pps, mrp_date,
        max_rx_bps, mrb_date, max_tx_pps, mtp_date, max_tx_bps, mtb_date
        ]
    # Get raw data from device
    command = 'display nat statistics payload'
    output = conn.send_commands(command, waittime=3).lower()
    # Get first data with slot/cpu information
    main_list = [item.groupdict() for item in re.finditer(main, output)]
    # Add to each dict in main list additional key, value pairs from reg search
    for reg in reg_list:
        data = [reg_item.groupdict() for reg_item in re.finditer(reg, output)]
        for i in range(len(main_list)):
            main_list[i].update(data[i])
    copy_list = copy.deepcopy(main_list)
    # Add information with mbps rate for each instance
    for i in range(len(copy_list)):
        for key in copy_list[i].keys():
            if key.endswith('bps'):
                new_key = key.replace('bps', 'mbps')
                new_value = str(round(int(copy_list[i][key]) / 1024 / 1024, 3))
                main_list[i][new_key] = new_value
    return main_list


def get_huawei_nat_summary_statistic(conn, nat_phys_dict) -> dict:

    '''
    Get from Huawei CX summary table statistic information
    per NAT physical location.
    Returns dict like this:
    {'1': {'max_session_date': '2022-06-08 09:48:00',
           'max_session_qty': '1718823',
           'max_user_date': '2021-11-26 02:16:02',
           'max_user_qty': '7559',
           'total_session': '295432'}}
    '''

    res_dict = {}
    r_total_sess = (r'Total current nat444 sessions in Memory +'
                    r':(?P<total_session>\d+)')
    r_max_sess_qty = (r'Maximum session table number in history +'
                      r':(?P<max_session_qty>\d+)')
    r_max_sess_dat = (r'Maximum session table time in history +'
                      r':(?P<max_session_date>\S+ \S+)')
    r_max_user_qty = (r'Maximum user table number in history +'
                      r':(?P<max_user_qty>\d+)')
    r_max_user_dat = (r'Maximum user table time in history +'
                      r':(?P<max_user_date>\S+ \S+)')
    reg_list = [r_total_sess, r_max_sess_qty, r_max_sess_dat,
                r_max_user_qty, r_max_user_dat]
    for serv_loc in nat_phys_dict.keys():
        res_dict[serv_loc] = {}
        slot = nat_phys_dict[serv_loc]['slot']
        type_ = nat_phys_dict[serv_loc]['type'].lower()
        cpu_id = nat_phys_dict[serv_loc]['id']
        command = f'display nat statistics table slot {slot} {type_} {cpu_id}'
        output = conn.send_commands(command)
        for reg in reg_list:
            res_dict[serv_loc].update(re.search(reg, output).groupdict())
    return res_dict


def get_huawei_nat_session_license(conn):

    '''
    Get from Huawei CX information about NAT sessions
    licenses usage.
    Returns dict like this:
    {'distribution': {'per_cpu': [{'cpu_id': '0',
                                'cur_sess_qty': '2',
                                'slot': '3',
                                'type': 'engine'}],
                    'total': {'free': '2', 'total': '4', 'used': '2'}},
    'license': {'total': '2', 'used': '1'}}

    'license' contains information about LCX6NATDS00 license usage.

    'distribution' contains information about qty of NAT sessions
    available, used etc. 'total' contains summary information in
    millions units (i.e. 'free': '2' means that 2M sessions available).
    'per_cpu' contains list with dict with information per CPU basis.
    CPU there means service processor on VSUF card or SPxxx PIC in VSUF.
    '''

    res_dict = {'license': None,
                'distribution': {'total': None, 'per_cpu': []}}
    r_usage = r'.*LCX6NATDS00 +(?P<used>\d+)/(?P<total>\d+)'
    r_distr = (r' +(?P<slot>\d+) +(?P<cpu_id>\d)[(](?P<type>\S+)(?: +)?[)]'
               r' +(?P<cur_sess_qty>\d+) M')
    r_total = (r' *Total[ ]*Size *:(?P<total>\d+).*\n'
               r' *Used[ ]*Size *:(?P<used>\d+).*\n'
               r' *Free[ ]*Size *:(?P<free>\d+).*\n')
    output = conn.send_commands('display license resource usage')
    searched = re.search(r_usage, output)
    if searched:
        res_dict['license'] = searched.groupdict()
    output = conn.send_commands('display nat session-table size')
    searched = re.finditer(r_distr, output)
    if searched:
        for item in searched:
            res_dict['distribution']['per_cpu'].append(item.groupdict())
    searched = re.search(r_total, output)
    if searched:
        res_dict['distribution']['total'] = searched.groupdict()
    return res_dict


def get_huawei_nat_cards(conn):
    res_dict = {}
    r_vsu = r'VSU +(\d+) +\S+ +'
    r_vsuf = (r' *SDRAM Memory Size.*\n'
              r' *Flash Memory Size.*\n'
              r' *(\S+) version information')
    r_pic = (r' *(PIC\d): +Startup.*\n'
             r' *(\S+) version information.*\n')
    output = conn.send_commands('display elabel brief', waittime=4)
    lic_out = conn.send_commands('display current-conf conf license')
    for vsu in re.finditer(r_vsu, output):
        res_dict[vsu.group(1)] = {'board': None, 'pics': [],
                                  'bw_license': None}
    for slot in res_dict.keys():
        r_lic = fr' *active nat bandwith-enhance slot {slot} engine (\d)'
        output = conn.send_commands(f'display version slot {slot}')
        searched = re.search(r_vsuf, output)
        lic_search = re.search(r_lic, lic_out)
        if lic_search:
            engine = lic_search.group(1)
            res_dict[slot]['bw_license'] = f'engine {engine}'
        if searched:
            res_dict[slot]['board'] = searched.group(1)
        for pic in re.finditer(r_pic, output):
            res_dict[slot]['pics'].append(pic.groups())
    return res_dict
