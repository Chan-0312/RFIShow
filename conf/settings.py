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

project_path = "F:/xscPycharm/RFIShow"

def _get_settings(setting_name):
    """
    读取cfg配置文件
    :param setting_name: section名称
    :return: args参数
    """

    cf = ConfigParser()
    cf.read(project_path+"/conf/rfishow.cfg", encoding="utf-8")
    if setting_name == "rfi_detect_page":
        args = {
            "fits_path": cf.get(setting_name, "fits_path"),
            "mask_mode": cf.get(setting_name, "mask_mode"),
            "mask_kwargs": cf.get(setting_name, "mask_kwargs"),
            "block_num": cf.getint(setting_name, "block_num"),
            "npol_num": cf.getint(setting_name, "npol_num"),
            "show_mask": cf.getint(setting_name, "show_mask"),
            "edge_size": cf.getint(setting_name, "edge_size"),
            "connectivity": cf.getint(setting_name, "connectivity"),
        }
    elif setting_name == "rfi_cluster_page":
        args = {
            "csv_path": cf.get(setting_name, "csv_path"),
            "cut_path": cf.get(setting_name, "cut_path"),
            "sample_num": cf.getint(setting_name, "sample_num"),
            "tsne_perplexity": cf.getint(setting_name, "tsne_perplexity"),
            "cluster_mode": cf.getint(setting_name, "cluster_mode"),
            "n_clusters": cf.getint(setting_name, "n_clusters"),
            "cluster_kwargs": cf.get(setting_name, "cluster_kwargs"),
            "edge_size": cf.getint(setting_name, "edge_size"),
            "show_mask": cf.getboolean(setting_name, "show_mask")
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
    cf.write(open(project_path+args["conf_path"], "w", encoding="utf-8"))

"""
整个系统需要的一些参数文件
"""
args = {
    "version": "v0.3",
    "author": "熊盛春",
    "project_path": project_path,
    "conf_path": "/conf/rfishow.cfg",
    "FAST_path": "/data/FAST_data/",
    "temp_data": "/data/temp_data/",
    "save_dict_list": ["rfi_detect_page", "rfi_cluster_page"],
    "rfi_detect_page": _get_settings("rfi_detect_page"),
    "rfi_cluster_page": _get_settings("rfi_cluster_page"),
}

