#!/usr/local/easyops/python/bin/python
# -*- coding: UTF-8 -*-
# -----author：shekshi---
# 已验证型号【CISCO：N77-C7706、WS-C3560G-48TS-S、WS-C2960G-48TC-L】
import os
import json
import requests
import sys
import re
import subprocess
import threading
from time import sleep, ctime

reload(sys)
sys.setdefaultencoding("utf-8")
# CMDB组件所在机器ip
EASYOPS_CMDB_HOST = '192.166.14.162'

headers_cmdb = {
    "host": "cmdb_resource.easyops-only.com",
    "content-Type": "application/json",
    "user": "easyops",
    "org": '3120'
}

# 设置json_data(自动发现需要传的json)为全局变量，多线程的结果append至json_data
json_data = []
port_json_data = []
# community = 'sxtsoft'
community = 'sxtsoft'


# 设备oid列表
def oid_list():
    oid_info = {
        'public_oid': {
            'sysDescr': '1.3.6.1.2.1.1.1.0',
            'sysName': '1.3.6.1.2.1.1.5.0',
            'IfDescr': '1.3.6.1.2.1.2.2.1.2',
            'IfName': '1.3.6.1.2.1.31.1.1.1.1',
            'IfType': '.1.3.6.1.2.1.2.2.1.3',
            'IfOperStatus': '.1.3.6.1.2.1.2.2.1.8',
            'IfAdminStatus': '.1.3.6.1.2.1.2.2.1.7',
            'IfPhysAddress': '.1.3.6.1.2.1.2.2.1.6',
            'IfSpeed': '.1.3.6.1.2.1.2.2.1.5',
            'IfMTU': '.1.3.6.1.2.1.2.2.1.4',
            'IpNetToMediaPhysAddress': '.1.3.6.1.2.1.4.22.1.2',
            'dot1dBasePortIfIndex': '1.3.6.1.2.1.17.1.4.1.2',
            'dot1qTpFdbPort': '1.3.6.1.2.1.17.4.3.1.2',
            'dot1qTpFdbMac': '1.3.6.1.2.1.17.4.3.1.1',
            'portChannel': 'iso.2.840.10006.300.43.1.2.1.1.13',
            'lldpRemEntry': '1.0.8802.1.1.2.1.4.1.1',
            'serial': '1.3.6.1.2.1.47.1.1.1.1.11',
        },
        'cisco_oid': {
            'vmVlan': '.1.3.6.1.4.1.9.9.68.1.2.2.1.2',
            'cdpCacheSysName': '1.3.6.1.4.1.9.9.23.1.2.1.1.6',
            'cdpCachePortName': '1.3.6.1.4.1.9.9.23.1.2.1.1.7',
            'cdpCacheType': '1.3.6.1.4.1.9.9.23.1.2.1.1.3',  # 若为1，则cdpCacheIP为ip
            'cdpCacheIP': '1.3.6.1.4.1.9.9.23.1.2.1.1.4',
            'cisco_serial': '1.3.6.1.2.1.47.1.1.1.1.11',
            'cisco_module': '1.3.6.1.2.1.47.1.1.1.1.13',
        }
    }
    return oid_info


def collect_info(ip, community, oid_info):
    # 判断使用什么oid
    result = {}
    for oid_key in oid_list():
        if oid_info == oid_key:
            oid = oid_list()[oid_key]
            for oid_key in oid:
                oid_res = oid_key
                oid_res, code = snmp_collect(ip, community, oid[oid_key])
                if code == 0:
                    code_back = 0
                    result[oid_key] = oid_res
                else:
                    code_back = 1
                    result = {'msg': oid_res}
                    return code_back, result
    return code_back, result


ip_mac_result_info = {}


# 采集交换机信息，并解析
def collect_netd(page, info_list1):
    # info_list = switch_ip_collect('NETD')[page]
    # info_list = [{"ip": "192.166.255.11"}]
    info_list = [{"ip": "192.166.255.15"}]

    try:
        lock.acquire()
        # print page_i,':'
        for info_ip in info_list:
            try:
                # 采集的数据存入result
                result = {}
                netport_relation = []
                if info_ip.has_key('ip'):
                    code_back, oid_info = collect_info(info_ip['ip'], community, 'public_oid')
                    if code_back == 0:
                        # print '采集设备',info_ip['ip'],'...'
                        # 基本信息采集--------------------------------
                        result['ip'] = info_ip['ip']
                        # 数据解析————用分隔符解析数据（空格）
                        sys_descr = oid_info['sysDescr'].strip('\n').split(' ')
                        if 'PowerConnect' == sys_descr[3]:
                            brand = 'DELL'
                        else:
                            brand = sys_descr[3]
                        # 品牌
                        result['brand'] = brand
                        # 若设备为DELL
                        if brand.upper() == 'DELL':
                            result['software_version'] = \
                            re.findall(r'.sysDescr.0 = STRING: (.*)', oid_info['sysDescr'])[0].split(',')[1].replace(
                                ',', '')
                        # 软件版本
                        # result['software_version'] = sys_descr[10].strip(',')
                        elif brand.upper() == 'H3C':
                            result['software_version'] = oid_info['sysDescr'].split(' ')[-1]
                        else:
                            result['software_version'] = \
                            re.findall(r'.Version (.*)', oid_info['sysDescr'])[0].split(' ')[0].replace(',', '')
                        # 设备名称
                        sys_name = oid_info['sysName'].strip('\n').split(' ')
                        result['name'] = sys_name[3]

                        sys_descr = oid_info['sysDescr'].strip('\n').split(' ')

                        if brand.upper() == 'H3C':
                            # result['module'] = oid_info['sysDescr'].split('\n')[1].split(' ')[1].strip('\r')
                            result['module'] = oid_info['sysDescr'].split(' ')[-1]
                        elif brand.upper() == 'HUAWEI':
                            result['module'] = sys_descr[13].strip('(')

                        serial = re.findall(r'.STRING: "(.*)"', oid_info['serial'])
                        # print serial
                        result['sn'] = serial[0]

                        ####################     基本信息   ######################################
                        # {'ip': '192.166.255.16', 'brand': 'Cisco', 'name': 'GBZX-SW-ACCESS-C2960X-006', 'software_version': '15.2(2)E7', 'sn': 'FOC2320T06B'}
                        ##########################################################

                        # print serial[0]
                        # net_serial=oid_info['cisco_serial'].strip('\n').split(' ')
                        # result['sn'] = net_serial[3].strip('"').split('"')[0]
                        # 端口信息采集---------------------------------
                        res_If = {}
                        # 网络接口信息描述,oid=.1.3.6.1.2.1.2.2.1.2
                        IfName = re.findall(r'IF-MIB::ifDescr.(.*)', oid_info['IfDescr'])
                        index_max_len = 0
                        for port_info in IfName:
                            port_index = port_info.split()[0]
                            len_portIndex = len(port_index)
                            if len_portIndex > index_max_len:
                                index_max_len = len_portIndex
                        for i in IfName:
                            IfName_info = i.split(' ')
                            # 端口标识 取‘设备名称’+‘/端口index’
                            netd_port_logo = sys_name[3] + '/' + str(IfName_info[0].zfill(index_max_len))
                            # 端口名
                            if_name = IfName_info[3]
                            res_If[IfName_info[0]] = {'name': netd_port_logo, 'if_name': if_name}

                            # 网络设备-网络设备端口，关系处理
                            netport_relation.append({'name': netd_port_logo})
                        result['NETDPORT'] = netport_relation
                        IfType = re.findall(r'IF-MIB::ifType.(.*)', oid_info['IfType'])
                        for i in IfType:
                            IfType_info = i.split(' ')
                            # 类型，去掉括号里的内容
                            res_If[IfType_info[0]]['type'] = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", IfType_info[3])
                            # res_If[IfType_info[0]]['type'] = IfType_info[3]
                        IfOperStatus = re.findall(r'IF-MIB::ifOperStatus.(.*)', oid_info['IfOperStatus'])
                        for i in IfOperStatus:
                            IfOperStatus_info = i.split(' ')
                            # 连接状态，去掉括号里的内容
                            res_If[IfOperStatus_info[0]]['oper_status'] = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "",
                                                                                 IfOperStatus_info[3])
                            # res_If[IfOperStatus_info[0]]['oper_status'] = IfOperStatus_info[3]
                        IfAdminStatus = re.findall(r'IF-MIB::ifAdminStatus.(.*)', oid_info['IfAdminStatus'])
                        for i in IfAdminStatus:
                            IfAdminStatus_info = i.split(' ')
                            # 管理状态，去掉括号里的内容
                            res_If[IfAdminStatus_info[0]]['admin_status'] = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "",
                                                                                   IfAdminStatus_info[3])
                            # res_If[IfAdminStatus_info[0]]['admin_status'] = IfAdminStatus_info[3]
                        IfPhysAddress = re.findall(r'IF-MIB::ifPhysAddress.(.*)', oid_info['IfPhysAddress'])
                        for i in IfPhysAddress:
                            IfPhysAddress_info = i.split(' ')
                            # 端口mac地址
                            if IfPhysAddress_info[3] != '':
                                # mac_format将mac转换为大写字母，同时缺少的0补齐
                                res_If[IfPhysAddress_info[0]]['phys_addr'] = mac_format(IfPhysAddress_info[3])
                        IfSpeed = re.findall(r'IF-MIB::ifSpeed.(.*)', oid_info['IfSpeed'])
                        for i in IfSpeed:
                            IfSpeed_info = i.split(' ')
                            # 协商速率
                            res_If[IfSpeed_info[0]]['speed'] = str(int(IfSpeed_info[3]) / 1000000) + 'Mbps'
                        IfMTU = re.findall(r'IF-MIB::ifMtu.(.*)', oid_info['IfMTU'])
                        for i in IfMTU:
                            IfMTU_info = i.split(' ')
                            # MTU
                            res_If[IfMTU_info[0]]['mtu'] = IfMTU_info[3]


                        #######################  res_If 端口信息    #######################################
                        #
                        # '10140': {
                        #     'name': 'GBZX-SW-ACCESS-C2960X-006/10140',
                        #     'phys_addr': '6C:5E:3B:2B:20:A8',
                        #     'speed': '100Mbps',
                        #     'oper_status': 'up',
                        #     'if_name': 'GigabitEthernet1/0/40',
                        #     'mtu': '1500',
                        #     'admin_status': 'up',
                        #     'type': 'ethernetCsmacd'
                        # }
                        #######################   #######################################

                        ################################ result 基本信息 ###################
                        # 'name': 'GBZX-SW-ACCESS-C2960X-006',
                        # 'software_version': '15.2(2)E7',
                        # 'ip': '192.166.255.16',
                        # 'brand': 'Cisco',
                        # 'NETDPORT': [{
                        #     'name': 'GBZX-SW-ACCESS-C2960X-006/00001'
                        # },]
                        # 'sn': 'FOC2320T06B'
                        #######################   #######################################


                        # 聚合端口查询
                        portChannel_list = re.findall(r'iso.2.840.10006.300.43.1.2.1.1.13.(.*)', oid_info['portChannel'])

                        if 'No Such Object available on this agent at this OID' in portChannel_list[0]:
                            # print ' 该设备无聚合端口或不支持此聚合端口oid采集'
                            portChannel_list = []

                        portChannel_res = {}
                        portChannel_port = []
                        if portChannel_list != []:
                            for portChannel in portChannel_list:
                                port_result = portChannel.split()
                                if port_result[3] not in portChannel_port:
                                    portChannel_port.append(port_result[3])
                                if portChannel_res.has_key(port_result[3]):
                                    portChannel_res[port_result[3]].append({'portIndex': port_result[0]})
                                else:
                                    portChannel_res[port_result[3]] = [{'portIndex': port_result[0]}]

                        # 初始化对端列表的数据，若未采集到数据，则置空。
                        for if_info in res_If:
                            if 'remote_list' not in res_If[if_info].keys():
                                res_If[if_info]['remote_list'] = []


                        # print portChannel_res   {'0': [{'portIndex': '10101'}, {'portIndex': '10102'}}
                        # print portChannel_port  ['0']


                        # 判断设备是否为思科-采集vlan---------------------------------------------------------------------------------------------------------
                        cisco = re.search(result['brand'], 'Cisco', re.IGNORECASE)

                        vlan_info = []
                        if bool(cisco):
                            cisco_result = cisco_neted_collect(info_ip['ip'])

                            # 序列号
                            result['sn'] = cisco_result['sn']
                            # 型号
                            result['module'] = cisco_result['module']
                            # vlan
                            vlan_list = cisco_result['vlan_list']

                            for vlan in vlan_list:
                                res = vlan.split()
                                if res[3] != '0':
                                    vlan_integer = res[0]
                                    res_If[vlan_integer]['vlan'] = res[3]
                                    if res[3] not in vlan_info and res[3] != '1':
                                        vlan_info.append(res[3])



                        # 对端列表ip-mac表,mac_ip表获取
                        IpNetToMediaPhysAddress = re.findall(r'.ipNetToMediaPhysAddress.(.*)', oid_info['IpNetToMediaPhysAddress'])

                        ip_mac_table = {}
                        mac_ip_table = {}
                        for info in IpNetToMediaPhysAddress:
                            remote_ip = info.partition('.')[2].split(' ')[0]
                            remote_mac = mac_format(info.partition('.')[2].split(' ')[3])
                            ip_mac_table[remote_ip] = remote_mac
                            mac_ip_table[remote_mac] = remote_ip
                            ip_mac_result_info[remote_ip] = remote_mac

                        # 根据ip-mac表，取出设备管理ip的mac信息
                        '''
                        try:
                            result['mac'] = ip_mac_result_info[info_ip['ip']]
                        except Exception,e:
                            msg = 'not found ip in ip-mac-table'
                        '''
                        mac_port_table = {}

                        # mac-prot表
                        dot1dBasePortIfIndex = oid_info['dot1dBasePortIfIndex']
                        dot1qTpFdbPort = oid_info['dot1qTpFdbPort']
                        dot1qTpFdbMac = oid_info['dot1qTpFdbMac']

                        err_info = 'No Such Instance currently exists at this OID'
                        if err_info not in dot1qTpFdbMac and err_info not in dot1qTpFdbPort and err_info not in dot1dBasePortIfIndex:
                            # mac_port table
                            mac_port_result = mac_port_table_format(dot1dBasePortIfIndex, dot1qTpFdbPort, dot1qTpFdbMac)

                            for mac in mac_port_result:
                                mac_port_table[mac] = mac_port_result[mac]

                        if vlan_info != []:
                            # 根据不同vlan采集信息
                            for vlan in vlan_info:
                                community_vlan = community + '@' + vlan

                                oid_info = oid_list()['public_oid']
                                dot1dBasePortIfIndex, code = snmp_collect(info_ip['ip'], community_vlan,oid_info['dot1dBasePortIfIndex'])

                                dot1qTpFdbPort, code = snmp_collect(info_ip['ip'], community_vlan,oid_info['dot1qTpFdbPort'])

                                dot1qTpFdbMac, code = snmp_collect(info_ip['ip'], community_vlan,oid_info['dot1qTpFdbMac'])

                                if err_info not in dot1qTpFdbMac and err_info not in dot1qTpFdbPort and err_info not in dot1dBasePortIfIndex:
                                    mac_port_result = mac_port_table_format(dot1dBasePortIfIndex, dot1qTpFdbPort,dot1qTpFdbMac)

                                    for mac in mac_port_result:
                                        mac_port_table[mac] = mac_port_result[mac]

                        cdp_port_list = []
                        lldp_port_list = []
                        # 根据cisco cdp协议，采集有邻居协议的设备
                        # if bool(cisco):
                        #     cdp_ip_list = []
                        #     for remote_info in cisco_result['cdp_result']:
                        #         cdp_remote_list = {}
                        #         if cisco_result['cdp_result'][remote_info].has_key('remote_ip'):
                        #             remote_ip = cisco_result['cdp_result'][remote_info]['remote_ip']
                        #             cdp_remote_list['ip'] = remote_ip
                        #             cdp_ip_list.append(remote_ip)
                        #         netd_name = cisco_result['cdp_result'][remote_info]['remote_sys_name']
                        #         cdp_remote_list['netd_name'] = netd_name
                        #         if_name = cisco_result['cdp_result'][remote_info]['remote_portName']
                        #         cdp_remote_list['if_name'] = if_name
                        #         cdp_port_list.append(remote_info)
                        #         '''
                        #         if res_If[remote_info].has_key('remote_list'):
                        #             res_If[remote_info]['remote_list'].append(cdp_remote_list)
                        #         else:
                        #             res_If[remote_info]['remote_list'] = [cdp_remote_list]
                        #         '''
                        #         res_If[remote_info]['remote_list'] = [cdp_remote_list]
                        # # 否则使用lldp采集邻居协议设备
                        # else:
                        #     # print oid_info['lldpRemEntry']
                        #     lldp_info = re.findall(r'iso.0.8802.1.1.2.1.4.1.1.7.(.*)', oid_info['lldpRemEntry'])
                        #     if lldp_info != [] and 'Hex-STRING' not in lldp_info[0]:
                        #         lldp_info = re.findall(r'iso.0.8802.1.1.2.1.4.1.1.5.(.*)', oid_info['lldpRemEntry'])
                        #         for lldp in lldp_info:
                        #             # print lldp
                        #             lldp_portIndex = lldp.split('.')[1]
                        #             lldp_mac = re.findall(r'.Hex-STRING: (.*) ', lldp)[0].replace(' ', ':').upper()
                        #             res_If[lldp_portIndex]['remote_list'] = [{'mac': lldp_mac}]



                        for remote_mac in mac_port_table:
                            # 判断端口是否为聚合端口
                            if mac_port_table[remote_mac] not in portChannel_port:
                                # 判断端口是否已经通过cdp协议采集到对端设备数据
                                if mac_port_table[remote_mac] not in cdp_port_list:
                                    # 判断mac是否在mac-ip表，若存在，则取出对应ip
                                    if remote_mac in mac_ip_table.keys():
                                        # 若存在remote_list字段，则使用append
                                        if res_If[mac_port_table[remote_mac]].has_key('remote_list'):
                                            res_If[mac_port_table[remote_mac]]['remote_list'].append(
                                                {'ip': mac_ip_table[remote_mac], 'mac': remote_mac})
                                        else:
                                            res_If[mac_port_table[remote_mac]]['remote_list'] = {
                                                'ip': mac_ip_table[remote_mac], 'mac': remote_mac}
                                    else:
                                        # 若存在remote_list字段，则使用append
                                        if res_If[mac_port_table[remote_mac]].has_key('remote_list'):
                                            res_If[mac_port_table[remote_mac]]['remote_list'].append(
                                                {'mac': remote_mac})
                                        else:
                                            res_If[mac_port_table[remote_mac]]['remote_list'] = [{'mac': remote_mac}]

                        # print res_If
                        for port_name_res in res_If:
                            # 判断端口名称是否为port-channel，类型是否为propVirtual
                            if res_If[port_name_res]['type'] == 'propVirtual' and 'port-channel' in res_If[port_name_res]['if_name'].lower():
                                if res_If[port_name_res].has_key('remote_list'):
                                    res_If[port_name_res]['remote_list'] = []



                        # 若为聚合端口
                        if portChannel_list != []:
                            for portChannelIndex in portChannel_res:
                                if portChannelIndex != '0':
                                    res_list = []
                                    for portChannel_list in portChannel_res[portChannelIndex]:
                                        for res in res_If[portChannel_list['portIndex']]['remote_list']:
                                            res_list.append(res)
                                    res_If[portChannelIndex]['remote_list'] = res_list


                        # 每个端口详情信息[{},{}]
                        for i in res_If:
                            port_json_data.append(res_If[i])


                        # 将结果append至json_data, 所有的消息合并
                        json_data.append(result)
                    else:
                        print '采集设备', info_ip['ip'], '...', 'ERROR:', oid_info
                        msg = 'error'
            except Exception, e:
                print e.message
                msg = e.message
    finally:
        lock.release()


def mac_port_table_format(dot1dBasePortIfIndex, dot1qTpFdbPort, dot1qTpFdbMac):
    # 取出端口和索引的关系
    dot1dBasePortIfIndex = re.findall(r'SNMPv2-SMI::mib-2.17.1.4.1.2.(.*)', dot1dBasePortIfIndex)
    dot1qTpFdbPort = re.findall(r'SNMPv2-SMI::mib-2.17.4.3.1.2.(.*)', dot1qTpFdbPort)
    dot1qTpFdbMac = re.findall(r'SNMPv2-SMI::mib-2.17.4.3.1.1.(.*)', dot1qTpFdbMac)

    dot1dBasePortIfIndex_table = {}
    # print dot1dBasePortIfIndex
    for dBasePort_info in dot1dBasePortIfIndex:
        dbPort = dBasePort_info.split()[0]
        dbPortIfIndex = dBasePort_info.split()[3]
        dot1dBasePortIfIndex_table[dbPort] = dbPortIfIndex



    # 取出端口和mac地址十进制之间的关系
    dot1qTpFdbPort_table = {}
    for qTpFdbPort_info in dot1qTpFdbPort:
        mac_index = qTpFdbPort_info.split(' ')[0]
        dbPortIfIndex = qTpFdbPort_info.split(' ')[3]
        dot1qTpFdbPort_table[mac_index] = dbPortIfIndex


    mac_port_result = {}
    # 取出端口和mac之间的关系
    for qTpFdbMac_info in dot1qTpFdbMac:
        # print qTpFdbMac_info
        # mac十进制的值
        qTpFdbMac_index = qTpFdbMac_info.split(' ')[0]
        # 对应的mac地址
        qTpFdbMac = re.findall(r'.Hex-STRING: (.*)', qTpFdbMac_info)[0].replace(' ', ':')[0:-1]
        # 根据mac十进制取出端口信息
        dbPortIfIndex = dot1qTpFdbPort_table[qTpFdbMac_index]
        # print dbPortIfIndex
        # 根据端口信息取端口索引
        if dbPortIfIndex != '0' and dot1dBasePortIfIndex_table.has_key(dbPortIfIndex):
            dot1dBasePortIfIndex = dot1dBasePortIfIndex_table[dbPortIfIndex]
            # 将对应索引的mac地址存入res_If中的remote_list
            mac_port_result[qTpFdbMac] = dot1dBasePortIfIndex
    return mac_port_result


def cisco_neted_collect(ip):
    code_back, cisco_info = collect_info(ip, community, 'cisco_oid')
    if code_back == 0:
        ######################### 基本信息
        cisco_result = {}
        # 序列号
        serial = re.findall(r'."(.*)"', cisco_info['cisco_serial'].split('\n')[0])
        cisco_result['sn'] = serial[0]

        # 型号
        module = re.findall(r'."(.*)"', cisco_info['cisco_module'].split('\n')[0])
        cisco_result['module'] = module[0]

        # vlan
        vlan_list = re.findall(r'.9.9.68.1.2.2.1.2.(.*)', cisco_info['vmVlan'])
        cisco_result['vlan_list'] = vlan_list

        ################### 对端信息
        # cdp采集对端设备
        cdp_result = {}

        # 对端设备名称
        portIndex_list = re.findall(r'.9.9.23.1.2.1.1.6.(.*)', cisco_info['cdpCacheSysName'])

        if "No Such" in portIndex_list[0]:
            cdp_result["0"] = {'remote_sys_name': 'UNKNOW'}
        else:
            for portIndex in portIndex_list:
                port_index = portIndex.split('.')[0]
                remote_sys_name = re.findall(r'."(.*)"', portIndex)[0]
                cdp_result[port_index] = {'remote_sys_name': remote_sys_name}
        # {'10101': {'remote_sys_name': 'AP03'}}


        # 对端端口名称
        remotePortName_list = re.findall(r'.9.9.23.1.2.1.1.7.(.*)', cisco_info['cdpCachePortName'])
        if "No Such" in remotePortName_list[0]:
            cdp_result["0"]['remote_portName'] = 'UNKNOW'
        else:
            for remotePortName in remotePortName_list:
                port_index = remotePortName.split('.')[0]
                remote_portName = re.findall(r'."(.*)"', remotePortName)[0]
                cdp_result[port_index]['remote_portName'] = remote_portName

        # {'10110': {'remote_portName': 'GigabitEthernet0', 'remote_sys_name': 'AP03'}


        # 对端设备类型
        cdpCacheType_list = re.findall(r'.9.9.23.1.2.1.1.3.(.*)', cisco_info['cdpCacheType'])
        if "No Such" in cdpCacheType_list[0]:
            cdp_result["0"]['type'] = 'UNKNOW'
        else:
            for cdpCacheType in cdpCacheType_list:
                port_index = cdpCacheType.split('.')[0]
                cdp_type = re.findall(r'.INTEGER: (.*)', cdpCacheType)[0]
                cdp_result[port_index]['type'] = cdp_type

        # {'10110': {'remote_portName': 'GigabitEthernet0', 'type': '1', 'remote_sys_name': 'AP03'}

        # 对端ip
        cdpCacheIP_list = re.findall(r'.9.9.23.1.2.1.1.4.(.*)', cisco_info['cdpCacheIP'])
        if "No Such" in cdpCacheIP_list[0]:
            cdp_result["0"]['remote_ip'] = 'UNKNOW'
        else:
            for cdpCacheIP in cdpCacheIP_list:
                port_index = cdpCacheIP.split('.')[0]
                # 若type为1，则为ip
                if cdp_result[port_index]['type'] == '1':
                    remote_ip = re.findall(r'.Hex-STRING: (.*)', cdpCacheIP)[0]
                    # 十六进制转换为十进制
                    res_ip = ''
                    for i in remote_ip.split():
                        res_ip += (str(int(i, 16)) + '.')
                    cdp_result[port_index]['remote_ip'] = res_ip[:-1]

        # {'10110': {'remote_portName': 'GigabitEthernet0', 'type': '1', 'remote_sys_name': 'AP03', 'remote_ip': '192.166.254.250'}

        cisco_result['cdp_result'] = cdp_result

        return cisco_result
    else:
        # print '采集Cisco设备',info_ip['ip'],'...','ERROR:',oid_info
        msg = 'error'


def mac_format(mac):
    res = {}
    format_list = mac.split(':')
    num = 0
    # 根据':'分隔，若位数为1，则在前面补齐0
    for i in format_list:
        num += 1
        if len(i) == 1:
            res[num] = '0' + i
        elif len(i) == 2:
            res[num] = i
    mac_addr = res[1] + ':' + res[2] + ':' + res[3] + ':' + res[4] + ':' + res[5] + ':' + res[6]
    # 小写字母转换为大写
    return mac_addr.upper()


class MyThread(threading.Thread):

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        apply(self.func, self.args)


lock = threading.Lock()


# snmp协议采集设备信息
def snmp_collect(ip, community, oid):
    cmd = 'snmpwalk -v 2c -c {0} {1} {2}'.format(community, ip, oid)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = p.stdout.read()
    code = p.wait()
    return stdout, code


# 查出EasyOps模型“网络设备”中交换机的ip列表
def switch_ip_collect(object_id):
    url = "http://" + EASYOPS_CMDB_HOST + "/object/" + object_id + "/instance/_search"
    result = {}
    # ret_list = []
    count = 0
    page = 1
    page_size = 200
    # 设置查询条件
    while (count >= 0):
        count = 0
        params = {
            "page": page,
            "page_size": page_size,
            "fields": {
                "ip": True,
            }
        }
        HEADERS = headers_cmdb
        ret = requests.post(url, headers=HEADERS, data=json.dumps(params)).json()
        # print '查询“网络设备”ip'
        res_key = 'page-' + str(page)
        # ret_list += ret['data']['list']
        if ret['data']['list'] != []:
            result[res_key] = ret['data']['list']
        count = len(ret['data']['list']) - page_size
        page += 1
    return result


# 创建线程
res = switch_ip_collect('_SWITCH')  # 获取到交换机所有实例

threads = []
files = range(len(res))
for k, v in res.items():
    t = MyThread(collect_netd, (k, v), collect_netd.__name__)
    threads.append(t)


class AutoDiscovery():
    # 定义全局变量autodiscovery_data_list
    global autodiscovery_data_list
    autodiscovery_data_list = []

    # 数据格式化
    def data_format(self, json_data, object_id, pks, upsert=False):
        # json_data：需要上报的数据
        # object_id：CMDB模型ID
        # pks：更新依据，格式为list，例如['name']
        # upsert：不存在实例时是否创建,bool类型，True or False，默认为False
        for data in json_data:
            result = {
                'dims': {
                    "pks": pks,  # 用于查询出唯一实例的模型字段组合
                    "object_id": object_id,  # CMDB模型ID
                    "upsert": upsert  # 不存在时是否创建，默认为False
                },
                'vals': data  # 上报的数据
            }
            # 将格式化后的数据append至全局变量autodiscovery_data_list
            autodiscovery_data_list.append(result)

    # 数据上报
    def report_data(self):
        # 注意：自动采集中只能输出最终的json数据，不能有其它多余输出
        print json.dumps(autodiscovery_data_list)


AutoDiscovery = AutoDiscovery()

if __name__ == '__main__':
    collect_netd('page-1', [])

    # print json_data
    netd_json_data = []
    for i in json_data:
        if i['ip'] in ip_mac_result_info.keys():
            i['mac'] = ip_mac_result_info[i['ip']]
        netd_json_data.append(i)

    print netd_json_data

    exit()
        # ip_mac_result_info
    # print len(netd_json_data)
    # print netd_json_data
    # AutoDiscoveryJson(json_data=port_json_data, object_id='NETDPORT')
    # AutoDiscoveryJson(json_data=netd_json_data, object_id='NETD')
    # 交换机端口
    AutoDiscovery.data_format(json_data=port_json_data, object_id='NETDPORT', pks=['name'], upsert=True)
    # 交换机
    AutoDiscovery.data_format(json_data=netd_json_data, object_id='NETD', pks=['ip'], upsert=True)
    # 数据上报
    AutoDiscovery.report_data()

    exit(0)
    # 线程数按查询cmdb中网络设备时的分页数自动调整，共有多少page，就有多少线程
    # 启动线程
    for i in files:
        threads[i].start()
    for i in files:
        threads[i].join()
    netd_json_data = []
    for i in json_data:
        if i['ip'] in ip_mac_result_info.keys():
            i['mac'] = ip_mac_result_info[i['ip']]
        netd_json_data.append(i)
        # ip_mac_result_info
    # print len(netd_json_data)
    # print netd_json_data
    # AutoDiscoveryJson(json_data=port_json_data, object_id='NETDPORT')
    # AutoDiscoveryJson(json_data=netd_json_data, object_id='NETD')
    # 交换机端口
    AutoDiscovery.data_format(json_data=port_json_data, object_id='NETDPORT', pks=['name'], upsert=True)
    # 交换机
    AutoDiscovery.data_format(json_data=netd_json_data, object_id='NETD', pks=['ip'], upsert=True)
    # 数据上报
    AutoDiscovery.report_data()