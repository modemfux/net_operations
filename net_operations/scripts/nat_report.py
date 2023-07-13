import sys
from datetime import datetime
from net_operations.lib.funcs import generate_from_template
from net_operations.lib.huawei.nat_funcs import get_nat_report_dict
from net_operations.lib.classes.NetOperations import NetOperations


def main():

    if sys.argv[1:3]:
        ip, vendor = sys.argv[1:3]
    else:
        ip = input('Введите IP-адрес устройства: ')
        vendor = input('Введите имя вендора устройства: ').lower()

    conn = NetOperations(ip, vendor)
    try:
        conn.establish_connection()
        report_dic = get_nat_report_dict(conn)
        report_str = generate_from_template('templates/nat_report.md.jinja2',
                                            report_dic)
        time = str(datetime.now()).replace(' ', '_').replace(':', '.')
        filename = f'{time}_{ip}.md'
        with open(filename, 'w') as dst:
            dst.write(report_str)
        print(f'Report for {ip} saved as {filename}.')
    except Exception as error:
        print('Something gone wrong.')
        print(f'Error is "{error}"')


if __name__ == '__main__':
    main()
