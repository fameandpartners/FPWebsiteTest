# 生成虚拟环境requirements.txt
pip freeze > requirements.txt

# 安装虚拟环境内依赖包
pip install -r requirements.txt

# 运行提示 'module' object has no attribute 'verbose'  pycharm2017.3
1，pycharm  Tools - python scientific
or
2，pip uninstall matplotlib
   pip install matplotlib==2.1.2


# 项目介绍
项目顶级目录为 - THAutoTestFrameWork

 THAutoTestFrameWork
|
| --- apps
|      |
|      |--- MTM
|
|
|--- source