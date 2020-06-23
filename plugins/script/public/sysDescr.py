# -*- coding: utf-8 -*-
"""
Cisco:
    SNMPv2-MIB::sysDescr.0 = STRING: Cisco Internetwork Operating System Software
    IOS (tm) C2950 Software (C2950-I6Q4L2-M), Version 12.1(13)EA1, RELEASE SOFTWARE (fc1)
    Copyright (c) 1986-2003 by cisco Systems, Inc.
    Compiled Tue 04-Mar-03 02:14 by yenanh

    SNMPv2-MIB::sysDescr.0 = STRING: Cisco IOS Software, C2960 Software (C2960-LANBASE-M), Version 12.2(25)SEE, RELEASE SOFTWARE (fc2)
    Copyright (c) 1986-2006 by Cisco Systems, Inc.
    Compiled Thu 02-Feb-06 18:53 by antonino

    SNMPv2-MIB::sysDescr.0 = STRING: Cisco IOS Software, C3560E Software (C3560E-UNIVERSALK9-M), Version 12.2(55)SE3, RELEASE SOFTWARE (fc1)
    Technical Support: http://www.cisco.com/techsupport
    Copyright (c) 1986-2011 by Cisco Systems, Inc.
    Compiled Thu 05-May-11 15:57 by prod_rel_team

    SNMPv2-MIB::sysDescr.0 = STRING: Cisco IOS Software [Fuji], Catalyst L3 Switch Software (CAT3K_CAA-UNIVERSALK9-M), Version 16.9.4, RELEASE SOFTWARE (fc2);
    Technical Support: http://www.cisco.com/techsupport;
    Copyright (c) 1986-2019 by Cisco Systems, Inc.;Compiled Thu 22-Aug-19 17:33 by

    firewall RV325
    SNMPv2-MIB::sysDescr.0 = STRING: Linux, Cisco RV325, Version 1.3.2.02 Fri Sep 23 15:19:56 CST 2016

H3C:
    SNMPv2-MIB::sysDescr.0 = STRING: H3C Switch S5110-52P-PWR Software Version 5.20.99, Release 1111
    Copyright(c)2004-2016 Hangzhou H3C Tech. Co., Ltd. All rights reserved.

    SNMPv2-MIB::sysDescr.0 = STRING: H3C Comware Platform Software, Software Version 7.1.048, Release 7353P16
    H3C SR8808-X
    Copyright (c) 2004-2017 Hangzhou H3C Tech. Co., Ltd. All rights reserved.

New H3C:
    SNMPv2-MIB::sysDescr.0 = STRING: H3C Comware Platform Software, Software Version 7.1.075, Release 7751P11
    H3C SR8804-X
    Copyright (c) 2004-2019 New H3C Technologies Co., Ltd. All rights reserved.

Huawei:
    SNMPv2-MIB::sysDescr.0 = STRING: S5720-52X-LI-AC
    Huawei Versatile Routing Platform Software
    VRP (R) software,Version 5.170 (S5720 V200R010C00SPC600)
    Copyright (C) 2007 Huawei Technologies Co., Ltd.

    SNMPv2-MIB::sysDescr.0 = STRING: Quidway S7706
    Huawei Versatile Routing Platform Software
    VRP (R) Software, Version 5.170 (S7700 V200R010C00SPC600)
    Copyright (c) 2000-2016 Huawei Technologies Co., Ltd
"""
import re, time


# 基本信息 OID="sysDescr" 返回数据  sys_descr 品牌 型号 软件版本 信息
def get_sysDescr(data):
    result = {}

    txtData = data.replace("\r\n", ';')
    if len(txtData) == 0:
        return result

    sysDescrList = re.findall(r'.sysDescr.0 = STRING: (.*)', txtData)
    if sysDescrList:
        sysDescr = sysDescrList[0]
    else:
        sysDescr = ""
    result['sysDescr'] = sysDescr

    brand = 'unknown'
    brandList = ["New H3C", "H3C", "HUAWEI", "Cisco", "DELL", "Juniper"]
    if len(sysDescr) > 0:
        ## 思科防火墙 RV32x 返回数据没有copyright
        copyright = sysDescr.split('Copyright')
        if copyright and len(copyright) > 1:
            brandStr = copyright[1]
        else:
            brandStr = sysDescr
        for i in brandList:
            m = re.search(i, brandStr, re.I)
            if m:
                brand = i
                break

    # 品牌
    result['brand'] = brand

    # 型号
    sys_model = 'unknown type'
    if brand.lower() == "new h3c" or brand.lower() == "h3c":
        sys_descr = sysDescr.split()
        if sys_descr[1].lower() == "switch":
            sys_model = sys_descr[2]
        else:
            sys_model = sysDescr.split(';')[1].split(' ')[1]
    elif brand.lower() == "huawei":
        sys_model = sysDescr.split(';')[0]
    elif brand.lower() == "cisco":
        tmp = re.findall(r'Software (\(.*\)),', sysDescr)
        if tmp:
            sys_model = tmp[0][1:-1]
        else:
            # SNMPv2-MIB::sysDescr.0 = STRING: Linux, Cisco RV325, Version 1.3.2.02 Fri Sep 23 15:19:56 CST 2016
            sys_model = sysDescr.split(',')[1].lstrip().split(' ')[1]
            sys_version = sysDescr.split(',')[2]
    elif brand.lower() == "juniper":
        sys_model = sysDescr.split(',')[1].split(' ')[2]
        sys_version = sysDescr.split(',')[2]

    result['sysModel'] = sys_model

    # 软件版本
    if brand == 'DELL':
        sys_version_list = re.findall(r'.sysDescr.0 = STRING: (.*)', data)
        if sys_version_list:
            result['sysVersion'] = sys_version_list[0].split(',')[1].replace(',', '')
        else:
            result['sysVersion'] = "unknown version"
    elif brand == 'Juniper':
        result['sysVersion'] = sysDescr.split(',')[2]
    else:
        sys_version_list = re.findall(r'.Version (.*)', sysDescr)
        if sys_version_list:
            result['sysVersion'] = sys_version_list[0].split(' ')[0].replace(',', '')
        else:
            result['sysVersion'] = "unknown version"

    return result
