# -*- coding: utf-8 -*-
"""
返回数据说明
    1.3.6.1.2.1.4.20.1.1 - ipAdEntAddr              #### IP地址 ####
    1.3.6.1.2.1.4.20.1.2 - ipAdEntIfIndex           #### IP地址接口编号 ####
    1.3.6.1.2.1.4.20.1.3 - ipAdEntNetMask           #### IP地址掩码 ####
    1.3.6.1.2.1.4.20.1.4 - ipAdEntBcastAddr         #### 是否广播 ####
    1.3.6.1.2.1.4.20.1.5 - ipAdEntReasmMaxSize      #### 可重组IP报文最大值 ####
实例数据:
    IP-MIB::ipAdEntAddr.172.24.0.1 = IpAddress: 172.24.0.1
    IP-MIB::ipAdEntAddr.172.25.0.5 = IpAddress: 172.25.0.5
    IP-MIB::ipAdEntAddr.172.25.0.13 = IpAddress: 172.25.0.13
    IP-MIB::ipAdEntAddr.172.25.0.18 = IpAddress: 172.25.0.18
    IP-MIB::ipAdEntAddr.172.25.0.245 = IpAddress: 172.25.0.245
    IP-MIB::ipAdEntAddr.172.25.2.1 = IpAddress: 172.25.2.1
    IP-MIB::ipAdEntAddr.172.25.2.2 = IpAddress: 172.25.2.2
    IP-MIB::ipAdEntIfIndex.172.24.0.1 = INTEGER: 7234
    IP-MIB::ipAdEntIfIndex.172.25.0.5 = INTEGER: 7237
    IP-MIB::ipAdEntIfIndex.172.25.0.13 = INTEGER: 7238
    IP-MIB::ipAdEntIfIndex.172.25.0.18 = INTEGER: 7235
    IP-MIB::ipAdEntIfIndex.172.25.0.245 = INTEGER: 7260
    IP-MIB::ipAdEntIfIndex.172.25.2.1 = INTEGER: 7233
    IP-MIB::ipAdEntIfIndex.172.25.2.2 = INTEGER: 7233
    IP-MIB::ipAdEntNetMask.172.24.0.1 = IpAddress: 255.255.255.255
    IP-MIB::ipAdEntNetMask.172.25.0.5 = IpAddress: 255.255.255.252
    IP-MIB::ipAdEntNetMask.172.25.0.13 = IpAddress: 255.255.255.252
    IP-MIB::ipAdEntNetMask.172.25.0.18 = IpAddress: 255.255.255.252
    IP-MIB::ipAdEntNetMask.172.25.0.245 = IpAddress: 255.255.255.252
    IP-MIB::ipAdEntNetMask.172.25.2.1 = IpAddress: 255.255.255.252
    IP-MIB::ipAdEntNetMask.172.25.2.2 = IpAddress: 255.255.255.252
    IP-MIB::ipAdEntBcastAddr.172.24.0.1 = INTEGER: 1
    IP-MIB::ipAdEntBcastAddr.172.25.0.5 = INTEGER: 1
    IP-MIB::ipAdEntBcastAddr.172.25.0.13 = INTEGER: 1
    IP-MIB::ipAdEntBcastAddr.172.25.0.18 = INTEGER: 1
    IP-MIB::ipAdEntBcastAddr.172.25.0.245 = INTEGER: 1
    IP-MIB::ipAdEntBcastAddr.172.25.2.1 = INTEGER: 1
    IP-MIB::ipAdEntBcastAddr.172.25.2.2 = INTEGER: 1
    IP-MIB::ipAdEntReasmMaxSize.172.24.0.1 = INTEGER: 65500
    IP-MIB::ipAdEntReasmMaxSize.172.25.0.5 = INTEGER: 65500
    IP-MIB::ipAdEntReasmMaxSize.172.25.0.13 = INTEGER: 65500
    IP-MIB::ipAdEntReasmMaxSize.172.25.0.18 = INTEGER: 65500
    IP-MIB::ipAdEntReasmMaxSize.172.25.0.245 = INTEGER: 65500
    IP-MIB::ipAdEntReasmMaxSize.172.25.2.1 = INTEGER: 65500
    IP-MIB::ipAdEntReasmMaxSize.172.25.2.2 = INTEGER: 65500
"""
import re


# 交换机关联IP，包括管理IP,VLAN IP
def get_ipAdEnt(data):
    ipAdEntDict = {}

    # ipAdEntAddrTxt = re.findall(r'IP-MIB::ipAdEntAddr.(.*)', data)
    # for i in ipAdEntAddrTxt:
    #     addr_list = re.findall(r'IpAddress:.(.*)', i)
    #     if addr_list:
    #         addr = addr_list[0]
    #         ipAdEntDict.update({"ip": addr})
    #         break

    ipAdEntIfIndexTxt = re.findall(r'IP-MIB::ipAdEntIfIndex.(.*)', data)
    for i in ipAdEntIfIndexTxt:
        IfIndex_list = re.findall(r'INTEGER:.(.*)', i)
        if IfIndex_list:
            IfIndex = IfIndex_list[0]
        else:
            IfIndex = '0'
        ipAdEntDict.update({"ifIdx": int(IfIndex)})

    ipAdEntNetMaskTxt = re.findall(r'IP-MIB::ipAdEntNetMask.(.*)', data)
    for i in ipAdEntNetMaskTxt:
        netmask_list = re.findall(r'IpAddress:.(.*)', i)
        if netmask_list:
            netmask = netmask_list[0]
        else:
            netmask = "255.255.255.255"

        ipAdEntDict.update({"netMask": netmask})

    ipAdEntBcastAddrTxt = re.findall(r'IP-MIB::ipAdEntBcastAddr.(.*)', data)
    for i in ipAdEntBcastAddrTxt:
        BcastAddr_list = re.findall(r'INTEGER:.(.*)', i)
        if BcastAddr_list:
            BcastAddr = BcastAddr_list[0]
        else:
            BcastAddr = "255.255.255.255"

        ipAdEntDict.update({"BcastAddr": int(BcastAddr)})

    ipAdEntReasmMaxSizeTxt = re.findall(r'IP-MIB::ipAdEntReasmMaxSize.(.*)', data)
    for i in ipAdEntReasmMaxSizeTxt:
        ReasmMaxSize_list = re.findall(r'INTEGER:.(.*)', i)
        if ReasmMaxSize_list:
            ReasmMaxSize = ReasmMaxSize_list[0]
        else:
            ReasmMaxSize = 65535

        ipAdEntDict.update({"ReasmMaxSize": int(ReasmMaxSize)})

    return ipAdEntDict
