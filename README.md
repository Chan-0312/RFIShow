# RFIShow
---
- 项目介绍: RFIShow主要致力于给天文科研人员提供一个可视化的交互界面，简化对FAST天文观测数据进行RFI检测、RFI特征提取以及聚类分析等。
- 项目作者: 熊盛春
---


## 依赖包
```
scipy==1.5.3
numpy==1.19.4
pandas==1.1.4
astropy==2.0.16
scikit-learn==0.23.2
scikit-image=0.17.2
matplotlib==3.3.2
pyqt5==5.15.2
```

## 启动使用
```
$ python main.py
```

## 功能介绍
- [x] RFI检测：读取FAST文件中的数据进行
    - df
- [ ] RFI特征提取
- [x] RFI聚类分析
- [ ] 其他

## 文件架构介绍

- 文件管理说明：
    - core:存放核心功能代码，将各个功能的代码抽离处理
    - ui:存放界面代码
    - test:存放模块测试代码
    - data:
        - FAST_data:存放FAST数据(不需要上传,我们仅取编号前5)
        - temp_data:临时中间数据
        - ...
- 版本记录:
    -[ ] v0.1: 初步实现
- 备注:
    - log日志
    - 报表输出