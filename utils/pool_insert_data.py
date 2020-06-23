# -*- coding: utf-8 -*-
from multiprocessing.dummy import Pool as ThreadPool
import subprocess

# 单独多线程采集任务
import setting
from core.EasyopsCollection import EasyopsPubic
from utils.cmdb_inser_data import http_post
from setting import setting_model


class insertData(object):
    def __init__(self, datas):
        self.datas = datas

        # 汇报数据，初始化端口信息
        self.port_info_list = {}  # 每个端口的详情信息
        self.easyopsobj = EasyopsPubic()

    # 入口
    def run(self):
        self.snmp_run()
        self.async_pool.close()

    # 拼接执行命令
    def snmp_run(self):
        self.async_pool = ThreadPool(setting.pool_nums if len(self.datas) > setting.pool_nums else len(self.datas))  # 线程池

        # 执行线程
        results = []
        for data_info in self.datas:
            result = self.async_pool.apply_async(self.deal_snmp, args=(data_info,))
            results.append(result)

        # 执行线程
        for i in results:
            i.wait()  # 等待线程函数执行完毕

    # 执行命令
    def deal_snmp(self, data_info):
        try:
            if type(data_info) == list:
                data_info = data_info[0]
            else:
                data_info = data_info

            # 1.  根据ARP表去更新ipaddress模型数据
            params = {
                "name": "",
                "mac": "",
                "status": u"已分配"
            }

            dict_arp = data_info.get('ipNetToMediaPhysAddress')['dict_arp']

            search_obj = EasyopsPubic()
            for mac, ip in dict_arp.items():
                params['name'] = ip
                params['mac'] = mac

                search = {
                    "query": {
                        "name": {"$eq": ip}
                    },
                    "fields": {
                        "name": True,
                        "mac": True
                    }
                }

                res_list = search_obj.instance_search(object_id='IPADDRESS', params=search)
                if not res_list:
                    continue

                for res in res_list:
                    instance_id = res.get('instanceId')
                    old_mac = res.get('mac')
                    if mac != old_mac:
                        restful_api = '/object/%s/instance/%s' % ('IPADDRESS', instance_id)
                        http_post('put', restful_api, params)

            # 2. 汇报数据
            self._inser_data_to_cmdb(data_info)

        except Exception as e:
            print '处理聚合端口:' + str(e)

    # 信息汇报到cmdb
    def _inser_data_to_cmdb(self, data_info):
        try:
            # 基本信息入库
            data = {}
            info_url = "/object/{0}/instance/{1}".format(setting_model.get('model_id'), data_info.get('instanceId'))

            for param in setting_model.get('fields').keys():
                try:
                    res = data_info.get(param, '')
                    data.update({param: res})
                # 数据里面可能没有定义的这个属性，如果没则设置为空
                except Exception as e:
                    data.update({param: ''})

            res = http_post('put', info_url, data)

            if res:
                # 端口信息
                data = {
                    "keys": [setting_model.get('pk')],
                    "datas": data_info['port_info_list'].values()
                }

                port_url = '/object/%s/instance/_import' % setting_model.get('port_modol_id')
                port_res = http_post('post', port_url, data)

                if port_res:
                    # 路由和端口关联信息
                    data = {
                        "objectId": setting_model.get('model_id'),
                        "instance_ids": [data_info.get('instanceId')],
                        "related_instance_ids": self._get_port_instanceId(data_info)
                    }
                    info_to_port_url = '/object/{0}/relation/{1}/append'.format(setting_model.get('model_id'),setting_model.get('to_port_id'))
                    info_to_port_res = http_post('info_port', info_to_port_url, data)
                    if info_to_port_res:
                        print '%s 实例ID：%s 基本信息, 端口信息, 关联端口信息入库成功' % (str(data_info.get('ip')), str(data_info.get('instanceId')))
                    else:
                        print '%s 实例ID：%s 基本信息, 端口信息, 关联端口信息入库成功' % (str(data_info.get('ip')), str(data_info.get('instanceId')))

                else:
                    print '%s 实例ID：%s 端口信息入库失败' % (str(data_info.get('ip')), str(data_info.get('instanceId')))

            else:
                if data_info.get('ip', ''):
                    print '%s 实例ID：%s 基本信息入库失败' % (str(data_info.get('ip')), str(data_info.get('instanceId')))
                else:
                    print '%s 实例ID：%s 基本信息入库失败' % (str(data_info.get('ip_info')['ip']), str(data_info.get('instanceId')))

        except Exception as e:
            print '汇报数据出错:' + str(e)

    # 获取端口信息所有实例ID，关联端口关系的时候需要
    def _get_port_instanceId(self, data):
        name = []
        port_datas = data.get('port_info_list').values()
        for data in port_datas:
            name.append(data.get('name'))

        params = {
            "query": {
                "name": {"$in": name}
                # "name": {"$eq": str(name)}
            },
            "fields": {
                "instanceId": True
            }
        }
        res = self.easyopsobj.instance_search(setting_model.get('port_modol_id'), params)

        return [str(i.get('instanceId')).encode('utf-8') for i in res]
        # 通过easyops查询实例
