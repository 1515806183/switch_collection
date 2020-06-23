# -*- coding: utf-8 -*-
import re


# 交换机端口 - 状态 : up/down
def get_IfOperStatus(data):
    result = []

    IfOperStatus = re.findall(r'IF-MIB::ifOperStatus.(.*)', data)
    for i in IfOperStatus:
        array_data = i.split(' ')
        if len(array_data) < 3:
            continue
        result.append((array_data[0], str(array_data[-1]).split('(')[0]))

    return {'operstatus': result}
