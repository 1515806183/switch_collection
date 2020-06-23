# -*- coding: utf-8 -*-
import re


#  交换机端口 - MTU : 9600 或 1500
def get_IfMTU(data):
    result = []

    IfOperStatus = re.findall(r'IF-MIB::ifMtu.(.*)', data)
    for i in IfOperStatus:
        array_data = i.split(' ')
        if len(array_data) < 3:
            continue
        result.append((array_data[0], str(array_data[-1]).split('(')[0]))
    return {'mtu': result}