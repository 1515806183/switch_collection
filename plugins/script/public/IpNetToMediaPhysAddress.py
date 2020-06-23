# -*- coding: utf-8 -*-
# IP-MIB::ipNetToMediaPhysAddress.54.172.24.42.29 = STRING: 60:da:83:41:e1:71

import re


# 处理ARP信息 （ MAC -> IP )
def get_IpNetToMediaPhysAddress(data):
    # 对端列表ip-mac表,mac_ip表获取
    dict_arp = {}
    ip_mac_result_info = {}

    IpNetToMediaPhysAddress = re.findall(r'.ipNetToMediaPhysAddress.(.*)', data)
    for i in IpNetToMediaPhysAddress:
        array_data = i.partition('.')[2].split(' ')
        if len(array_data) < 3:
            continue
        remote_ip = array_data[0]
        mac = mac_format(array_data[3])
        dict_arp[mac] = remote_ip
        ip_mac_result_info[remote_ip] = mac

    # print self.dict_arp  # {"mac": "ip", "mac": "ip"}
    # print self.ip_mac_result_info  # {"ip": "mac", "ip": "mac"}

    return {"ipNetToMediaPhysAddress": {"dict_arp": dict_arp, "ip_mac_result_info": ip_mac_result_info}}


# 格式化mac
def mac_format(mac):
    res = {}
    format_list = mac.split(':')
    num = 0
    # 根据':'分隔，若位数为1，则在前面补齐0
    for i in format_list:
        num += 1
        if len(i) == 1:
            res[num] = '0' + i
        elif len(i) == 2:
            res[num] = i
    mac_addr = res[1] + ':' + res[2] + ':' + res[3] + ':' + res[4] + ':' + res[5] + ':' + res[6]
    # 小写字母转换为大写
    return mac_addr.upper()