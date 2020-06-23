# -*- coding: utf-8 -*-
import re

# vlan
def get_vlan(data):
    result = {}
    vlan_list = re.findall(r'9.9.46.1.3.1.1.18(.*)', data)
    vlan = set()
    if vlan_list:
        for i in vlan_list:
            get_vlan = i.split(" ")[-1]
            try:
                get_vlan = int(get_vlan)
                if get_vlan:
                    vlan.add(str(get_vlan))
            except:
                pass

    result['vlan'] = list(vlan)

    return result