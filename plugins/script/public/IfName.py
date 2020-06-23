# -*- coding: utf-8 -*-
import re


# 设备名称
def get_ifName(data):
    result = {"ifName": []}

    try:
        datalist = []
        for i in data.split('\n'):
            if i:
                res = re.search(r'IF-MIB::ifName.(\d+)\s+=\s+\w+:\s+(\w+)', i).groups()
                datalist.append(res)
        result['ifName'] = datalist
    except Exception as e:
        result['ifName'] = []

    return result