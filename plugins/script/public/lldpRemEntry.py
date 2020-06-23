# -*- coding: utf-8 -*-
import re


# 获取cdp或lldp协议端口信息
def get_lldpRemEntry(data):
    result = {}
    remote_list = {}

    #### peer_mac -> 1.0.8802.1.1.2.1.4.1.1.5 (lldpRemChassisId) ####
    peerMacList = re.findall(r'iso.0.8802.1.1.2.1.4.1.1.5.(.*)', data)
    for i in peerMacList:
        if "Hex-STRING" in i:
            idx = i.split()[0].split(".")[1]
            peer_mac_list = re.findall(r'. Hex-STRING: (.*) ', i)
            if peer_mac_list:
                peer_mac = peer_mac_list[0].replace(' ', ':').upper()
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
        # if peer_mac_list:
        #     peer_mac = peer_mac_list[0].replace(' ',':').upper()
        # else:
        if remote_list.has_key(idx):
            if remote_list[idx].has_key('peer_mac'):
                remote_list[idx]['peer_mac'] = peer_mac
            else:
                remote_list[idx] = {'peer_mac': peer_mac}
        else:
            remote_list[idx] = {'peer_mac': peer_mac}

    #### peer_type -> 1.0.8802.1.1.2.1.4.1.1.6 (lldpRemPortIdSubtype) ####
    peerType = re.findall(r'iso.0.8802.1.1.2.1.4.1.1.6.(.*)', data)
    for i in peerType:
        idx = i.split('.')[1]
        peer_type = i.split(' ')[3]
        if remote_list.has_key(idx):
            remote_list[idx]['peer_type'] = peer_type
        else:
            remote_list[idx] = {'peer_type': peer_type}

    #### peer_port -> 1.0.8802.1.1.2.1.4.1.1.7 (lldpRemPortId) ####
    peerPortList = re.findall(r'iso.0.8802.1.1.2.1.4.1.1.7.(.*)', data)
    for i in peerPortList:
        idx = i.split('.')[1]
        peer_port_list = re.findall(r'."(.*)"', i)
        if peer_port_list:
            peer_port = peer_port_list[0]
        else:
            peer_port = 0
        # peer_port = re.findall(r'."(.*)"',i)[0]

        if remote_list.has_key(idx):
            remote_list[idx]['peer_port'] = peer_port
        else:
            remote_list[idx] = {'peer_port': peer_port}

    #### peer_port_desc (port_desc) -> 1.0.8802.1.1.2.1.4.1.1.8 (lldpRemPortDesc) ####
    portDescList = re.findall(r'iso.0.8802.1.1.2.1.4.1.1.8.(.*)', data)
    for i in portDescList:
        idx = i.split('.')[1]
        port_desc = re.findall(r'."(.*)"', i)[0]
        if remote_list.has_key(idx):
            remote_list[idx]['peer_port_desc'] = port_desc
        else:
            remote_list[idx] = {'peer_port_desc': port_desc}

    #### peer_device (sys_name) --> 1.0.8802.1.1.2.1.4.1.1.9 (lldpRemSysName) ####
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
