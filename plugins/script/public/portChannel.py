# -*- coding: utf-8 -*-

"""
iso.2.840.10006.300.43.1.2.1.1.13.1 = INTEGER: 0
...
iso.2.840.10006.300.43.1.2.1.1.13.50 = INTEGER: 0
iso.2.840.10006.300.43.1.2.1.1.13.51 = INTEGER: 55
iso.2.840.10006.300.43.1.2.1.1.13.52 = INTEGER: 55
"""
import re


# 处理聚合端口
def get_portChannel(data):
    # 聚合端口查询
    # data = '''
    #         iso.2.840.10006.300.43.1.2.1.1.13.10101 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10102 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10103 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10104 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10105 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10106 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10107 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10108 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10109 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10110 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10111 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10112 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10113 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10114 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10115 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10116 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10117 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10118 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10119 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10120 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10121 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10122 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10123 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10124 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10125 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10126 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10127 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10128 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10129 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10130 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10131 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10132 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10133 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10134 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10135 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10136 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10137 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10138 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10139 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10140 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10141 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10142 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10143 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10144 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10145 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10146 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10147 = INTEGER: 0
    # iso.2.840.10006.300.43.1.2.1.1.13.10148 = INTEGER: 0
    # '''
    portChannel = {"listPortChannel": [], "dictPortChannel": {}}

    listPortChannel = re.findall(r'iso.2.840.10006.300.43.1.2.1.1.13.(.*)', data)

    if not listPortChannel:
        return portChannel

    # cisco 返回字串为: No Such Instance currently exists at this OID
    # 其他设备返回: No Such Object available on this agent at this OID
    # print ' 该设备无聚合端口或不支持此聚合端口oid采集'
    if 'No Such' in listPortChannel[0]:
        return portChannel

    for i in listPortChannel:
        array_data = i.split()
        if len(array_data) < 3:
            continue
        idx_port = array_data[0]
        idx_channel = array_data[3]

        if portChannel.get("dictPortChannel").has_key(idx_channel):
            portChannel.get('dictPortChannel')[idx_channel].append({'portIndex': idx_port})
        else:
            portChannel.get('dictPortChannel')[idx_channel] = [{'portIndex': idx_port}]

    portChannel['listPortChannel'] = listPortChannel

    return {'portChannel': portChannel}