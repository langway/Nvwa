# Nvwa
Nvwa Brain，女娲大脑，是世界上第一款基于理解体系建立起来的可真正实现机器思维的“强”人工智能（GAI，General Artificial Intelligence）！ 目标是打造一款像人一样“学习、思维”，帮人做事的机器思维！一个类似于人的可理解的世界，可以进一步形成其他技术实现不了的逻辑推理，联想，情感，甚至幽默等思维结果！ 

## 一、运行环境搭建：
### 1、数据库：
####  （1）数据库使用Postgre，安装完成后，postgre用户密码设置为123456qaz，你也可以在\trunk\loongtian\nvwa\settings.py中更改数据库用户及密码。
####  （2）安装数据库，在目前项目中的
### 2、python：
####  （1）目前使用版本python2.7，正在完成向python3.7的迁移
####  （2）修改python库中的log代码，否则会报错！具体修改方案见下面。
####  （3）安装需要的库，打开loongtian/util/pip目录，运行pipInstallAll.py，前期需要pytz等库，安装完成后检查，一般未安装成功不影响运行。

## 二、运行基本代码

## 三、基于理解的理论（基础部分）

## 四、其他
###  1、python库更改
\Lib\logging\__init__.py\LogRecord.getMessage最后一句话：
原语句：
if self.args:
    msg = msg % self.args
修改为：
if self.args:
    try:
        msg = msg % self.args
    except:
        pass
        
\Lib\logging\handlers
class RotatingFileHandler(BaseRotatingHandler):
    def doRollover(self):
        def doRollover(self):
            原语句：
            # Issue 18940: A file may not have been created if delay is True.
            if os.path.exists(self.baseFilename):
                os.rename(self.baseFilename, dfn)
            
            
            更改为：
            # Issue 18940: A file may not have been created if delay is True.
            if os.path.exists(self.baseFilename):
                try:
                    os.rename(self.baseFilename, dfn)
                except:
                    pass


