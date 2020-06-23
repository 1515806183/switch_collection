# -*- coding: utf-8 -*-


# 整合思科设备数据
class CleanCiscoData(object):

    # 处理 思科sn， 型号，vlan信息
    def _deal_indof(self):
        # 1. 取sn号
        cisco_sn = self.data.get('cisco_serial')
        if cisco_sn:
            cisco_sn = cisco_sn.values()[0]
        else:
            cisco_sn = ''

        # 删除旧数据
        del self.data['cisco_serial']
        # 更新新数据
        self.data['sn'] = cisco_sn

        # 2. 取型号
        cisco_module = self.data.get('cisco_module')
        if cisco_module:
            cisco_module = cisco_module.values()[0]
        else:
            cisco_module = ''

        # 删除旧数据
        del self.data['cisco_module']
        # 更新新数据
        self.data['moduleOther'] = cisco_module

        # 3. 处理vlan
        vlan_info = []
        cisco_valn = self.data.get('cisco_vmVlan')

        # 将每个vlan加入端口信息内
        for port_key in self.data.get('port_info_list'): # 每个端口信息

            if cisco_valn.has_key(port_key):
                valn_vlaus = str(cisco_valn.get(port_key))
                self.data.get('port_info_list')[port_key].update({"vlan": valn_vlaus})
                # 这个到后面要根据不同的vlan进行处理
                if valn_vlaus not in vlan_info and valn_vlaus != '1':
                    vlan_info.append(valn_vlaus)

        # 把它加到总数据里面，这里没法处理，最后在处理
        self.data['valn_info'] = vlan_info
        # 删除旧数据
        del self.data['cisco_vmVlan']

    # 整合对端设备信息，废弃
    def _dael_remote_list(self):
        # 1. 先处理对端ip信息
        cisco_remote_ip_not_deal = self.data.get('cisco_remote_ip_not_deal')
        cisco_remote_sys_type = self.data.get('cisco_remote_sys_type')

        if cisco_remote_ip_not_deal:
            # 如果type为1，则为IP
            for remote_ip_key, remote_ip_val in dict(cisco_remote_ip_not_deal).items():
                if cisco_remote_sys_type[remote_ip_key] == 1:
                    # 十六进制转换为十进制
                    res_ip = ''
                    for ip in remote_ip_val.split():
                        res_ip += (str(int(ip, 16)) + '.')

                    # 组合数据回cisco_remote_ip_not_deal
                    cisco_remote_ip_not_deal[remote_ip_key] = res_ip[:-1]
                # type 不为1，则删除
                else:
                    del self.data['cisco_remote_sys_type'][str(remote_ip_key)]

        cisco_remote_sys_name = self.data.get('cisco_remote_sys_name')
        cisco_remote_portName = self.data.get('cisco_remote_portName')

        # 2. 拼接成对端集合remote_portName， type， remote_sys_name， remote_ip
        if not all([cisco_remote_ip_not_deal, cisco_remote_sys_type, cisco_remote_sys_name, cisco_remote_portName]):
            for val in self.data['port_info_list'].values():
                # 初始化remote_list
                val['remoteList'] = []

        else:
            for key, val in cisco_remote_sys_name.items():
                # 2.0 初始化对端设备列表
                self.data['port_info_list'][str(key)]['remoteList'] = []
                remote_list = self.data['port_info_list'][key]['remoteList']
                # 2.1 判断protname是否有这个key
                if cisco_remote_portName.has_key(key):
                    data = {"remotePortName": cisco_remote_portName[key]}
                    remote_list.append(data)

                # 2.2 判断type是否有这个key
                if cisco_remote_sys_type.has_key(key):
                    data = {"type": str(cisco_remote_sys_type[key])}
                    remote_list.append(data)

                # 2.2 判断remote_ip是否有这个key
                if cisco_remote_ip_not_deal.has_key(key):
                    data = {"remotePortName": cisco_remote_ip_not_deal[key]}
                    remote_list.append(data)

                # 自己remote_sys_name 加入数据
                data = {"remoteSysName": val}
                remote_list.append(data)

        # 删除处理完的数据
        del self.data['cisco_remote_ip_not_deal']
        del self.data['cisco_remote_sys_type']
        del self.data['cisco_remote_sys_name']
        del self.data['cisco_remote_portName']

    def run(self, data):
        self.data = data
        self._deal_indof()
        # self._dael_remote_list()
        return self.data
