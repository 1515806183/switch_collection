# -*- coding: utf-8 -*-
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.4.10101.19 = Hex-STRING: C0 A6 FE F7
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.4.10102.12 = Hex-STRING: C0 A6 FE F6
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.4.10103.13 = Hex-STRING: C0 A6 FE F3
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.4.10104.21 = Hex-STRING: C0 A6 FE FD
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.4.10105.15 = Hex-STRING: C0 A6 FE F9
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.4.10106.14 = Hex-STRING: C0 A6 FE FB
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.4.10107.16 = Hex-STRING: C0 A6 FE F8
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.4.10108.18 = Hex-STRING: C0 A6 FE FC
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.4.10109.17 = Hex-STRING: C0 A6 FE F4
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.4.10110.22 = Hex-STRING: C0 A6 FE FA
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.4.10111.20 = Hex-STRING: C0 A6 FE F5


import re
# 这里要到最后处理数据，因为要根据cisco_remote_sys_type == 1 这才是真正的IP


# 对端ip
def get_cdpCacheIP(data):
    serial_dict = {
        "cisco_remote_ip_not_deal": {}
    }

    # 判断是否真的采集
    if 'No Such' not in data:
        for i in str(data).split('\n'):
            if i:
                serial = re.search(r'9.9.23.1.2.1.1.4.(\d+).\d+\s+=\s+Hex-STRING:\s+(.*)', i)
                num = serial.group(1)  # 10101 10102
                integer = serial.group(2) # C0 A6 FE F5

                one_data = {num: integer}
                serial_dict['cisco_remote_ip_not_deal'].update(one_data)

    return serial_dict
