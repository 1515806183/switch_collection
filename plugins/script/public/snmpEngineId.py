# -*- coding: utf-8 -*-
import re, time


# 启动时间
def get_snmpEngineId(data):
    """
    SNMP-FRAMEWORK-MIB::snmpEngineTime.0 = INTEGER: 192528781 seconds
    :param data:
    :return:
    """
    result = {}

    upTimeTxt = re.findall(r'SNMP-FRAMEWORK-MIB::snmpEngineTime.(.*)', data)
    if upTimeTxt:
        upTime_seconds = int(upTimeTxt[0].split(' ')[3])
        upTime_localTime = time.localtime(time.time() - upTime_seconds)
        dev_upTime = time.strftime("%Y-%m-%d %H:%M:%S", upTime_localTime)
        # dev_upTime = (datetime.datetime.now()-datetime.timedelta(seconds=days)).strftime('%Y-%m-%d %H:%M:%S')
    else:
        dev_upTime = ""

    result['upTime'] = dev_upTime
    return result