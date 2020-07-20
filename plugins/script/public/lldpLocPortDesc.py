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


if __name__ == '__main__':
    data = """
iso.0.8802.1.1.2.1.3.7.1.4.83886080 = STRING: "mgmt0"
iso.0.8802.1.1.2.1.3.7.1.4.436207616 = STRING: "Ethernet1/1"
iso.0.8802.1.1.2.1.3.7.1.4.436208128 = STRING: "Ethernet1/2"
iso.0.8802.1.1.2.1.3.7.1.4.436208640 = STRING: "Ethernet1/3"
iso.0.8802.1.1.2.1.3.7.1.4.436209152 = STRING: "Ethernet1/4"
iso.0.8802.1.1.2.1.3.7.1.4.436209664 = STRING: "Ethernet1/5"
iso.0.8802.1.1.2.1.3.7.1.4.436210176 = STRING: "Ethernet1/6"
iso.0.8802.1.1.2.1.3.7.1.4.436210688 = STRING: "Ethernet1/7"
iso.0.8802.1.1.2.1.3.7.1.4.436211200 = STRING: "Ethernet1/8"
iso.0.8802.1.1.2.1.3.7.1.4.436211712 = STRING: "Ethernet1/9"
iso.0.8802.1.1.2.1.3.7.1.4.436212224 = STRING: "Ethernet1/10"
iso.0.8802.1.1.2.1.3.7.1.4.436212736 = STRING: "Ethernet1/11"
iso.0.8802.1.1.2.1.3.7.1.4.436213248 = STRING: "Ethernet1/12"
iso.0.8802.1.1.2.1.3.7.1.4.436213760 = STRING: "Ethernet1/13"
iso.0.8802.1.1.2.1.3.7.1.4.436214272 = STRING: "Ethernet1/14"
iso.0.8802.1.1.2.1.3.7.1.4.436214784 = STRING: "Ethernet1/15"
iso.0.8802.1.1.2.1.3.7.1.4.436215296 = STRING: "Ethernet1/16"
iso.0.8802.1.1.2.1.3.7.1.4.436215808 = STRING: "Ethernet1/17"
iso.0.8802.1.1.2.1.3.7.1.4.436216320 = STRING: "Ethernet1/18"
iso.0.8802.1.1.2.1.3.7.1.4.436216832 = STRING: "Ethernet1/19"
iso.0.8802.1.1.2.1.3.7.1.4.436217344 = STRING: "Ethernet1/20"
iso.0.8802.1.1.2.1.3.7.1.4.436217856 = STRING: "Ethernet1/21"
iso.0.8802.1.1.2.1.3.7.1.4.436218368 = STRING: "Ethernet1/22"
iso.0.8802.1.1.2.1.3.7.1.4.436218880 = STRING: "Ethernet1/23"
iso.0.8802.1.1.2.1.3.7.1.4.436219392 = STRING: "Ethernet1/24"
iso.0.8802.1.1.2.1.3.7.1.4.436219904 = STRING: "Ethernet1/25"
iso.0.8802.1.1.2.1.3.7.1.4.436220416 = STRING: "Ethernet1/26"
iso.0.8802.1.1.2.1.3.7.1.4.436220928 = STRING: "Ethernet1/27"
iso.0.8802.1.1.2.1.3.7.1.4.436221440 = STRING: "Ethernet1/28"
iso.0.8802.1.1.2.1.3.7.1.4.436221952 = STRING: "Ethernet1/29"
iso.0.8802.1.1.2.1.3.7.1.4.436222464 = STRING: "Ethernet1/30"
iso.0.8802.1.1.2.1.3.7.1.4.436222976 = STRING: "Ethernet1/31"
iso.0.8802.1.1.2.1.3.7.1.4.436223488 = STRING: "Ethernet1/32"
iso.0.8802.1.1.2.1.3.7.1.4.436224000 = STRING: "Ethernet1/33"
iso.0.8802.1.1.2.1.3.7.1.4.436224512 = STRING: "Ethernet1/34"
iso.0.8802.1.1.2.1.3.7.1.4.436225024 = STRING: "Ethernet1/35"
iso.0.8802.1.1.2.1.3.7.1.4.436225536 = STRING: "Ethernet1/36"
iso.0.8802.1.1.2.1.3.7.1.4.436226048 = STRING: "Ethernet1/37"
iso.0.8802.1.1.2.1.3.7.1.4.436226560 = STRING: "Ethernet1/38"
iso.0.8802.1.1.2.1.3.7.1.4.436227072 = STRING: "Ethernet1/39"
iso.0.8802.1.1.2.1.3.7.1.4.436227584 = STRING: "Ethernet1/40"
iso.0.8802.1.1.2.1.3.7.1.4.436228096 = STRING: "Ethernet1/41"
iso.0.8802.1.1.2.1.3.7.1.4.436228608 = STRING: "Ethernet1/42"
iso.0.8802.1.1.2.1.3.7.1.4.436229120 = STRING: "Ethernet1/43"
iso.0.8802.1.1.2.1.3.7.1.4.436229632 = STRING: "Ethernet1/44"
iso.0.8802.1.1.2.1.3.7.1.4.436230144 = STRING: "Ethernet1/45"
iso.0.8802.1.1.2.1.3.7.1.4.436230656 = STRING: "Ethernet1/46"
iso.0.8802.1.1.2.1.3.7.1.4.436231168 = STRING: "Ethernet1/47"
iso.0.8802.1.1.2.1.3.7.1.4.436231680 = STRING: "Ethernet1/48"
iso.0.8802.1.1.2.1.3.7.1.4.436232192 = STRING: "Ethernet1/49"
iso.0.8802.1.1.2.1.3.7.1.4.436232704 = STRING: "Ethernet1/50"
iso.0.8802.1.1.2.1.3.7.1.4.436233216 = STRING: "Ethernet1/51"
iso.0.8802.1.1.2.1.3.7.1.4.436233728 = STRING: "Ethernet1/52"
iso.0.8802.1.1.2.1.3.7.1.4.436234240 = STRING: "Ethernet1/53"
iso.0.8802.1.1.2.1.3.7.1.4.436234752 = STRING: "Ethernet1/54"
"""
    get_lldpLocPortDesc(data)
