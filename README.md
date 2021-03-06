# RFIShow
- **项目介绍**: RFIShow软件致力于打造为一个对FAST数据进行聚类可视化分析的软件，为用户提供FAST数据分析、RFI检测分析、RFI连通块聚类分析等功能。具体如下：
  1. 可视化FAST数据，并且支持局部区域数据的放大显示；
  2. 对FAST数据进行RFI检测、调参与分析；
  3.  提取RFI连通块特征数据；
  4. 对RFI连通块数据集进行批量分析：降维、聚类、分类器剔除等；
  5. 支持导出中间测试结果数据；
  6. 提供API接口供高级用户使用；
  7. ...
- **项目负责人**: *熊盛春*
---

## 一、功能介绍


### 1.1 RFI检测分析

> **功能**：读取FAST文件中的数据进行可视化，并提供一个交互式的界面便于用户实现对RFI的检测参数调节以及RFI特征提取的参数调节。
>
> **RFI特征包括**：
>
> ```basic
> x：		起始位置,时间点
> y：		起始位置，频率
> bandwidth：	带宽
> duration：	持续时间
> data_mean：	强度均值
> data_var：	强度方差
> ```

- [x] **参数设置**：FAST文件、RFI检测算法、RFI特征提取的参数设置
  - [x] **FAST文件设置**：选中文件、数据块编号、极化通道。
  - [x] **RFI检测算法的选择**：提供各种RFI mask检测算法供用户选择使用，支持在线交互参数的调节。
    - [x] [arpls_mask](http://zmtt.bao.ac.cn/GPPS/RFI/)
    - [x] [st_mask](https://github.com/cosmo-ethz/seek)
    - [x] template_mask：用户自定义RFI检测，需要按照一个的格式存放于指定位置。(参考`/core/mitigation/TemplateMask`存放于`/core/mitigation`路径下)
  - [x] **显示参数设置**：
    - [x] 是否显示条状mask
    - [x] 是否显示点状mask
    - [x] 视野尺寸
  - [x] 特征检测算法设置：
    - [x] 连通计算算法设置：4连通、8连通。
- [x] **保存当前检测结果**：含图片数据、RFI mask矩阵数据、RFI特征数据。
- [x] **RFI检测**：按选定的参数对数据进行RFI检测。
  - [x] 显示RFI检测结果。
  - [x] 动态显示局部数据图像。
- [x] RFI特征提取：
  - [x] 显示RFI特征提取的表格结果。
  - [x] 动态显示选定特征局部数据图像。
  - [x] 排序表格。
- [x] 其他
  - [x] 批量进行RFI检测。
  - [x] 批量进行RFI特征提取。

### 1.2 RFI聚类分析

> **功能**：采用了析取的方法对提取的RFI特征进行聚类分析，并可视化聚类的结果。

- [x] **参数设置**：
  - [x] 选择RFI特征数据的文件。
  - [x] 是否剔除单点状RFI样本。
  - [x] RFI特征采用t-SNE降维的的参数调节。
  - [x] 提供各种RFI特征的聚类的方法选择，及在线参数调节。
    - [x] KMeans
    - [x] AgglomerativeClustering
    - [x] GaussianMixture
    - [x] DBSCAN
    - [x] 用户自定义
  - [ ] 聚类个数K值的确定。
- [x] **显示聚类结果与局部RFI可视化**：
  - [x] 实现点击聚类样本点实时显示局部RFI数据。
  - [x] 实现显示局部RFI数据的视野调节。
  - [x] 显示统计数据分析。
  - [ ] 查询记录(记录用户点击查询的数据，便于用户的对比)。
  - [ ] 导出查询记录。
  - [x] 导出选中聚类区域样本数据。
- [x] 其他
  - [x] 能够保存退出前数据降维的结果，避免重复运算。

### 1.3 其他

> **功能**：软件的一些其他功能

- [x] 保存用户退出程序前的指定的参数信息(可以避免每次打开软件重复性的参数设置)。
- [ ] ...

## 二、依赖包

```bash
scipy==1.5.3
numpy==1.19.4
pandas==1.1.4
astropy==2.0.16
scikit-learn==0.23.2
scikit-image=0.17.2
matplotlib==3.3.2
pyqt5==5.15.2
```

## 三、启动使用
```bash
$ python main.py
```

## 四、文件架构介绍
- [bin](/bin)：存放脱离界面的一些可单独执行的功能包。
- [conf](/conf)：存放环境和用户相关的配置文件。
- [core](/core)：存放核心功能代码。
    - [mitigation](/core/mitigation)：各种RFI检测算法包。
    - [rfi_features.py](/core/rfi_features.py): RFI特征相关的核心代码。
    - [rfi_cluster.py](/core/rfi_cluster.py)：RFI特征聚类相关的核心代码。
    - [utils.py](/core/utils.py)：其他一些有效的代码。
- [data]()：存放相关检测数据、临时文件和日志文件。
    - [FAST_data]()：存放fast数据(未上传)。
    - [log]()：存放日志文件。
    - [temp_data]()：存放中间临时文件。
- [resource]()：存放UI界面相关资源文件(未上传)。
- [test](/test)：存放模块测试代码。
- [ui](/ui)：存放界面相关代码。
- [main.py](/main.py): 软件启动函数

## 五、版本记录
- **~2021.4.14---v0.0**：
  1. 初步完成RFI特征提取、RFI特征聚类的相关代码。
  2. 搭建UI界面整体架构。
  3. 搭建RFI聚类可视化界面。
  4. 实现点击聚类样本点实时显示局部RFI数据。
  5. 实现显示局部RFI数据的视野调节。
- **~2021.4.21---v0.1**:
  1. 抽象重构RFI特征提取、RFI特征聚类相关核心代码。
  2. 主界面添加了一个gif动画。
  3. 搭建RFI检测界面以及参数设置子界面。
  4. 实现交互式的RFI检测算法选择和参数设置。
  5. 实现当前检测结果的保存(保存检测可视化图片与RFI mask矩阵)。
  6. 添加环境和用户配置相关文件，并可保存用户上传退出时的参数设置。
- **~2021.4.28---v0.2:**
  1. 将RFI特征提取功能合并到RFI检测与分析中。
  2. RFI检测分析中的参数设置界面加入极化通道、视野尺寸以及特征提取连通算法等的参数设置。
  3. RFI检测分析中加入动态显示局部RFI检测结果图像的功能。
  4. RFI检测分析中加入特征提取后部分表格数据的可视化，并具有动态显示所选定的局部数据图像。
  5. 优化RFI局部显示的代码，几乎不用等待。
- **~2021.5.11---v0.3:**
  1. 实现表格数据排序的功能。
  2. 重构RFI聚类分析界面，包括一个主显示，两个副显示，已经5个功能按键(参数设置、切换显示、特征降维、特征聚类、保存结果)。
  3. 加入了一个切换显示功能，能够切换显示聚类类别统计信息和RFI局部显示信息。
- **~2021.5.18---v0.4:**
  1. 增加了DBSCAN聚类方法。
  2. 加入了鼠标框选导出样本数据的功能。
  3. 加入了点击某一类别时隐藏其他类别的功能。

# 六、界面演示

## 6.1 主界面

![RFIShow/main_page.png at master · Chan-0312/RFIShow (github.com)](https://github.com/Chan-0312/RFIShow/blob/master/resource/image/main_page.png)

## 6.2 RFI检测分析界面

![RFIShow/detect_page_1.png at master · Chan-0312/RFIShow (github.com)](https://github.com/Chan-0312/RFIShow/blob/master/resource/image/detect_page.png)

## 6.3 RFI聚类分析界面

![RFIShow/cluster_page_1.png at master · Chan-0312/RFIShow (github.com)](https://github.com/Chan-0312/RFIShow/blob/master/resource/image/cluster_page.png)
