# -*- coding: UTF-8 -*-

# author:p_ppcjchen
# create by:2022/3/13/1:19 下午

import os

# 获取当前目录
os.path.dirname(__file__)
# 获取当前目录的上一级
os.path.dirname(os.path.dirname(__file__))


# 获取指定目录
def file_dir(dir_path):
    """
    :param dir_path: 目录
    :return: 返回完整目录
    """
    base_path = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_path,dir_path)


def file_path(file_dir="data",file_name = "data.xls"):
    """
    :param file_dir: 目录
    :param file_name: 文件名称
    :return:
    """
    return os.path.join(os.path.dirname(os.path.dirname(__file__)),file_dir,file_name)

