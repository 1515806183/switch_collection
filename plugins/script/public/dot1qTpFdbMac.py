# -*- coding: utf-8 -*-
"""
 根据 SNMPv2-SMI （1dBasePortIfIndex,1qTpFdbMac,1qTpFdbPort）信息获取交换机的mac地址（逻辑端口
 SNMPv2-SMI::mib-2.17.4.3.1.1.148.198.145.16.83.151 = Hex-STRING: 94 C6 91 10 53 97
            SNMPv2-SMI::mib-2.17.4.3.1.1.188.241.242.91.162.1 = Hex-STRING: BC F1 F2 5B A2 01
            SNMPv2-SMI::mib-2.17.4.3.1.1.148.198.145.16.83.97 = Hex-STRING: 94 C6 91 10 53 61

            SNMPv2-SMI::mib-2.17.4.3.1.1.96.46.32.41.47.176 = Hex-STRING: 60 2E 20 29 2F B0
            SNMPv2-SMI::mib-2.17.4.3.1.1.96.46.32.41.48.32 = STRING: "`. )0 "
            SNMPv2-SMI::mib-2.17.4.3.1.1.96.46.32.41.48.48 = STRING: "`. )00"
            SNMPv2-SMI::mib-2.17.4.3.1.1.96.46.32.41.48.160 = Hex-STRING: 60 2E 20 29 30 A0
            SNMPv2-SMI::mib-2.17.4.3.1.1.96.46.32.41.49.80 = STRING: "`. )1P"
            SNMPv2-SMI::mib-2.17.4.3.1.1.96.46.32.41.49.112 = STRING: "`. )1p"
            SNMPv2-SMI::mib-2.17.4.3.1.1.96.46.32.41.49.208 = Hex-STRING: 60 2E 20 29 31 D0
            SNMPv2-SMI::mib-2.17.4.3.1.1.96.46.32.41.52.32 = STRING: "`. )4 "
            SNMPv2-SMI::mib-2.17.4.3.1.1.96.46.32.41.52.80 = STRING: "`. )4P"
            SNMPv2-SMI::mib-2.17.4.3.1.1.100.0.106.195.141.124 = Hex-STRING: 64 00 6A C3 8D 7C
"""
import re


# 取出端口和mac地址
def get_dot1qTpFdbMac(data):
    #     data =  '''
    # SNMPv2-SMI::mib-2.17.4.3.1.1.0.7.235.48.64.193 = Hex-STRING: 00 07 EB 30 40 C1
    # SNMPv2-SMI::mib-2.17.4.3.1.1.0.36.129.226.25.136 = Hex-STRING: 00 24 81 E2 19 88
    # SNMPv2-SMI::mib-2.17.4.3.1.1.0.80.86.136.35.160 = Hex-STRING: 00 50 56 88 23 A0
    # SNMPv2-SMI::mib-2.17.4.3.1.1.0.80.86.152.0.8 = Hex-STRING: 00 50 56 98 00 08

    res = {"dot1qTpFdbMac": {}}

    if 'No Such' not in data:
        dot1qTpFdbMac = re.findall(r'SNMPv2-SMI::mib-2.17.4.3.1.1.(.*)', data)
        res["dot1qTpFdbMac"] = dot1qTpFdbMac

    # 要根据dot1dBasePortIfIndex dot1qTpFdbPort数据才能处理，所有把他放在最后数据处理
    return res
