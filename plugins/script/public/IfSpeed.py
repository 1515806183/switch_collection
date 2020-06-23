# -*- coding: utf-8 -*-
import re


# 交换机端口 - 协商速率
def get_IfSpeed(data):
    result = []

    IfOperStatus = re.findall(r'IF-MIB::ifSpeed.(.*)', data)
    for i in IfOperStatus:
        array_data = i.split(' ')
        if len(array_data) < 3:
            continue
        result.append((array_data[0], str(int(array_data[-1].split('(')[0]) / 1000000) + ' Mbps'))
    return {'speed': result}