# -*- coding: utf-8 -*-

# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.3.10101.19 = INTEGER: 1
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.3.10102.12 = INTEGER: 1
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.3.10103.13 = INTEGER: 1
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.3.10104.21 = INTEGER: 1
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.3.10105.15 = INTEGER: 1
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.3.10106.14 = INTEGER: 1
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.3.10107.16 = INTEGER: 1
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.3.10108.18 = INTEGER: 1
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.3.10109.17 = INTEGER: 1
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.3.10110.22 = INTEGER: 1
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.3.10111.20 = INTEGER: 1

import re


# 对端设备类型
def get_cdpCacheType(data):
    serial_dict = {
        "cisco_remote_sys_type": {}
    }

    # 判断是否真的采集
    if 'No Such' not in data:
        for i in str(data).split('\n'):
            if i:
                serial = re.search(r'9.9.23.1.2.1.1.3.(\d+).\d+\s+=\s+INTEGER:\s+(.*)', i)
                num = serial.group(1)  # 10101 10102
                integer = eval(serial.group(2))  # 1

                one_data = {num: integer}

                serial_dict['cisco_remote_sys_type'].update(one_data)
    return serial_dict
