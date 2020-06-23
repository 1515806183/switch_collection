# -*- coding: utf-8 -*-
"""
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10101 = INTEGER: 254
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10102 = INTEGER: 254
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10103 = INTEGER: 254
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10104 = INTEGER: 254
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10105 = INTEGER: 254
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10106 = INTEGER: 254
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10107 = INTEGER: 254
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10108 = INTEGER: 254
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10109 = INTEGER: 254
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10110 = INTEGER: 254
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10111 = INTEGER: 254
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10112 = INTEGER: 254
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10113 = INTEGER: 81
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10114 = INTEGER: 81
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10115 = INTEGER: 81
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10116 = INTEGER: 81
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10117 = INTEGER: 81
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10118 = INTEGER: 81
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10119 = INTEGER: 81
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10120 = INTEGER: 81
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10121 = INTEGER: 81
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10122 = INTEGER: 81
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10125 = INTEGER: 1
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10126 = INTEGER: 1
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10127 = INTEGER: 1
SNMPv2-SMI::enterprises.9.9.68.1.2.2.1.2.10128 = INTEGER: 1

"""
import re


# vlan
def get_vmVlan(data):
    vmVlan_dict = {
        "cisco_vmVlan": {}
    }

    # 判断是否真的采集
    if 'No Such' not in data:
        for i in str(data).split('\n'):
            if i:
                vmVlan = re.search(r'9.9.68.1.2.2.1.2.(\d+)\s+=\s+INTEGER:\s+(\d+)', i)
                serial_num = vmVlan.group(1)  # 1061 1062
                serial_int = vmVlan.group(2)  # 1061 1062
                one_serial = {serial_num: serial_int}
                vmVlan_dict['cisco_vmVlan'].update(one_serial)
    return vmVlan_dict