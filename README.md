CatPlot
========

[![Build Status](https://travis-ci.org/PytLab/catplot.svg?branch=master)](https://travis-ci.org/PytLab/catplot)
[![platform](https://img.shields.io/badge/python-2.7-green.svg)]()
[![versions](https://img.shields.io/badge/versions%20-%20%200.1.0-blue.svg)]()

**CatPlot** is a Python module for catalysis data plotting.

催化剂相关的python绘图库

###目前提供的功能

1. Plotting energy profile
2. ...

###依赖
- `python2.7.x`
- `Numpy`
- `scipy`
- `matplotlib`

###下载
下载链接：
[Download ZIP](https://github.com/PytLab/catplot/archive/master.zip)

或者通过git：

    $ git clone https://github.com/PytLab/catplot.git

###安装

使用[pip](https://pypi.python.org/pypi/pip#downloads)安装第三方依赖库：

    $ pip install -r requirement.txt
通过源码安装：

- [`python2.7.x`](https://www.python.org/downloads/release/python-2710/)
- [`Numpy`](https://github.com/numpy/numpy)
- [`scipy`](https://github.com/scipy/scipy)
- [`matplotlib`](https://github.com/matplotlib/matplotlib)


安装catplot：

    $ unzip python-catplot-x.x.x.zip

    $ cd python-catplot-x.x.x

    $ python setup.py install

###使用举例
#####执行脚本
catplot/scripts/ 中提供了两个绘制energy profile的脚本和输入文件模板
(使用者可以根据自己的需要单独写脚本，此目录的脚本仅作为参考和快速使用):

- scripts/plot (绘制单条energy profile)
  - `input.txt` -- 输入文件模板
  - `plot_energy_profile.py` -- 绘图脚本
- scripts/mplot (绘制合并的energy profile)
  - `input.txt` -- 输入文件模板
  - `plot_energy_profile.py` -- 绘图脚本

#####参数设置说明
以`catplot/scripts/plot/input.txt`为例:

若进行多个基元反应的energy profile的绘制则需要将`rxn_equations`和`energy_tuples`的注视取消。

**基元反应式**

    #elementary reaction equations
    rxn_equations = [
        'HCOOH_g + 2*_s <-> HCOO-H_s + *_s -> HCOO_s + H_s',
        'HCOO_s + *_s <-> H-COO_s + *_s -> COO_s + H_s',
        'COO_s -> CO2_g + *_s',
        '2H_s <-> H-H_s + *_s -> H2_g + 2*_s'
    ]

**相应每个态的能量**

    #relative energies
    energy_tuples = [
        # IS,  TS,  FS
        #--------------
        (0.0, 1.0, 0.5),
        (3.0, 4.7, 0.7),
        (0.0, 4.0),
        (3.0, 4.7, 0.7),
    ]

*能量和基元反应式的形状必须匹配，否则程序会把抛出异常。

其余的参数用于调节绘图的其他效果，例如是否显示标注，线的颜色，阴影颜色和深度等等，使用者可以根据自己需求进行调节。

###效果图展示：

一个基元反应：

![](https://github.com/PytLab/catplot/blob/master/examples/0.jpeg)

多个基元反应：

![](https://github.com/PytLab/catplot/blob/master/examples/multi_energy_diagram_04.jpeg)

两条路径合并：

![](https://github.com/PytLab/catplot/blob/master/examples/merged_energy_profile_1_trans.png)
