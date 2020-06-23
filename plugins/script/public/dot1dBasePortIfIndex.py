# -*- coding: utf-8 -*-
"""
 根据 SNMPv2-SMI （1dBasePortIfIndex,1qTpFdbMac,1qTpFdbPort）信息获取交换机的mac地址（逻辑端口

 cisco vlan 返回数据
            dot1dBasePortIfIndex 返回样例数据
                snmpwalk -v 2c -c zabbixread@401 185.40.1.3 1.3.6.1.2.1.17.4.3.1.2
                SNMPv2-SMI::mib-2.17.4.3.1.2.0.0.12.7.172.100 = INTEGER: 2315
                SNMPv2-SMI::mib-2.17.4.3.1.2.12.196.122.64.42.123 = INTEGER: 45
                SNMPv2-SMI::mib-2.17.4.3.1.2.12.196.122.64.42.135 = INTEGER: 46
                SNMPv2-SMI::mib-2.17.4.3.1.2.12.196.122.64.44.218 = INTEGER: 45
                SNMPv2-SMI::mib-2.17.4.3.1.2.12.196.122.64.44.242 = INTEGER: 46
                SNMPv2-SMI::mib-2.17.4.3.1.2.76.119.109.83.120.111 = INTEGER: 0
                SNMPv2-SMI::mib-2.17.4.3.1.2.76.119.109.91.158.239 = INTEGER: 2315
"""
import re


# 获取本地端口表
def get_dot1dBasePortIfIndex(data):
#     data = '''
# SNMPv2-SMI::mib-2.17.1.4.1.2.1 = INTEGER: 10101
# SNMPv2-SMI::mib-2.17.1.4.1.2.2 = INTEGER: 10102
# SNMPv2-SMI::mib-2.17.1.4.1.2.3 = INTEGER: 10103
# SNMPv2-SMI::mib-2.17.1.4.1.2.4 = INTEGER: 10104
# SNMPv2-SMI::mib-2.17.1.4.1.2.5 = INTEGER: 10105
# SNMPv2-SMI::mib-2.17.1.4.1.2.6 = INTEGER: 10106
# SNMPv2-SMI::mib-2.17.1.4.1.2.7 = INTEGER: 10107
# SNMPv2-SMI::mib-2.17.1.4.1.2.8 = INTEGER: 10108
# SNMPv2-SMI::mib-2.17.1.4.1.2.9 = INTEGER: 10109
# SNMPv2-SMI::mib-2.17.1.4.1.2.10 = INTEGER: 10110
# SNMPv2-SMI::mib-2.17.1.4.1.2.11 = INTEGER: 10111
# SNMPv2-SMI::mib-2.17.1.4.1.2.12 = INTEGER: 10112
# SNMPv2-SMI::mib-2.17.1.4.1.2.13 = INTEGER: 10113
# SNMPv2-SMI::mib-2.17.1.4.1.2.14 = INTEGER: 10114
# SNMPv2-SMI::mib-2.17.1.4.1.2.15 = INTEGER: 10115
# SNMPv2-SMI::mib-2.17.1.4.1.2.16 = INTEGER: 10116
# SNMPv2-SMI::mib-2.17.1.4.1.2.17 = INTEGER: 10117
# SNMPv2-SMI::mib-2.17.1.4.1.2.18 = INTEGER: 10118
# SNMPv2-SMI::mib-2.17.1.4.1.2.19 = INTEGER: 10119
# SNMPv2-SMI::mib-2.17.1.4.1.2.20 = INTEGER: 10120
# SNMPv2-SMI::mib-2.17.1.4.1.2.21 = INTEGER: 10121
# SNMPv2-SMI::mib-2.17.1.4.1.2.22 = INTEGER: 10122
# SNMPv2-SMI::mib-2.17.1.4.1.2.23 = INTEGER: 10123
# SNMPv2-SMI::mib-2.17.1.4.1.2.24 = INTEGER: 10124
# SNMPv2-SMI::mib-2.17.1.4.1.2.25 = INTEGER: 10125
# SNMPv2-SMI::mib-2.17.1.4.1.2.26 = INTEGER: 10126
# SNMPv2-SMI::mib-2.17.1.4.1.2.27 = INTEGER: 10127
# SNMPv2-SMI::mib-2.17.1.4.1.2.28 = INTEGER: 10128
# SNMPv2-SMI::mib-2.17.1.4.1.2.29 = INTEGER: 10129
# SNMPv2-SMI::mib-2.17.1.4.1.2.30 = INTEGER: 10130
# SNMPv2-SMI::mib-2.17.1.4.1.2.31 = INTEGER: 10131
# SNMPv2-SMI::mib-2.17.1.4.1.2.32 = INTEGER: 10132
# SNMPv2-SMI::mib-2.17.1.4.1.2.33 = INTEGER: 10133
# SNMPv2-SMI::mib-2.17.1.4.1.2.34 = INTEGER: 10134
# SNMPv2-SMI::mib-2.17.1.4.1.2.35 = INTEGER: 10135
# SNMPv2-SMI::mib-2.17.1.4.1.2.36 = INTEGER: 10136
# SNMPv2-SMI::mib-2.17.1.4.1.2.37 = INTEGER: 10137
# SNMPv2-SMI::mib-2.17.1.4.1.2.38 = INTEGER: 10138
# SNMPv2-SMI::mib-2.17.1.4.1.2.39 = INTEGER: 10139
# SNMPv2-SMI::mib-2.17.1.4.1.2.40 = INTEGER: 10140
# SNMPv2-SMI::mib-2.17.1.4.1.2.41 = INTEGER: 10141
# SNMPv2-SMI::mib-2.17.1.4.1.2.42 = INTEGER: 10142
# SNMPv2-SMI::mib-2.17.1.4.1.2.43 = INTEGER: 10143
# SNMPv2-SMI::mib-2.17.1.4.1.2.44 = INTEGER: 10144
# SNMPv2-SMI::mib-2.17.1.4.1.2.45 = INTEGER: 10145
# SNMPv2-SMI::mib-2.17.1.4.1.2.46 = INTEGER: 10146
# SNMPv2-SMI::mib-2.17.1.4.1.2.47 = INTEGER: 10147
# SNMPv2-SMI::mib-2.17.1.4.1.2.48 = INTEGER: 10148
# '''
    portIfDict = {"dot1dBasePortIfIndex": {}}  # portIfDict = {"1":"1",..."52":"52","53":"55"}
    if 'No Such' not in data:
        portIfList = re.findall(r'SNMPv2-SMI::mib-2.17.1.4.1.2.(.*)', data)

        # 取出端口和接口索引的关系
        for i in portIfList:
            idx = i.split()[0]
            If_idx = i.split()[3]
            data = {str(idx): str(If_idx)}
            portIfDict["dot1dBasePortIfIndex"].update(data)
    return portIfDict
