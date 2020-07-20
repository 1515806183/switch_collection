# -*- coding: utf-8 -*-
import re


# 获取cdp或lldp协议端口信息
def get_lldpRemEntry(data):
    result = {}
    remote_list = {}

    ####对端mac地址 peer_mac -> 1.0.8802.1.1.2.1.4.1.1.5 (lldpRemChassisId) ####
    peerMacList = re.findall(r'iso.0.8802.1.1.2.1.4.1.1.5.(.*)', data)  # '0.436207616.13 = Hex-STRING: DC 8C 37 73 D0 9B '
    for i in peerMacList:
        if "Hex-STRING" in i:
            idx = i.split()[0].split(".")[1]  # 436207616
            peer_mac_list = re.search(r'.\s+Hex-STRING:\s+(.*)\s+', i)  # ['DC 8C 37 73 D0 9B ']
            if peer_mac_list:
                peer_mac = peer_mac_list.group(1).replace(' ', ':').upper()
            else:
                peer_mac = "unknown mac"
        else:
            idx = i.split()[0].split(".")[1]
            i = i.replace("\"", "")
            peer_mac_list = re.findall(r'.STRING: (.*)', i)
            if peer_mac_list:
                peer_mac = peer_mac_list[0].replace(' ', ':').upper()
            else:
                peer_mac = "unknown mac"

        if remote_list.has_key(idx):
            if remote_list[idx].has_key('peer_mac'):
                remote_list[idx]['peer_mac'] = peer_mac
            else:
                remote_list[idx] = {'peer_mac': peer_mac}
        else:
            remote_list[idx] = {'peer_mac': peer_mac}

    ####对端类型 peer_type -> 1.0.8802.1.1.2.1.4.1.1.6 (lldpRemPortIdSubtype) ####
    peerType = re.findall(r'iso.0.8802.1.1.2.1.4.1.1.6.(.*)', data)  # '0.436207616.13 = INTEGER: 5'
    for i in peerType:
        idx = i.split('.')[1]
        peer_type = i.split(' ')[3]
        if remote_list.has_key(idx):
            remote_list[idx]['peer_type'] = peer_type
        else:
            remote_list[idx] = {'peer_type': peer_type}

    ####对端端口名 peer_port -> 1.0.8802.1.1.2.1.4.1.1.7 (lldpRemPortId) ####
    peerPortList = re.findall(r'iso.0.8802.1.1.2.1.4.1.1.7.(.*)', data)
    for i in peerPortList:
        idx = i.split('.')[1]
        peer_port_list = re.findall(r'."(.*)"', i)
        if peer_port_list:
            peer_port = peer_port_list[0]
        else:
            peer_port = ""
        # peer_port = re.findall(r'."(.*)"',i)[0]
        if remote_list.has_key(idx):
            remote_list[idx]['peer_port'] = peer_port
        else:
            remote_list[idx] = {'peer_port': peer_port}

    ###对端设备端口描述 peer_port_desc (port_desc) -> 1.0.8802.1.1.2.1.4.1.1.8 (lldpRemPortDesc) ####
    portDescList = re.findall(r'iso.0.8802.1.1.2.1.4.1.1.8.(.*)', data)
    for i in portDescList:
        idx = i.split('.')[1]
        port_desc = re.findall(r'."(.*)"', i)[0]
        if remote_list.has_key(idx):
            remote_list[idx]['peer_port_desc'] = port_desc
        else:
            remote_list[idx] = {'peer_port_desc': port_desc}

    ####对端设备名称 peer_device (sys_name) --> 1.0.8802.1.1.2.1.4.1.1.9 (lldpRemSysName) ####
    sysNameList = re.findall(r'iso.0.8802.1.1.2.1.4.1.1.9.(.*)', data)
    for i in sysNameList:
        idx = i.split('.')[1]
        peer_device_list = re.findall(r'."(.*)"', i)
        if peer_device_list:
            peer_device = peer_device_list[0]
        else:
            peer_device = ""

        if remote_list.has_key(idx):
            remote_list[idx]['peer_device'] = peer_device
        else:
            remote_list[idx] = {'peer_device': peer_device}

    result['lldpRemEntry'] = remote_list
    return result


if __name__ == '__main__':
    data = """
iso.0.8802.1.1.2.1.4.1.1.4.0.436207616.13 = INTEGER: 4
iso.0.8802.1.1.2.1.4.1.1.4.0.436208128.12 = INTEGER: 4
iso.0.8802.1.1.2.1.4.1.1.4.0.436208640.14 = INTEGER: 4
iso.0.8802.1.1.2.1.4.1.1.4.0.436209152.15 = INTEGER: 4
iso.0.8802.1.1.2.1.4.1.1.4.0.436217856.23 = INTEGER: 4
iso.0.8802.1.1.2.1.4.1.1.4.0.436218368.21 = INTEGER: 4
iso.0.8802.1.1.2.1.4.1.1.4.0.436218880.24 = INTEGER: 4
iso.0.8802.1.1.2.1.4.1.1.4.0.436219392.22 = INTEGER: 4
iso.0.8802.1.1.2.1.4.1.1.4.0.436229120.26 = INTEGER: 4
iso.0.8802.1.1.2.1.4.1.1.4.0.436230144.8 = INTEGER: 4
iso.0.8802.1.1.2.1.4.1.1.4.0.436230656.9 = INTEGER: 4
iso.0.8802.1.1.2.1.4.1.1.4.0.436231168.6 = INTEGER: 4
iso.0.8802.1.1.2.1.4.1.1.4.0.436231680.7 = INTEGER: 4
iso.0.8802.1.1.2.1.4.1.1.4.0.436234240.10 = INTEGER: 4
iso.0.8802.1.1.2.1.4.1.1.4.0.436234752.11 = INTEGER: 4
iso.0.8802.1.1.2.1.4.1.1.5.0.436207616.13 = Hex-STRING: DC 8C 37 73 D0 9B 
iso.0.8802.1.1.2.1.4.1.1.5.0.436208128.12 = Hex-STRING: DC 8C 37 73 D0 FB 
iso.0.8802.1.1.2.1.4.1.1.5.0.436208640.14 = Hex-STRING: DC 8C 37 A9 13 FB 
iso.0.8802.1.1.2.1.4.1.1.5.0.436209152.15 = Hex-STRING: 78 BC 1A 78 AB BB 
iso.0.8802.1.1.2.1.4.1.1.5.0.436217856.23 = Hex-STRING: 34 80 0D 05 C5 92 
iso.0.8802.1.1.2.1.4.1.1.5.0.436218368.21 = Hex-STRING: 34 80 0D 05 E5 EA 
iso.0.8802.1.1.2.1.4.1.1.5.0.436218880.24 = Hex-STRING: 34 80 0D 05 C5 93 
iso.0.8802.1.1.2.1.4.1.1.5.0.436219392.22 = Hex-STRING: 34 80 0D 05 E5 EB 
iso.0.8802.1.1.2.1.4.1.1.5.0.436229120.26 = Hex-STRING: 70 7D B9 87 1A A8 
iso.0.8802.1.1.2.1.4.1.1.5.0.436230144.8 = Hex-STRING: 00 3A 9C 80 23 34 
iso.0.8802.1.1.2.1.4.1.1.5.0.436230656.9 = Hex-STRING: 00 3A 9C 80 23 35 
iso.0.8802.1.1.2.1.4.1.1.5.0.436231168.6 = Hex-STRING: 00 3A 9C 80 23 36 
iso.0.8802.1.1.2.1.4.1.1.5.0.436231680.7 = Hex-STRING: 00 3A 9C 80 23 37 
iso.0.8802.1.1.2.1.4.1.1.5.0.436234240.10 = Hex-STRING: 00 3A 9C 80 23 48 
iso.0.8802.1.1.2.1.4.1.1.5.0.436234752.11 = Hex-STRING: 00 3A 9C 80 23 4C 
iso.0.8802.1.1.2.1.4.1.1.6.0.436207616.13 = INTEGER: 5
iso.0.8802.1.1.2.1.4.1.1.6.0.436208128.12 = INTEGER: 5
iso.0.8802.1.1.2.1.4.1.1.6.0.436208640.14 = INTEGER: 5
iso.0.8802.1.1.2.1.4.1.1.6.0.436209152.15 = INTEGER: 5
iso.0.8802.1.1.2.1.4.1.1.6.0.436217856.23 = INTEGER: 3
iso.0.8802.1.1.2.1.4.1.1.6.0.436218368.21 = INTEGER: 3
iso.0.8802.1.1.2.1.4.1.1.6.0.436218880.24 = INTEGER: 3
iso.0.8802.1.1.2.1.4.1.1.6.0.436219392.22 = INTEGER: 3
iso.0.8802.1.1.2.1.4.1.1.6.0.436229120.26 = INTEGER: 5
iso.0.8802.1.1.2.1.4.1.1.6.0.436230144.8 = INTEGER: 5
iso.0.8802.1.1.2.1.4.1.1.6.0.436230656.9 = INTEGER: 5
iso.0.8802.1.1.2.1.4.1.1.6.0.436231168.6 = INTEGER: 5
iso.0.8802.1.1.2.1.4.1.1.6.0.436231680.7 = INTEGER: 5
iso.0.8802.1.1.2.1.4.1.1.6.0.436234240.10 = INTEGER: 5
iso.0.8802.1.1.2.1.4.1.1.6.0.436234752.11 = INTEGER: 5
iso.0.8802.1.1.2.1.4.1.1.7.0.436207616.13 = STRING: "Ethernet1/52"
iso.0.8802.1.1.2.1.4.1.1.7.0.436208128.12 = STRING: "Ethernet1/52"
iso.0.8802.1.1.2.1.4.1.1.7.0.436208640.14 = STRING: "Ethernet1/52"
iso.0.8802.1.1.2.1.4.1.1.7.0.436209152.15 = STRING: "Ethernet1/52"
iso.0.8802.1.1.2.1.4.1.1.7.0.436217856.23 = Hex-STRING: 34 80 0D 05 C5 92 
iso.0.8802.1.1.2.1.4.1.1.7.0.436218368.21 = Hex-STRING: 34 80 0D 05 E5 EA 
iso.0.8802.1.1.2.1.4.1.1.7.0.436218880.24 = Hex-STRING: 34 80 0D 05 C5 93 
iso.0.8802.1.1.2.1.4.1.1.7.0.436219392.22 = Hex-STRING: 34 80 0D 05 E5 EB 
iso.0.8802.1.1.2.1.4.1.1.7.0.436229120.26 = STRING: "Ethernet1/47"
iso.0.8802.1.1.2.1.4.1.1.7.0.436230144.8 = STRING: "Ethernet1/45"
iso.0.8802.1.1.2.1.4.1.1.7.0.436230656.9 = STRING: "Ethernet1/46"
iso.0.8802.1.1.2.1.4.1.1.7.0.436231168.6 = STRING: "Ethernet1/47"
iso.0.8802.1.1.2.1.4.1.1.7.0.436231680.7 = STRING: "Ethernet1/48"
iso.0.8802.1.1.2.1.4.1.1.7.0.436234240.10 = STRING: "Ethernet1/53"
iso.0.8802.1.1.2.1.4.1.1.7.0.436234752.11 = STRING: "Ethernet1/54"
iso.0.8802.1.1.2.1.4.1.1.8.0.436207616.13 = STRING: "To-[WY-114-DB-SW93180-2]_Eth1/1"
iso.0.8802.1.1.2.1.4.1.1.8.0.436208128.12 = STRING: "To-[WY-114-DB-SW93180-2]_Eth1/2"
iso.0.8802.1.1.2.1.4.1.1.8.0.436208640.14 = STRING: "To-[WY-114-DB-SW93180-2]_Eth1/3"
iso.0.8802.1.1.2.1.4.1.1.8.0.436209152.15 = STRING: "To-[WY-114-DB-SW93180-2]_Eth1/4"
iso.0.8802.1.1.2.1.4.1.1.8.0.436217856.23 = STRING: "null"
iso.0.8802.1.1.2.1.4.1.1.8.0.436218368.21 = STRING: "null"
iso.0.8802.1.1.2.1.4.1.1.8.0.436218880.24 = STRING: "null"
iso.0.8802.1.1.2.1.4.1.1.8.0.436219392.22 = STRING: "null"
iso.0.8802.1.1.2.1.4.1.1.8.0.436229120.26 = STRING: "to_GT-DB-SW7009-2_E3/16"
iso.0.8802.1.1.2.1.4.1.1.8.0.436230144.8 = STRING: "To_[WY-114-DB-SW93180-2]_Eth1/45"
iso.0.8802.1.1.2.1.4.1.1.8.0.436230656.9 = STRING: "To_[WY-114-DB-SW93180-2]_Eth1/46"
iso.0.8802.1.1.2.1.4.1.1.8.0.436231168.6 = STRING: "To_[WY-114-DB-SW93180-2]_Eth1/47"
iso.0.8802.1.1.2.1.4.1.1.8.0.436231680.7 = STRING: "To_[WY-114-DB-SW93180-2]_Eth1/48"
iso.0.8802.1.1.2.1.4.1.1.8.0.436234240.10 = STRING: "To_[WY-114-DB-SW93180-2]_Eth1/53"
iso.0.8802.1.1.2.1.4.1.1.8.0.436234752.11 = STRING: "To_[WY-114-DB-SW93180-2]_Eth1/54"
iso.0.8802.1.1.2.1.4.1.1.9.0.436207616.13 = STRING: "WY-115-DB-SW3048-1"
iso.0.8802.1.1.2.1.4.1.1.9.0.436208128.12 = STRING: "WY-114-DB-SW3048-2"
iso.0.8802.1.1.2.1.4.1.1.9.0.436208640.14 = STRING: "WY-111-DB-SW3048-3"
iso.0.8802.1.1.2.1.4.1.1.9.0.436209152.15 = STRING: "WY-110-DB-SW3048-4"
iso.0.8802.1.1.2.1.4.1.1.9.0.436217856.23 = STRING: "null"
iso.0.8802.1.1.2.1.4.1.1.9.0.436218368.21 = STRING: "null"
iso.0.8802.1.1.2.1.4.1.1.9.0.436218880.24 = STRING: "null"
iso.0.8802.1.1.2.1.4.1.1.9.0.436219392.22 = STRING: "null"
iso.0.8802.1.1.2.1.4.1.1.9.0.436229120.26 = STRING: "N-A08-DB-SW92160-2"
iso.0.8802.1.1.2.1.4.1.1.9.0.436230144.8 = STRING: "WY-115-DB-SW93180-1"
iso.0.8802.1.1.2.1.4.1.1.9.0.436230656.9 = STRING: "WY-115-DB-SW93180-1"
iso.0.8802.1.1.2.1.4.1.1.9.0.436231168.6 = STRING: "WY-115-DB-SW93180-1"
iso.0.8802.1.1.2.1.4.1.1.9.0.436231680.7 = STRING: "WY-115-DB-SW93180-1"
iso.0.8802.1.1.2.1.4.1.1.9.0.436234240.10 = STRING: "WY-115-DB-SW93180-1"
iso.0.8802.1.1.2.1.4.1.1.9.0.436234752.11 = STRING: "WY-115-DB-SW93180-1"
iso.0.8802.1.1.2.1.4.1.1.10.0.436207616.13 = STRING: "Cisco Nexus Operating System (NX-OS) Software 7.0(3)I7(6)
TAC support: http://www.cisco.com/tac
Copyright (c) 2002-2019, Cisco Systems, Inc. All rights reserved."
iso.0.8802.1.1.2.1.4.1.1.10.0.436208128.12 = STRING: "Cisco Nexus Operating System (NX-OS) Software 7.0(3)I7(6)
TAC support: http://www.cisco.com/tac
Copyright (c) 2002-2019, Cisco Systems, Inc. All rights reserved."
iso.0.8802.1.1.2.1.4.1.1.10.0.436208640.14 = STRING: "Cisco Nexus Operating System (NX-OS) Software 7.0(3)I7(6)
TAC support: http://www.cisco.com/tac
Copyright (c) 2002-2019, Cisco Systems, Inc. All rights reserved."
iso.0.8802.1.1.2.1.4.1.1.10.0.436209152.15 = STRING: "Cisco Nexus Operating System (NX-OS) Software 7.0(3)I7(6)
TAC support: http://www.cisco.com/tac
Copyright (c) 2002-2019, Cisco Systems, Inc. All rights reserved."
iso.0.8802.1.1.2.1.4.1.1.10.0.436217856.23 = STRING: "null"
iso.0.8802.1.1.2.1.4.1.1.10.0.436218368.21 = STRING: "null"
iso.0.8802.1.1.2.1.4.1.1.10.0.436218880.24 = STRING: "null"
iso.0.8802.1.1.2.1.4.1.1.10.0.436219392.22 = STRING: "null"
iso.0.8802.1.1.2.1.4.1.1.10.0.436229120.26 = STRING: "Cisco Nexus Operating System (NX-OS) Software 7.0(3)I4(7)
TAC support: http://www.cisco.com/tac
Copyright (c) 2002-2017, Cisco Systems, Inc. All rights reserved."
iso.0.8802.1.1.2.1.4.1.1.10.0.436230144.8 = STRING: "Cisco Nexus Operating System (NX-OS) Software 7.0(3)I7(6)
TAC support: http://www.cisco.com/tac
Copyright (c) 2002-2019, Cisco Systems, Inc. All rights reserved."
iso.0.8802.1.1.2.1.4.1.1.10.0.436230656.9 = STRING: "Cisco Nexus Operating System (NX-OS) Software 7.0(3)I7(6)
TAC support: http://www.cisco.com/tac
Copyright (c) 2002-2019, Cisco Systems, Inc. All rights reserved."
iso.0.8802.1.1.2.1.4.1.1.10.0.436231168.6 = STRING: "Cisco Nexus Operating System (NX-OS) Software 7.0(3)I7(6)
TAC support: http://www.cisco.com/tac
Copyright (c) 2002-2019, Cisco Systems, Inc. All rights reserved."
iso.0.8802.1.1.2.1.4.1.1.10.0.436231680.7 = STRING: "Cisco Nexus Operating System (NX-OS) Software 7.0(3)I7(6)
TAC support: http://www.cisco.com/tac
Copyright (c) 2002-2019, Cisco Systems, Inc. All rights reserved."
iso.0.8802.1.1.2.1.4.1.1.10.0.436234240.10 = STRING: "Cisco Nexus Operating System (NX-OS) Software 7.0(3)I7(6)
TAC support: http://www.cisco.com/tac
Copyright (c) 2002-2019, Cisco Systems, Inc. All rights reserved."
iso.0.8802.1.1.2.1.4.1.1.10.0.436234752.11 = STRING: "Cisco Nexus Operating System (NX-OS) Software 7.0(3)I7(6)
TAC support: http://www.cisco.com/tac
Copyright (c) 2002-2019, Cisco Systems, Inc. All rights reserved."
iso.0.8802.1.1.2.1.4.1.1.11.0.436207616.13 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.11.0.436208128.12 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.11.0.436208640.14 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.11.0.436209152.15 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.11.0.436217856.23 = Hex-STRING: 00 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.11.0.436218368.21 = Hex-STRING: 00 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.11.0.436218880.24 = Hex-STRING: 00 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.11.0.436219392.22 = Hex-STRING: 00 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.11.0.436229120.26 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.11.0.436230144.8 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.11.0.436230656.9 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.11.0.436231168.6 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.11.0.436231680.7 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.11.0.436234240.10 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.11.0.436234752.11 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.12.0.436207616.13 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.12.0.436208128.12 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.12.0.436208640.14 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.12.0.436209152.15 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.12.0.436217856.23 = Hex-STRING: 00 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.12.0.436218368.21 = Hex-STRING: 00 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.12.0.436218880.24 = Hex-STRING: 00 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.12.0.436219392.22 = Hex-STRING: 00 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.12.0.436229120.26 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.12.0.436230144.8 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.12.0.436230656.9 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.12.0.436231168.6 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.12.0.436231680.7 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.12.0.436234240.10 = Hex-STRING: 28 00 00 00 
iso.0.8802.1.1.2.1.4.1.1.12.0.436234752.11 = Hex-STRING: 28 00 00 00 """

    get_lldpRemEntry(data)
