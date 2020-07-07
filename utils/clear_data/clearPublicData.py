# -*- coding: utf-8 -*-
import re, threading
if_name = 'if_name'
phys_addr = 'phys_addr'
oper_status = 'oper_status'
admin_status = 'admin_status'
speed = 'speed'
mtu = 'mtu'
type = 'type'

# t = threading.currentThread()


# 整合公共oid的数据
class CleanPublicData(object):
    def __init__(self):
        """
        :param data: 每台机器才回来的数据，待合并
        """
        self.port_info_list = {}  # 每个端口的详情信息

    # 数据整理- 处理基本信息
    def _dealdescription(self):
        """
        处理网络接口信息
        :return:
        """
        try:
            # 网络接口列表: 网络接口标识符 = 设备名 + ":" + 端口
            if self.data.get('ifDescr'):
                self.sysName = self.data.get('sysName')  # 设备名称
                for descr in self.data.get('ifDescr'):
                    # 判断k是否存在，不存在则初始化
                    if not self.port_info_list.has_key(descr[0]):
                        self.port_info_list[descr[0]] = {}
                    self.port_info_list[descr[0]].update({"name": str(self.sysName) + ":" + descr[
                        1]})  # 网络接口标识符 [(u '1', u 'Vlan1'), (u '255', u 'Vlan255')]

                    # 网卡名
                    self.port_info_list[descr[0]].update({if_name: descr[1]})

                # 合并完网卡描叙后 删除ifName， ifDescr
                del self.data['ifDescr']
                del self.data['ifName']

            # 端口mac地址
            if self.data.get('macaddr'):  # [(u '1', u '6c:5e:3b:2a:40:c0'), (u '255', u '6c:5e:3b:2a:40:c1')]
                for descr in self.data.get('macaddr'):
                    # 判断k是否存在，不存在则初始化
                    if not self.port_info_list.has_key(descr[0]):
                        self.port_info_list[descr[0]] = {}
                    self.port_info_list[descr[0]].update({phys_addr: descr[1].upper()})

                # 合并完网卡描叙后 删除mac
                del self.data['macaddr']

            # speed 速率
            if self.data.get('speed'):
                for descr in self.data.get('speed'):
                    # 判断k是否存在，不存在则初始化
                    if not self.port_info_list.has_key(descr[0]):
                        self.port_info_list[descr[0]] = {}
                    self.port_info_list[descr[0]].update({speed: descr[1]})

                # 合并完网卡描叙后 删除speed
                del self.data['speed']

            # oper_status 状态
            if self.data.get('operstatus'):
                for descr in self.data.get('operstatus'):
                    # 判断k是否存在，不存在则初始化
                    if not self.port_info_list.has_key(descr[0]):
                        self.port_info_list[descr[0]] = {}
                    self.port_info_list[descr[0]].update({oper_status: descr[1]})

                # 合并完网卡描叙后 删除oper_status
                del self.data['operstatus']

            # admin_status 状态
            if self.data.get('adminstatus'):
                for descr in self.data.get('adminstatus'):
                    # 判断k是否存在，不存在则初始化
                    if not self.port_info_list.has_key(descr[0]):
                        self.port_info_list[descr[0]] = {}
                    self.port_info_list[descr[0]].update({admin_status: descr[1]})

                # 合并完网卡描叙后 删除 admin_status
                del self.data['adminstatus']

            # mut
            if self.data.get('mtu'):
                for descr in self.data.get('mtu'):
                    # 判断k是否存在，不存在则初始化
                    if not self.port_info_list.has_key(descr[0]):
                        self.port_info_list[descr[0]] = {}
                    self.port_info_list[descr[0]].update({mtu: descr[1]})

                # 合并完网卡描叙后 删除mtu
                del self.data['mtu']

            # type 端口类型
            if self.data.get('type'):
                for descr in self.data.get('type'):
                    # 判断k是否存在，不存在则初始化
                    if not self.port_info_list.has_key(descr[0]):
                        self.port_info_list[descr[0]] = {}
                    self.port_info_list[descr[0]].update({type: descr[1]})

                # 合并完网卡描叙后 删除 type
                del self.data['type']

            # 初始化remote_list
            for k in self.port_info_list:
                self.port_info_list[k]['remote_list'] = []

            # 加入到data数据中
            self.data['port_info_list'] = self.port_info_list
        except Exception as e:
            print "数据整理- 处理基本信息: " + str(e)

    # 数据整理- 处理 MAC/PORT 表
    def _dealmacporttable(self):
        dot1dBasePortIfIndex = self.data.get('dot1dBasePortIfIndex', '')  # 取出端口和索引的关系
        dot1qTpFdbMac = self.data.get('dot1qTpFdbMac', '')
        dot1qTpFdbPort = self.data.get('dot1qTpFdbPort', '')  # 取出端口和mac地址十进制之间的关系
        # print dot1dBasePortIfIndex
        # print dot1qTpFdbPort
        # {u'49': u'10149', u'51': u'10151', u'50': u'10150', u'456': u'5001', u'52': u'10152'}
        # {u'96.8.16.192.174.0': u'456', u'96.8.16.192.174.2': u'456', u'0.224.252.9.188.249': u'456'}

        # print dot1qTpFdbMac
        # [u'0.224.252.9.188.249 = Hex-STRING: 00 E0 FC 09 BC F9 ', u'96.8.16.192.174.0 = Hex-STRING: 60 08 10 C0 AE 00 ',
        #  u'96.8.16.192.174.2 = Hex-STRING: 60 08 10 C0 AE 02 ']

        # 2. mac单独处理，且dot1qTpFdbMac是原始数据
        mac_port_result = {}

        # 3. 判断是否采集到数据
        if dot1dBasePortIfIndex and dot1qTpFdbMac and dot1qTpFdbPort:
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

        # TODO 下面要根据不同vlan采集信息
        self.data['mac_port_table'].update(mac_port_result)
        del self.data['dot1dBasePortIfIndex']
        del self.data['dot1qTpFdbMac']
        del self.data['dot1qTpFdbPort']

    # 根据cdp或lldp协议获取端口对方的mac地址信息
    def _deallldpRemEntry(self):
        try:
            # 1. 对端信息 lldpRemEntr
            lldpRemEntry = self.data.get('lldpRemEntry', '')
            # 2. lldpLocPortDesc
            localPortDic = self.data.get('localPortDic', '')

            if lldpRemEntry and localPortDic:
                # 循环遍历对端字典
                for k, v in lldpRemEntry.items():
                    # 1. 取对端标识符描叙
                    peer_device = v.get('peer_device', '')
                    # 2. 判断描述是否存在
                    if peer_device:
                        # 2.1 拼接端口标识符
                        v['name'] = v['peer_device'] + ":" + v['peer_port']

                        local_port = localPortDic[k]
                        # 3. 循环端口信息
                        for port_k, port_v in self.data.get('port_info_list').items():

                            # 3.2 判断对端的k 和端口详情的k是否相等
                            if port_v[if_name] == str(local_port):
                                self.data.get('port_info_list')[str(port_k)]['remote_list'].append(v)

                del self.data['lldpRemEntry']
                del self.data['localPortDic']

        except Exception as e:
            print '根据cdp或lldp协议获取端口对方的mac地址信息, ' + str(e)

    # 处理端口模型的对端列表数据
    def _dealprocess_netd_port_remote_list(self):
        try:
            mac_port_table = self.data.get('mac_port_table', '')
            listPortChannel = self.data.get('portChannel')['listPortChannel']
            dict_arp = self.data.get('ipNetToMediaPhysAddress')['dict_arp']

            if mac_port_table and listPortChannel and dict_arp:
                for mac, port in mac_port_table.items():
                    # 判断端口是否在端口信息里面
                    if not self.data.get('port_info_list').has_key(str(port)):
                        continue

                    # 判断端口是否为聚合端口
                    if port in listPortChannel:
                        continue

                    # 判断mac是否在mac-ip表，若存在，则取出对应ip
                    if mac in dict_arp.keys():
                        dict_arp_ip = dict_arp[mac]
                        data = {
                            'name': "unknown",
                            'peer_type': "unknown",
                            'peer_mac': mac,
                            'peer_port': "unknown",
                            'peer_device': "unknown",
                            'peer_ip': dict_arp_ip
                        }
                    else:
                        data = {
                            'name': 'unknown',
                            'peer_type': "unknown",
                            'peer_mac': mac,
                            'peer_port': "unknown",
                            'peer_device': 'unknown',
                            'peer_ip': 'unknown'
                        }

                    # 把数据添加到remote_list 里面
                    self.data.get('port_info_list')[str(port)]['remote_list'].append(data)

                    # 判断端口名称是否为port-channel，类型是否为 propVirtual 然后清空 remote_list
                    for port, info in self.data.get('port_info_list').items():
                        if info['type'] == 'propVirtual' and 'port-channel' in info[if_name].lower():
                            info['remote_list'] = []
                            # 赋值到self.data
                            self.data.get('port_info_list')[port] = info

        except Exception as e:
            print '处理端口模型的对端列表数据, ' + str(e)

    def run(self, data):
        self.data = data
        self._dealdescription()  # 数据整理- 处理基本信息
        self._dealmacporttable()  # 数据整理- 处理 MAC/PORT 表
        self._deallldpRemEntry()  # 根据cdp或lldp协议获取端口对方的mac地址信息
        self._dealprocess_netd_port_remote_list()  # 处理端口模型的对端列表数据
        return self.data
