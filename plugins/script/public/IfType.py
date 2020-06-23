# -*- coding: utf-8 -*-
import re


# 交换机端口 - 类型
def get_IfType(data):
    result = {"type": []}

    try:
        datalist = []
        for i in data.split('\n'):
            if i:
                res = re.search(r'IF-MIB::ifType.(\d+)\s+=\s+\w+:\s+(\w+)', i).groups()
                datalist.append(res)
        result['type'] = datalist
    except Exception as e:
        result['type'] = []

    return result
