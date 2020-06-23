# -*- coding: utf-8 -*-
import re

# 换机端口 - 物理地址 MAC 地址 或 0.0.0.0
def get_ifPhysAddress(data):
    result = []

    IfOperStatus = re.findall(r'IF-MIB::ifPhysAddress.(.*)', data)
    for i in IfOperStatus:
        array_data = i.split(' ')
        if len(array_data) < 3:
            continue
        result.append((array_data[0], str(array_data[-1]).split('(')[0]))

    return {'macaddr': result}
