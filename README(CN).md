# Nvwa
女娲大脑，是基于理解体系建立起来的可真正实现机器思维的“强”人工智能（GAI，General Artificial Intelligence）！ 目标是打造一款像人一样“学习、思维”，帮人做事的机器思维！一个类似于人的可理解的世界，可以进一步形成其他技术实现不了的逻辑推理，联想，情感，甚至幽默等思维结果！  
Nuwa Brain is a GAI (General Artificial Intelligence) based on understanding system that can truly realize machine thinking. The goal is to create a machine thinking like human beings that can "learn and think" and help people do things. An understandable world similar to human beings can further form the results of logical reasoning, association, emotion and even humor that other technologies can not achieve.

## 一、为什么叫女娲？
### 女娲，是中国神话中抟土造人的女神。而人类之所以为人，就是因为人类具有智慧的大脑。给项目名称起名“女娲”，就是希望项目能让机器实现像人类一样的思考。

## 二、运行环境搭建：
### 1、数据库：
####  （1）数据库使用Postgre，安装完成后，postgre用户密码设置为123456qaz，你也可以在\trunk\loongtian\nvwa\settings.py中更改数据库用户及密码。
####  （2）安装数据库，新建auth、nvwa（目前为nvwa2）、yiya三个数据库，在目前项目中的\database_backup目录下，恢复三个数据库。
### 2、python：
####  （1）目前使用版本python2.7，正在完成向python3.7的迁移
####  （2）修改python库中的log代码，否则会报错！具体修改方案见下面。
####  （3）安装需要的库，打开loongtian/util/pip目录，运行pipInstallAll.py，前期需要pytz等库，安装完成后检查，一般未安装成功不影响运行。

## 三、运行基本代码
### 1、启动nvwa中央大脑：运行/调试 loongtian/nvwa/centralBrainRuner.py
#### （1）系统会询问是否删除原有数据（如下图），默认调试状态下，建议删除，以便测试系统关联的正确性；

![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/start-nvwa-del-db.png)
    
#### （2）启动完成后，应如下图：
   
![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/start-nvwa-success.png)

### 2、启动输入输出控制台（客户端）：运行/调试 loongtian/nvwa/adminConsoleRunner.py

![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/start-console.png)

#### （1）会要求输入用户名和密码，系统默认用户名：nvwa，密码：123，即可登录，登录后界面如下图：
  
![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/start-console-logon.png)
    
#### （2）试着输入“牛”、“牛有腿”等简单句子，结果如下：
    
![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/console-dialog1.png)
    
![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/console-dialog2.png)

### 3、开发情况下，直接使用test/nvwa/testBrain.py，运行testMeaning函数，即可逐行查看运行结果

![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/console-dialog3.png)


## 四、网页形式运行

### 1、首先启动启动nvwa中央大脑，见三-1

### 2、启动http server：运行/调试 loongtian/fuxi/httpServerRunner.py，启动后界面如下图（目前以超级用户的身份登录）：

![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/start-web-server.png)

### 3、启动服务器端后，使用浏览器打开网址：http://127.0.0.1:1547/，界面如下图：

![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/start-web-index-page.png)

    说明：默认情况下，界面显示的是传统的搜索引擎样式，可以通过左侧按钮更改板式，例如：默认\适合\全屏

### 4、可以输入一些简单句子，然后点击”发送“按钮，即可逐行查看运行结果。

![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/web-dialog0.png)

![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/web-dialog1.png)


## 五、基于理解的理论（基础部分）
### 1、关于元数据-实际对象
### 2、关于顶级关系
### 3、关于丁字形数据结构（T型数据结构）
### 4、关于意义的分层结构
### 5、关于动作
#### （1）简单动作
#### （2）共轭动作
#### （3）上下文动作
#### （4）内外关联动作

目前，可阅读doc/《对象之间的关系.doc》

## 六、其他
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

## 七、联系方式：手机/微信 15640193617

## 八、问题：

### 1、不知为什么，python3.0的速度比python2.0的速度要慢！

