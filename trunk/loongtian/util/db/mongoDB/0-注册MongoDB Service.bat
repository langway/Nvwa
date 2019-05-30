::表示在此语句后所有运行的命令都不显示命令行本身
@echo off

::以管理员身份运行bat
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

if '%errorlevel%' NEQ '0' (

  goto UACPrompt

) else ( goto gotAdmin )

:UACPrompt

echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"

echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"

"%temp%\getadmin.vbs"

exit /B

:gotAdmin

if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )

pushd "%CD%"

CD /D "%~dp0"



rem 真正的批处理部分
echo 正在注册MongoDB服务...

rem 删除MongoDB.log，否则如果MongoDB.log存在，将会创建另外一个MongoDB.log
if exist "D:\Program Files\MongoDB\Data\log\MongoDB.log" ( del "D:\Program Files\MongoDB\Data\log\MongoDB.log")

::进入d盘
D:
cd \Program Files\MongoDB\Server\3.4\bin
mongod -dbpath "D:\Program Files\MongoDB\Data\db" -logpath "D:\Program Files\MongoDB\Data\log\MongoDB.log" -install -serviceName "MongoDB"


echo 注册成功


::显示log文件
cd D:\Program Files\MongoDB\Data\log

start MongoDB.log

pause

@echo on