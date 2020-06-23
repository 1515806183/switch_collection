# -*- coding: utf-8 -*-
# 发送requests请求
import requests, json
from setting import headers, easyops_cmdb_host


# 请求cmdb，汇报数据
def http_post(method, restful_api, params=None):
    url = u'http://{easy_host}{restful_api}'.format(easy_host=easyops_cmdb_host, restful_api=restful_api)
    if method in ('post', 'POST'):
        try:
            r = requests.post(url, headers=headers, data=json.dumps(params))
            if r.status_code == 200:
                return json.loads(r.content)['data']
        except Exception as e:
            return {"list": []}

    if method in ('put', "PUT"):
        try:

            r = requests.put(url=url, headers=headers, json=params)
            if r.status_code == 200:
                return json.loads(r.content)['data']
        except Exception as e:
            return {"list": []}

    if method in ("info_port",):
        # 这里是交换机端口关联，因为关联成功返回的信息{u'message': u'', u'code': 0, u'data': None, u'error': u''}， 如果像上面那么写 data返回的是None
        try:
            r = requests.post(url, headers=headers, data=json.dumps(params))
            if r.status_code == 200:
                data = json.loads(r.content)
                if data.get('code') == 0:
                    return True
                else:
                    return False
        except Exception as e:
            return False

