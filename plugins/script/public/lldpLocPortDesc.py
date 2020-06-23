# -*- coding: utf-8 -*-
import re


# lldpLocPortDesc
def get_lldpLocPortDesc(data):
    result = {}
    localPortList = re.findall(r'iso.0.8802.1.1.2.1.3.7.1.4.(.*)', data)
    localPortDic = {}
    for i in localPortList:
        idx = i.split(' ')[0]
        local_port = i.split(' ')[3].strip("\"")
        localPortDic[idx] = local_port

    result['localPortDic'] = localPortDic
    return result
