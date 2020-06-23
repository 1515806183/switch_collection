# -*- coding: utf-8 -*-
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.6.10101.19 = STRING: "AP05"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.6.10102.12 = STRING: "AP06"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.6.10103.13 = STRING: "AP07"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.6.10104.21 = STRING: "AP08"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.6.10105.15 = STRING: "AP09"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.6.10106.14 = STRING: "AP10"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.6.10107.16 = STRING: "AP11"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.6.10108.18 = STRING: "AP01"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.6.10109.17 = STRING: "AP02"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.6.10110.22 = STRING: "AP03"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.6.10111.20 = STRING: "AP04"
import re


# 对端设备名称
def get_cdpCacheSysName(data):
    """
    10111 AP05
    :param data:
    :return:
    """
    serial_dict = {
        "cisco_remote_sys_name": {}
    }

    # 判断是否真的采集
    if 'No Such' not in data:
        for i in str(data).split('\n'):
            if i:
                serial = re.search(r'9.9.23.1.2.1.1.6.(\d+).\d+\s+=\s+STRING:\s+(.*)', i)
                num = serial.group(1)  # 10101 10102
                string = eval(serial.group(2))  # AP03 AP04

                one_data = {num: string}

                serial_dict['cisco_remote_sys_name'].update(one_data)

    return serial_dict

