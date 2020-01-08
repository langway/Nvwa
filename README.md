# Nvwa
Nvwa Brain is a AGI (Artificial General Intelligence. AI also include weak intelligence,such as deep leaning,etc.) based on understanding system that can truly realize machine thinking. The goal is to create a machine thinking like human beings that can "learn and think" and help people do things. An understandable world similar to human beings can further form the results of logical reasoning, association, emotion and even humor that other technologies can not achieve.

[中文版Readme](https://github.com/langway/Nvwa/blob/master/README(CN).md)

## First, why is it called Nvwa?
### Nvwa is the goddess of earth and human creation in Chinese mythology. The reason why human beings are human is that they have a wise brain. Naming the project "Nvwa" is the hope that the project will enable the machine to think like human beings.

## Second, Construction of operation environment:
### 1. Database:
#### (1) The database uses Postgre. After installation, the postgre user password is set to 123456qaz. You can also change the database user and password in \trunk\loongtian\nvwa\settings.py.
#### (2) Install the database, build three new databases, auth, Nvwa (currently nvwa2), yiya, and restore three databases under the database_backup directory in the current project.
### 2. python:
#### (1) Currently using version Python 3.7, the migration from Python 2.7 is completed（First Comit edition is python2.7）.
#### (2) Modify the log code in Python library, otherwise it will report an error! See below for specific modifications.
#### (3) Install the required libraries, open the loongtian/util/pip directory, run pipInstallAll.py, need pytz and other libraries in the early stage, check after installation, generally no successful installation does not affect the operation.

## Third,Running Basic Code
### 1. Start Nvwa brain: run/debug loongtian/nvwa/central Brain Runer.py
#### (1) The system will ask whether to delete the original data (as shown below). In the default debugging state, it is suggested to delete the data so as to test the correctness of the system association.

![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/start-nvwa-del-db.png)

#### (2) After the start-up is completed, the following should be done:
    
![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/start-nvwa-success.png)

### 2. Start the I/O console (client): Run/debug loongtian/nvwa/adminConsoleRunner.py

![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/start-console.png)

#### (1) Input user name and password will be required. The default user name of the system is Nvwa and password is 123. You can log in. The login interface is as follows:
    
![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/start-console-logon.png)
    
#### (2) Try to input simple sentences such as "cow" and "cow has legs". The results are as follows:

![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/console-dialog1.png)
    
![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/console-dialog2.png)

### 3. In the case of development, the test/nvwa/testBrain.py can be used directly to run the test Meaning function to view the running results line by line.

![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/console-dialog3.png)

## Fourth, Operation of Web Page Form

### 1. Start the Nvwa central brain first, see 3-1.

### 2. Start http server: run/debug loongtian/fuxi/http Server Runner.py. The interface after startup is as follows (login as a superuser at present):

![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/start-web-server.png)

### 3. After starting the server, use the browser to open the web address: http://127.0.0.1:1547/. The interface is as follows:

![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/start-web-index-page.png)

    Notice: By default, the interface displays the traditional search engine style, which can be changed by the left button, such as: default/fit/full screen
	
### 4. You can enter some simple sentences and click the "Send" button to view the results line by line.

![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/web-dialog0.png)

![Image text](https://raw.githubusercontent.com/langway/Nvwa/master/doc/img/web-dialog1.png)

## Fifth, Theory Based on Understanding (Basic Part)
### 1. On Metadata-Actual Objects
### 2. On Top Relations
### 3. About T-shaped Data Structure (T-shaped Data Structure)
### 4. The Hierarchical Structure of Meaning
### 5. About Action
#### (1) Simple action
#### (2) Conjugate action
#### (3) Context action
#### (4) Internal and External Relevant Action
Currently, you can read doc/"Relations between Objects.doc"


## Sixth. Why open source?
### 1. It has been a long time to do this project. From 2006, theoretical exploration has been started and has been going on till now.
### 2. At present, AI on the market is inclined to "perceptual computing". Image and sound are popular through deep learning technology. In terms of words, especially "cognitive computing" which can understand meaning like human beings, it is also very retarded, and deep learning can not solve the problem of artificial general intelligence.
### 3. Once set up a company, but finally because of the broken capital chain of investors, failed to survive to the end, not my fault! My heart has been holding a fire, I hope that my technology through open source, can see the sun again, rather than buried in my personal computer hard disk.

## Seventh. Hope:
### 1. More people of insight can join in and explore the development direction of strong artificial intelligence together.
### 2. Achieve further breakthroughs in technology at an early date. The current version only belongs to the core version of the foundation. It only develops the semantics and simple actions. There are more technologies to be explored and perfected.
### 3. Develop a commercial version as soon as possible.

## Eighth, Other
### 1. Python library changes

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

## Ninth,Contact information: mobile phone/Wechat 15640193617

## Ten. Questions:
### 1. Python 3.0 is more slower than Python 2.0!

