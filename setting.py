#!/usr/local/easyops/python/bin/python
# -*- coding: utf-8 -*-

# cmdb平台账号信息
# 广汽配置
easyops_cmdb_host = '16.16.1.72'
easyops_org = '9070'
easy_user = 'easyops'

# 公司配置
# easyops_cmdb_host = '192.168.10.144'
# easyops_org = '6620162'
# easy_user = 'easyops'

# demo配置
# easyops_cmdb_host = '119.147.214.51:1082'
# easyops_org = '6859096'
# easy_user = 'easyops'


# header配置
easy_domain = 'cmdb_resource.easyops-only.com'
headers = {'host': easy_domain, 'org': easyops_org, 'user': easy_user, 'content-Type': 'application/json'}

# 搜索实例配置，注意搜索的属性，有些人 ip对应ip，有些是name对应ip
# 示例
# params = {
#     "query": {
#         "auto_collect": {"$eq": "yes"}
#     },
#     "fields": {
#         "name": True,
#         "community": True,
#         "sys_name": True,
#         "ip": True
#     }
# }

# 搜索所有实例数据的ID
ConfigSWITCHMODEL = '_SWITCH'

# 在实例里面的团体字属性名称，ip地址属性的名称，有些人的ip叫IP属性，有些人ip叫name属性
community = 'community'
ip = 'ip'

# 搜索实列列表条件
ConfigParams = {
    "fields": {
        "name": True,
        community: True,
        ip: True
    }
}

# 模型配置,请先到cmdb中配置好
setting_model = {
    # 交换机模型基本属性
    "model_id": "_SWITCH",  # 模型ID
    "to_port_id": "port_list",  # 交换机 --> 网络设备端口 别名ID
    "fields": {
        "upTime": "启动时间",
        "ip": "管理IP",
        "brand": "品牌",
        "netMask": "网关",
        "sysDescr": "系统描叙",
        "sysVersion": "版本号",
        "sysName": "系统名称",
        "sysModel": "型号",
        "sn": "序列号",
    },

    # 端口基本属性
    "pk": "name",  # 网络端口模型主键
    "port_modol_id": "NETDPORT",  # 网络端口模型ID
    "port_info_list": {
        "operstatus": "OperStatus",
        "adminstatus": "AdminStatus",
        "type": "类型",
        "name": "标识符",  # 要设置唯一，一般用默认创建的name属性
        "macaddr": "物理地址",
        "speed": "协商速率",
        "ifname": "端口名",
        "mtu": "MTU",
        "vlan": "vlan",
        "remote_list": [{
            "name": "端口名",
            "peer_type": "对端类型",
            "peer_port": "对端端口",
            "peer_device": "对端设备",
            "peer_mac": "对端物理地址",
            "peer_ip": "对端ip"
        }]
    }

}

# 采集开关，on 获取现网数据，并保存到data目录下， load 获取data本地数据, deal处理完数据后插入到cmdb中
switc = 'deal'  # 默认deal

# 最大线程数量，默认开启10个进程
pool_nums = 20

# 执行shell命令超时时间
timeout = 3

# 勿动，公共OID，
plugins_oid = {
    'public_oid': {
        'ipAdEnt': '.1.3.6.1.2.1.4.20',  # ok  交换机关联IP，包括管理IP,VLAN IP
        'sysDescr': '1.3.6.1.2.1.1.1.0',  # ok  基本信息 OID="sysDescr" 返回数据  sys_descr 品牌 型号 软件版本 信息
        'sysName': '1.3.6.1.2.1.1.5.0',  # ok  ifDescr拼接成网卡标识 sysname + ":" + ifDescr
        'snmpEngineId': '.1.3.6.1.6.3.10.2.1.3',  # ok  启动时间
        'IfDescr': '1.3.6.1.2.1.2.2.1.2',  # ok 网络接口信息描述
        'IfName': '1.3.6.1.2.1.31.1.1.1.1',  # ok  端口名称
        'IfType': '.1.3.6.1.2.1.2.2.1.3',  # ok   交换机端口 - 类型
        'IfOperStatus': '.1.3.6.1.2.1.2.2.1.8',  # ok  交换机端口 - 状态
        'IfAdminStatus': '.1.3.6.1.2.1.2.2.1.7',  # ok  交换机端口 - 管理状态 : up
        'IfPhysAddress': '.1.3.6.1.2.1.2.2.1.6',  # ok  换机端口 - 物理地址 MAC 地址 或 0.0.0.0
        'IfSpeed': '.1.3.6.1.2.1.2.2.1.5',  # ok 交换机端口 - 协商速率
        'IfMTU': '.1.3.6.1.2.1.2.2.1.4',  # ok   交换机端口 - MTU : 9600 或 1500
        'IpNetToMediaPhysAddress': '.1.3.6.1.2.1.4.22.1.2',  # arp信息
        'dot1dBasePortIfIndex': '1.3.6.1.2.1.17.1.4.1.2',
        'dot1qTpFdbPort': '1.3.6.1.2.1.17.4.3.1.2',
        'dot1qTpFdbMac': '1.3.6.1.2.1.17.4.3.1.1',
        'portChannel': 'iso.2.840.10006.300.43.1.2.1.1.13',  # 聚合端口
        'lldpRemEntry': '1.0.8802.1.1.2.1.4.1.1',
        'vlan': '1.3.6.1.4.1.9.9.46.1.3.1.1.18',
        'lldpLocPortDesc': '1.0.8802.1.1.2.1.3.7.1.4'
    },
    'cisco_oid': {
        'vmVlan': '.1.3.6.1.4.1.9.9.68.1.2.2.1.2',
        'cdpCacheSysName': '1.3.6.1.4.1.9.9.23.1.2.1.1.6',
        'cdpCachePortName': '1.3.6.1.4.1.9.9.23.1.2.1.1.7',
        'cdpCacheType': '1.3.6.1.4.1.9.9.23.1.2.1.1.3',
        'cdpCacheIP': '1.3.6.1.4.1.9.9.23.1.2.1.1.4',
        'cisco_serial': '1.3.6.1.2.1.47.1.1.1.1.11',
        'cisco_module': '1.3.6.1.2.1.47.1.1.1.1.13',
    },
    'other_oid': {
        'dot1dBasePortIfIndex': '1.3.6.1.2.1.17.1.4.1.2',
        'dot1qTpFdbPort': '1.3.6.1.2.1.17.4.3.1.2',
        'dot1qTpFdbMac': '1.3.6.1.2.1.17.4.3.1.1'
    }
}
