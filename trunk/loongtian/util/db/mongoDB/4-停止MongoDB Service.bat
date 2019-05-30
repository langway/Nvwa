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
echo 正在停止MongoDB服务...

net stop mongodb


echo 停止成功

pause

::显示log文件
cd D:\Program Files\MongoDB\Data\log

start MongoDB.log


@echo on