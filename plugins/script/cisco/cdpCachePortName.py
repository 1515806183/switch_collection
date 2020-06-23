# -*- coding: utf-8 -*-
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.7.10101.19 = STRING: "GigabitEthernet0"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.7.10102.12 = STRING: "GigabitEthernet0"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.7.10103.13 = STRING: "GigabitEthernet0"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.7.10104.21 = STRING: "GigabitEthernet0"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.7.10105.15 = STRING: "GigabitEthernet0"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.7.10106.14 = STRING: "GigabitEthernet0"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.7.10107.16 = STRING: "GigabitEthernet0"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.7.10108.18 = STRING: "GigabitEthernet0"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.7.10109.17 = STRING: "GigabitEthernet0"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.7.10110.22 = STRING: "GigabitEthernet0"
# SNMPv2-SMI::enterprises.9.9.23.1.2.1.1.7.10111.20 = STRING: "GigabitEthernet0"
import re


# 对端端口名称
def get_cdpCachePortName(data):
    serial_dict = {
        "cisco_remote_portName": {}
    }

    # 判断是否真的采集
    if 'No Such' not in data:
        for i in str(data).split('\n'):
            if i:
                serial = re.search(r'9.9.23.1.2.1.1.7.(\d+).\d+\s+=\s+STRING:\s+(.*)', i)
                num = serial.group(1)  # 10101 10102
                string = eval(serial.group(2))  # GigabitEthernet0

                one_data = {num: string}

                serial_dict['cisco_remote_portName'].update(one_data)

    return serial_dict
