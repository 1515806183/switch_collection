# -*- coding: utf-8 -*-
import re


# 交换机端口 - 管理状态 : up
def get_ifAdminStatus(data):
    result = []

    IfOperStatus = re.findall(r'IF-MIB::ifAdminStatus.(.*)', data)
    for i in IfOperStatus:
        array_data = i.split(' ')
        if len(array_data) < 3:
            continue
        result.append((array_data[0], str(array_data[-1]).split('(')[0]))

    return {'adminstatus': result}

