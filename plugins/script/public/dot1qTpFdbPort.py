# -*- coding: utf-8 -*-
"""
 根据 SNMPv2-SMI （1dBasePortIfIndex,1qTpFdbMac,1qTpFdbPort）信息获取交换机的mac地址（逻辑端口

 样例数据为:
            SNMPv2-SMI::mib-2.17.4.3.1.2.148.198.145.16.83.151 = INTEGER: 53
            SNMPv2-SMI::mib-2.17.4.3.1.2.188.241.242.91.162.1 = INTEGER: 53
            SNMPv2-SMI::mib-2.17.4.3.1.2.148.198.145.16.83.97 = INTEGER: 53
"""
import re


# 获取从某个端口学习到的MAC地址及端口索引
def get_dot1qTpFdbPort(data):
#     data = '''
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.7.235.48.64.193 = INTEGER: 31
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.36.129.226.25.136 = INTEGER: 47
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.136.35.160 = INTEGER: 47
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.0.8 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.8.94 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.20.106 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.21.150 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.35.225 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.40.147 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.41.88 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.46.31 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.48.160 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.51.45 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.51.57 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.60.81 = INTEGER: 47
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.83.21 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.87.142 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.96.186 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.98.232 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.99.170 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.105.53 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.114.231 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.118.67 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.123.121 = INTEGER: 47
# SNMPv2-SMI::mib-2.17.4.3.1.2.0.80.86.152.127.212 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.24.251.123.157.141.107 = INTEGER: 31
# SNMPv2-SMI::mib-2.17.4.3.1.2.28.152.236.45.103.250 = INTEGER: 47
# SNMPv2-SMI::mib-2.17.4.3.1.2.44.68.253.122.230.208 = INTEGER: 43
# SNMPv2-SMI::mib-2.17.4.3.1.2.48.228.219.179.34.152 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.48.228.219.179.34.203 = INTEGER: 48
# SNMPv2-SMI::mib-2.17.4.3.1.2.56.234.167.169.80.166 = INTEGER: 34
# SNMPv2-SMI::mib-2.17.4.3.1.2.64.242.233.220.188.19 = INTEGER: 47
# SNMPv2-SMI::mib-2.17.4.3.1.2.64.242.233.220.188.22 = INTEGER: 47
# SNMPv2-SMI::mib-2.17.4.3.1.2.68.30.161.67.232.196 = INTEGER: 35
# SNMPv2-SMI::mib-2.17.4.3.1.2.68.168.66.14.198.152 = INTEGER: 31
# SNMPv2-SMI::mib-2.17.4.3.1.2.80.154.76.173.65.44 = INTEGER: 31
# SNMPv2-SMI::mib-2.17.4.3.1.2.80.154.76.173.65.138 = INTEGER: 31
# SNMPv2-SMI::mib-2.17.4.3.1.2.84.159.53.10.154.12 = INTEGER: 31
# SNMPv2-SMI::mib-2.17.4.3.1.2.104.188.12.208.3.48 = INTEGER: 47
# SNMPv2-SMI::mib-2.17.4.3.1.2.104.188.12.208.3.64 = INTEGER: 47
# SNMPv2-SMI::mib-2.17.4.3.1.2.116.230.226.252.146.110 = INTEGER: 47
# SNMPv2-SMI::mib-2.17.4.3.1.2.128.24.68.232.255.176 = INTEGER: 31
# SNMPv2-SMI::mib-2.17.4.3.1.2.144.177.28.14.210.63 = INTEGER: 13
# SNMPv2-SMI::mib-2.17.4.3.1.2.148.24.130.109.152.148 = INTEGER: 31
# SNMPv2-SMI::mib-2.17.4.3.1.2.164.186.219.14.60.208 = INTEGER: 47
# SNMPv2-SMI::mib-2.17.4.3.1.2.184.42.114.223.239.95 = INTEGER: 47
# SNMPv2-SMI::mib-2.17.4.3.1.2.184.172.111.18.254.121 = INTEGER: 47
# SNMPv2-SMI::mib-2.17.4.3.1.2.188.48.91.240.244.16 = INTEGER: 17
# SNMPv2-SMI::mib-2.17.4.3.1.2.200.31.102.216.229.215 = INTEGER: 47
# SNMPv2-SMI::mib-2.17.4.3.1.2.208.148.102.11.209.32 = INTEGER: 31
# SNMPv2-SMI::mib-2.17.4.3.1.2.208.148.102.32.233.244 = INTEGER: 31
# SNMPv2-SMI::mib-2.17.4.3.1.2.212.174.82.145.32.223 = INTEGER: 29
# SNMPv2-SMI::mib-2.17.4.3.1.2.212.190.217.246.254.15 = INTEGER: 27
# SNMPv2-SMI::mib-2.17.4.3.1.2.224.7.27.237.110.216 = INTEGER: 31
# SNMPv2-SMI::mib-2.17.4.3.1.2.224.7.27.237.126.76 = INTEGER: 31
# '''
    
    macPortDict = {"dot1qTpFdbPort": {}}  # {"macPortDict": {"148.198.145.16.83.151":"53","188.241.242.91.162.1":"53","148.198.145.16.83.97":"53"}}
    if 'No Such' not in data:
        macPortList = re.findall(r'SNMPv2-SMI::mib-2.17.4.3.1.2.(.*)', data)
    
        # 取出端口和mac地址十进制之间的关系
        for i in macPortList:
            mac_idx = i.split(' ')[0]
            port_idx = i.split(' ')[3]
            macPortDict["dot1qTpFdbPort"][mac_idx] = port_idx
    return macPortDict
