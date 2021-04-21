"""
@Author  :  熊盛春

@License :  (C) Copyright 2021-2023, 熊盛春

@Contact :  xiongshengchun@foxmail.com

@Software:  RFIShow

@File    :  settings.py

@Time    :  2021.4.16

@Desc    : 读取配置文件

"""


import sys
from configparser import ConfigParser


def _get_settings(setting_name):
    """
    读取cfg配置文件
    :param setting_name: section名称
    :return: args参数
    """

    cf = ConfigParser()
    cf.read(sys.path[0]+"/conf/rfishow.cfg", encoding="utf-8")
    if setting_name == "rfishow_page":
        args = {
            "fits_path": cf.get("rfishow_page", "fits_path"),
            "mask_mode": cf.get("rfishow_page", "mask_mode"),
            "mask_kwargs": cf.get("rfishow_page", "mask_kwargs"),
            "block_num": cf.getint("rfishow_page", "block_num"),
            "show_mask": cf.getboolean("rfishow_page", "show_mask"),
            "show_other": cf.getboolean("rfishow_page", "show_other"),
        }
    return args

def save_sttings(args, save_dict_list):
    """
    保存环境参数

    :param args: 全局的环境参数
    :param save_dict_list: 保存字典列表
    :return: None
    """
    cf = ConfigParser()
    for list_name in save_dict_list:
        cf.add_section(list_name)
        for key in args[list_name].keys():
            cf.set(list_name, key, str(args[list_name][key]))
    cf.write(open(sys.path[0]+args["conf_path"], "w", encoding="utf-8"))

"""
整个系统需要的一些参数文件
"""
args = {
    "version": "v0.2",
    "author": "熊盛春",
    "project_path": sys.path[0],
    "conf_path": "/conf/rfishow.cfg",
    "FAST_path": "/data/FAST_data/",
    "temp_data": "/data/temp_data/",
    "save_dict_list": ["rfishow_page"],
    "rfishow_page": _get_settings("rfishow_page"),
}

