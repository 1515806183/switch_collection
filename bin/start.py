# -*- coding: utf-8 -*-
import os, sys


sys.path.insert(0, os.path.abspath('.'))
reload(sys)
global_real_path = os.path.dirname(os.path.realpath(__file__))
global_home = os.path.abspath(os.path.dirname(global_real_path))
sys.path.insert(0, global_real_path)
sys.path.insert(0, global_home)

from core.MultiprocessPool import CollectionProcess

if __name__ == '__main__':
    # 开始开启进程操作
    print "*********************** 开始采集数据，请耐心等待 ************************"
    CollectionProcess().run()

