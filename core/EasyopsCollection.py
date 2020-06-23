# -*- coding: utf-8 -*-
# Easyops搜索实例
import requests, json
import setting
from setting import ConfigParams, ConfigSWITCHMODEL
from utils.cmdb_inser_data import http_post


class EasyopsPubic(object):

    def search_auto_collect_switch(self):
        """
        公共OID自动搜集，存放在OID.PY文件中
        :return:
        """
        return self.instance_search(ConfigSWITCHMODEL, ConfigParams)

    # 搜索实例
    def instance_search(self, object_id, params):
        """
        :param object_id: 配置文件中的搜索模型ID
        :param params: 配置文件中的搜索查询条件
        :return:
        """
        if params.has_key('page_size'):
            page_size = 500
        else:
            page_size = 1000
        params['page_size'] = page_size
        params['page'] = 1
        search_result = http_post(method='post',
                                  restful_api='/object/{object_id}/instance/_search'.format(object_id=object_id),
                                  params=params)

        if not search_result:
            raise Exception('CMDB中没有数据')
        total_instance_nums = int(search_result['total'])

        if total_instance_nums > page_size:
            pages = total_instance_nums / page_size  # total pages = pages + 1
            for cur_page in range(2, pages + 1):
                params['page'] = cur_page

                tmp_result = http_post(
                    restful_api='/object/{object_id}/instance/_search'.format(object_id=object_id), params=params,
                    method='post')
                search_result['list'] += tmp_result['list']

        return search_result['list']


# 搜索实例
def search_datas():
    obj = EasyopsPubic()
    examplelist = obj.search_auto_collect_switch()  # 搜索到所有的实例列表

    # examplelist = [{
    #     'name': '192.166.255.16',
    #     'instanceId': '5a50be0cc4d23',
    #     'ip': '192.166.255.16',
    #     'community': 'sxtsoft',
    #     '_object_id': '_SWITCH',
    #     'sys_name': 'GBZX-SW-ACCESS-C2960X-006'
    # }, {
    #     'name': '192.166.255.15',
    #     'instanceId': '5a8a596c1831d',
    #     'ip': '192.166.255.15',
    #     'community': 'sxtsoft',
    #     '_object_id': '_SWITCH',
    #     'sys_name': 'GBZX-SW-ACCESS-C2960X-005'
    # }]

    # examplelist = [{
    #     'name': '192.168.10.253',
    #     'instanceId': '5a50be0cc4911',
    #     'ip': '192.168.10.253',
    #     'community': 'public',
    #     '_object_id': '_SWITCH',
    #     'sys_name': 'GBZX-SW-ACCESS-C2960X-005'
    # }
    # ]

    # examplelist = [
    #     {
    #     'name': '192.166.255.16',
    #     'instanceId': '5a50be0cc4d23',
    #     'ip': '192.166.255.16',
    #     'community': 'sxtsoft',
    #     '_object_id': '_SWITCH',
    #     'sys_name': 'GBZX-SW-ACCESS-C2960X-006'
    # }
    # ]

    if len(examplelist) == 0:
        exit('没有可用的实例')

    aliveexamplelist = []
    # 排除实例列表里没有ip或者团体字的设备
    for example in examplelist:
        # 判断实例的ip和团体字都存在
        if example.has_key(setting.ip) and example.has_key(setting.community):
            aliveexamplelist.append(example)

    if len(aliveexamplelist) == 0:
        exit('所有实例都没配置好IP和团体字')

    return aliveexamplelist
