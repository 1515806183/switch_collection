# -*- coding: utf-8 -*-


# 设备名称
def get_sysDescr(data):
    result = {}
    sys_name = data.strip('\n').split(' ')
    if sys_name and len(sys_name) > 2:
        result['sysName'] = sys_name[3]

    return result