# -*- coding: utf-8 -*-
"""
多进程开启任务
"""
import os
from multiprocessing import Pool
import setting
from core.EasyopsCollection import search_datas
from utils.clear_data.cleanData import cleanPublicData, cleanCiscoData
from MultithreadingPool import CollectionThread

# t = threading.currentThread()
from utils.pool_insert_data import insertData
from utils.deal_vlan_two import deal_vlan

bashpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


# 多进程，获取实例数据，并传递到多线程，回调后插入数据到cmdb
class CollectionProcess(object):
    """
    多进程开启任务
    """

    def __init__(self):
        self.datalist = search_datas()  # 获取cmdb所有实例数据
        self.datas = []  # 每台机器采集完，待合并汇报的数据，为了以后开多线程准备

    def __call__(self, *args, **kwargs):
        # 多线程必须这么写， apply_async里面调用的self， 在到这里调用该执行的函数
        """
        :param args: (0, 1)  0 是数据 ，1 是public_oid或者cisco_oid
        :param kwargs:
        :return:
        """
        return self.func(args[0], args[1])

    def run(self):
        """
        默认执行 public_oid setting.plugins_oid.keys()[0]
        :return:
        """
        public_pool = Pool(10 if len(self.datalist) > 10 else len(self.datalist))  # 判断实例数据个数，最大开10个进程
        for data in self.datalist:
            public_pool.apply_async(self, args=(data, setting.plugins_oid.keys()[0]), callback=self.inser_callback)  # (data, ) 不这样写map会把数据遍历处理成每个key

        public_pool.close()
        public_pool.join()

        # 把超时的ip 从self.data里面剔除掉
        time_out_ip = []
        data = []
        for datainfo in self.datas:
            ip_list = datainfo.get('timeout_ip')
            if not ip_list:
                data.append(datainfo)
            else:
                time_out_ip += ip_list

        print '----------------------连接超时失败的IP：%s' % list(set(time_out_ip))

        # 重新赋值给self.datas
        self.datas = data
        print "*********************** 数据采集完成，保存在data目录下，下面开始整合公共OID数据 ************************"
        # 1. 根据vlan 线程执行二次处理mac_port_table
        deal_vlan(self.datas).run()  # == self.datas

        # 2. 公共oid采集的数据整合(前后print self.datas， 发现后面数据都整理好了，原因应该是多进程共享数据)，保险起见，我们还是将self.data重新赋值
        cleanPublicData(self.datas).run()  # == self.datas

        # 处理设备是思科的，只处理基本信息
        # self._deal_cisco()   # == self.datas

        # 4. 开启线程处理任务(汇报数据)
        insertData(self.datas).run()

    def inser_callback(self, res):
        """
        :param res: 采集的数据
        :return:
        """
        self.datas.append(res)

    def func(self, data, oid_name):
        """
        调用多线程处理函数
        :param data: 单独的实例信息
        :param oid_name: oid_name,配置文件中的
        :param datas: 思科单独处理需要的第一次采集的信息
        :return:
        """

        return CollectionThread(data, oid_name).run()

    def _deal_cisco(self):
        # 3. 根据brand属性判断是否是思科交换机，然后我们要采集思科设备信息，开启多线程
        cicso_data_info = []
        for data in self.datas:
            if data.get('brand') == 'Cisco':
                res = CollectionThread(data.get('ip_info'), setting.plugins_oid.keys()[1]).run()
                cicso_data_info.append(res)

        # 如果思科里面有数据，拼接数据,根据 instanceId 来判断, 这个先不管
        if cicso_data_info:
            for index, alldata in enumerate(self.datas):
                alldata_instanceId = alldata.get('instanceId')
                for cisco_data in cicso_data_info:
                    cisco_instanceId = cisco_data.get('instanceId')
                    if alldata_instanceId == cisco_instanceId:
                        # 拼接数据
                        res = dict(alldata, **cisco_data)
                        res_data = cleanCiscoData(res).run()  # 思科设备整合数据  只整合了基本数据
                        self.datas[index] = res_data[0]  # 把self.data 替换成合并的数据
