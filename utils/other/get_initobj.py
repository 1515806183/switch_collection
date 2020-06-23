# -*- coding: utf-8 -*-
# 动态加载实例化对象
import importlib


def initobj(path, class_name):
    """
    :param path: 文件路径 path.finlename
    :param class_name: 类名称
    :return: 实列化对象
    """
    # 导入
    model = importlib.import_module(path)
    # 初始化实列
    return getattr(model, class_name)()


# initobj(path='plugins.DealDataPlugins', class_name='Datapublic_oid')
