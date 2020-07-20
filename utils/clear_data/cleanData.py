# -*- coding: utf-8 -*-
from multiprocessing.dummy import Pool as ThreadPool
from utils.clear_data.clearPublicData import CleanPublicData
from utils.clear_data.clearCiscoData import CleanCiscoData
import setting

# class CleanData(object):
#     def __init__(self, data):
#         """
#         :param data: 采集回来的数据，格式为[{}]
#         """
#         self.data = data[0]
#         self.res = []
#
#     def run(self, name=None):
#         # 调用公共整合数据方法
#         if name == 'public':
#             res = CleanPublicData().run(self.data)
#         else:
#             res = CleanCiscoData().run(self.data)
#
#         return self.res.append(res)


# 多线程，合并每台机器数据
# 公共数据合并处理
class cleanPublicData(object):
    def __init__(self, datas):
        """
        :param datas: 根据public采集完的数据 [{}, {}]
        """

        self.public_datas = datas
        self.async_pool = ThreadPool(setting.pool_nums if len(self.public_datas) > setting.pool_nums else len(self.public_datas))  # 线程池
        self.res = []

    def run(self):
        # 加入线程池, 这里还是单线程处理，暂时不解决
        results = []
        for data in self.public_datas:
            result = self.async_pool.apply_async(self.cleandata, args=(data,))
            results.append(result)
        # 执行线程
        for i in results:
            i.wait()  # 等待线程函数执行完毕

        # 关闭线程
        self.async_pool.close()
        return self.res  # [{}]

    # 整合公共oid数据
    def cleandata(self, data):
        res = CleanPublicData(data).run()
        self.res.append(res)


# 思科数据合并处理
class cleanCiscoData(object):
    def __init__(self, datas):
        """
        :param datas: 根据public采集完的数据 [{}, {}]
        """
        self.cisco_datas = [datas]  # 这里有两个数据，一个为公共oid数据，一个为思科数据，所有这里要将数据合并下

        self.async_pool = ThreadPool(setting.pool_nums if len(self.cisco_datas) > setting.pool_nums else len(self.cisco_datas))  # 线程池
        self.res = []

    def run(self):
        # 加入线程池, 这里还是单线程处理，暂时不解决
        results = []
        for data in self.cisco_datas:
            result = self.async_pool.apply_async(self.cleandata, args=(data,))
            results.append(result)
        # 执行线程
        for i in results:
            i.wait()  # 等待线程函数执行完毕

        # 关闭线程
        self.async_pool.close()

        return self.res  # [{}]

    # 整合公共oid数据
    def cleandata(self, data):
        self.res.append(CleanCiscoData().run(data))
