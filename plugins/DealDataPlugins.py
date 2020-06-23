# -*- coding: utf-8 -*-
"""
解析数据，公共方式
"""
import re
from script.cisco import cisco_serial, cisco_module, vmVlan, cdpCacheSysName, cdpCachePortName, cdpCacheType, cdpCacheIP
from script.public import ipAdEnt, sysDescr, \
    sysName, snmpEngineId, IfDescr, IfType, \
    IfOperStatus, ifAdminStatus, IfName, \
    IfPhysAddress, IfSpeed, IfMTU, portChannel, IpNetToMediaPhysAddress, \
    dot1dBasePortIfIndex, dot1qTpFdbPort, dot1qTpFdbMac, vlan, lldpRemEntry, lldpLocPortDesc


# 公共数据解析类
class public_oid(object):
    def __init__(self):
        self.res = {}

    # 交换机关联IP，包括管理IP, VLAN IP    ok
    def ipAdEnt(self, data):
        return ipAdEnt.get_ipAdEnt(data)

    # 基本信息  sys_descr 品牌 型号 软件版本 信息   ok
    def sysDescr(self, data):
        return sysDescr.get_sysDescr(data)

    # 设备名称  ok
    def sysName(self, data):
        return sysName.get_sysDescr(data)

    # 启动时间  ok
    def snmpEngineId(self, data):
        return snmpEngineId.get_snmpEngineId(data)

    # 网卡名  ok
    def IfDescr(self, data):
        return IfDescr.get_IfDescr(data)

    # 端口名  ok
    def IfName(self, data):
        return IfName.get_ifName(data)

    # 交换机端口 - 类型 ok
    def IfType(self, data):
        return IfType.get_IfType(data)

    # 交换机端口 - 状态 : up/down  ok
    def IfOperStatus(self, data):
        return IfOperStatus.get_IfOperStatus(data)

    # 交换机端口 - 管理状态 : up  ok
    def IfAdminStatus(self, data):
        return ifAdminStatus.get_ifAdminStatus(data)

    # 交换机mac地址  ok
    def IfPhysAddress(self, data):
        return IfPhysAddress.get_ifPhysAddress(data)

    # 交换机端口 - 协商速率  ok
    def IfSpeed(self, data):
        return IfSpeed.get_IfSpeed(data)

    # 交换机端口 - MTU : 9600 或 1500  ok
    def IfMTU(self, data):
        return IfMTU.get_IfMTU(data)

    # ARP信息 ok
    def IpNetToMediaPhysAddress(self, data):
        return IpNetToMediaPhysAddress.get_IpNetToMediaPhysAddress(data)

    # 1. 根据 SNMPv2-SMI （1dBasePortIfIndex,1qTpFdbMac,1qTpFdbPort）信息获取交换机的mac地址（逻辑端口） ok
    def dot1dBasePortIfIndex(self, data):
        return dot1dBasePortIfIndex.get_dot1dBasePortIfIndex(data)

    # 2. 根据 SNMPv2-SMI （1dBasePortIfIndex,1qTpFdbMac,1qTpFdbPort）信息获取交换机的mac地址（逻辑端口）ok
    def dot1qTpFdbPort(self, data):
        return dot1qTpFdbPort.get_dot1qTpFdbPort(data)

    # 3. 根据 SNMPv2-SMI （1dBasePortIfIndex,1qTpFdbMac,1qTpFdbPort）信息获取交换机的mac地址（逻辑端口）ok 数据是在最后处理数据的时候合并的
    def dot1qTpFdbMac(self, data):
        return dot1qTpFdbMac.get_dot1qTpFdbMac(data)

    # 集合端口  ok
    def portChannel(self, data):
        return portChannel.get_portChannel(data)

    # 获取cdp或lldp协议端口信息
    def lldpRemEntry(self, data):
        return lldpRemEntry.get_lldpRemEntry(data)

    # vlan list
    def vlan(self, data):
        return vlan.get_vlan(data)

    # lldpLocPortDesc
    def lldpLocPortDesc(self, data):
        return lldpLocPortDesc.get_lldpLocPortDesc(data)


# 思科数据解析类
class cisco_oid(object):
    # vlan
    def vmVlan(self, data):
        return vmVlan.get_vmVlan(data)

    # 对端设备名称
    def cdpCacheSysName(self, data):
        return cdpCacheSysName.get_cdpCacheSysName(data)

    # 对端端口名称
    def cdpCachePortName(self, data):
        return cdpCachePortName.get_cdpCachePortName(data)

    # 对端设备类型
    def cdpCacheType(self, data):
        return cdpCacheType.get_cdpCacheType(data)

    def cdpCacheIP(self, data):
        return cdpCacheIP.get_cdpCacheIP(data)

    #  序列号
    def cisco_serial(self, data):
        return cisco_serial.get_cisco_serial(data)

    # 型号
    def cisco_module(self, data):
        return cisco_module.get_cisco_module(data)


class other_oid(object):

    # 1. 根据 SNMPv2-SMI （1dBasePortIfIndex,1qTpFdbMac,1qTpFdbPort）信息获取交换机的mac地址（逻辑端口） ok
    def dot1dBasePortIfIndex(self, data):
        return dot1dBasePortIfIndex.get_dot1dBasePortIfIndex(data)

    # 2. 根据 SNMPv2-SMI （1dBasePortIfIndex,1qTpFdbMac,1qTpFdbPort）信息获取交换机的mac地址（逻辑端口）ok
    def dot1qTpFdbPort(self, data):
        return dot1qTpFdbPort.get_dot1qTpFdbPort(data)

    # 3. 根据 SNMPv2-SMI （1dBasePortIfIndex,1qTpFdbMac,1qTpFdbPort）信息获取交换机的mac地址（逻辑端口）ok 数据是在最后处理数据的时候合并的
    def dot1qTpFdbMac(self, data):
        return dot1qTpFdbMac.get_dot1qTpFdbMac(data)

    def mergedata(self, data):
        dot1dBasePortIfIndex = data.get('dot1dBasePortIfIndex')  # 取出端口和索引的关系
        dot1qTpFdbMac = data.get('dot1qTpFdbMac')
        dot1qTpFdbPort = data.get('dot1qTpFdbPort')  # 取出端口和mac地址十进制之间的关系
        # print dot1dBasePortIfIndex
        # print dot1qTpFdbPort
        # {u'49': u'10149', u'51': u'10151', u'50': u'10150', u'456': u'5001', u'52': u'10152'}
        # {u'96.8.16.192.174.0': u'456', u'96.8.16.192.174.2': u'456', u'0.224.252.9.188.249': u'456'}

        # print dot1qTpFdbMac
        # [u'0.224.252.9.188.249 = Hex-STRING: 00 E0 FC 09 BC F9 ', u'96.8.16.192.174.0 = Hex-STRING: 60 08 10 C0 AE 00 ',
        #  u'96.8.16.192.174.2 = Hex-STRING: 60 08 10 C0 AE 02 ']

        # 2. mac单独处理，且dot1qTpFdbMac是原始数据
        mac_port_result = {}
        # 取出端口和mac之间的关系
        for mac_info in dot1qTpFdbMac:
            # mac十进制的值
            mac_index = str(mac_info.split(' ')[0])

            # 对应的mac地址
            qTpFdbMac = str(re.findall(r'.Hex-STRING: (.*)', mac_info)[0].replace(' ', ':')[0:-1])
            # 根据mac十进制取出端口信息 456
            dbPortIfIndex = str(dot1qTpFdbPort[mac_index])

            # 根据端口信息取端口索引 456: 5001
            if dbPortIfIndex != '0' and dict(dot1dBasePortIfIndex).has_key(dbPortIfIndex):
                PortIfIndex = dot1dBasePortIfIndex[dbPortIfIndex]
                # 将对应索引的mac地址存入res_If中的remote_list
                mac_port_result[qTpFdbMac] = PortIfIndex

        return mac_port_result
