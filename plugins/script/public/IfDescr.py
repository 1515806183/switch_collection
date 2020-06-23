# -*- coding: utf-8 -*-
import re


# 网络接口信息描述,oid=.1.3.6.1.2.1.2.2.1.2
# IF-MIB::ifDescr.1 = STRING: FortyGigE1/0/0/1
def get_IfDescr(data):
    IfDescrList = re.findall(r'IF-MIB::ifDescr.(.*)', data)

    # #### 最大端口号 ####
    # index_max_len = 0
    # for i in IfDescrList:
    #     idx = i.split()[0]
    #     len_portIndex = len(idx)
    #     if len_portIndex > index_max_len:
    #         index_max_len = len_portIndex

    # [ (1, valn), [2, valn2]]
    result_list = []
    for descr in IfDescrList:
        res_list = descr.split(' ')
        result_list.append((res_list[0], res_list[-1]))

    return {"ifDescr": result_list}



