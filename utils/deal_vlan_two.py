# -*- coding: utf-8 -*-
from multiprocessing.dummy import Pool as ThreadPool
import subprocess

# 单独多线程采集任务
import setting
from core.EasyopsCollection import EasyopsPubic
from utils.other.get_initobj import initobj


class deal_vlan(object):
    def __init__(self, datas):
        self.datas = datas

        # 汇报数据，初始化端口信息
        self.easyopsobj = EasyopsPubic()

    # 入口
    def run(self):
        self.snmp_run()
        self.async_pool.close()

    # 拼接执行命令
    def snmp_run(self):
        self.async_pool = ThreadPool(10 if len(self.datas) > 10 else len(self.datas))  # 线程池

        # 执行线程
        results = []
        for data_info in self.datas:
            result = self.async_pool.apply_async(self.deal_snmp, args=(data_info,))
            results.append(result)

        # 执行线程
        for i in results:
            i.wait()  # 等待线程函数执行完毕
            
        return self.datas

    # 执行命令
    def deal_snmp(self, data_info):
        mac_port_table = {}
        try:
            if type(data_info) == list:
                data_info = data_info[0]
            else:
                data_info = data_info

            # 1. 根据不同vlan采集信息相关信息是valn_info 和mac_port_result
            valn_info = data_info.get('vlan', '')
            if valn_info:
                # 2. 初始化信息
                ip_info = data_info.get('ip_info')  # 获取到ip信息
                other_name = setting.plugins_oid.keys()[-1]  # 获取到oid dict
                other_dict = setting.plugins_oid[setting.plugins_oid.keys()[-1]]  # 获取到oid的key
                other_obj = initobj(path='plugins.DealDataPlugins', class_name=other_name)  # 初始化处理数据的类

                # 采集other_id信息
                for vlan in valn_info:
                    community_vlan = ip_info['community'] + '@' + vlan
                    ip = ip_info['ip']

                    vlan_datas = {}
                    for key, val in other_dict.items():
                        cmd = "snmpwalk -v 2c -c {0} {1} {2}".format(community_vlan, ip, val)
                        data = subprocess.check_output(cmd, shell=True).decode()
                        res = getattr(other_obj, key)(data)
                        vlan_datas.update(res)
                    result = getattr(other_obj, 'mergedata')(vlan_datas)
                    if result:
                        mac_port_table.update(result)

                # 处理完成，删除多余的数据
                del data_info['vlan']

        except Exception as e:
            print '处理deal_vlan 函数:' + str(e)

        finally:
            data_info['mac_port_table'] = mac_port_table
