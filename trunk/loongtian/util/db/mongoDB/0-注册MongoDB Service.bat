::��ʾ�ڴ������������е��������ʾ�����б���
@echo off

::�Թ���Ա�������bat
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



rem ��������������
echo ����ע��MongoDB����...

rem ɾ��MongoDB.log���������MongoDB.log���ڣ����ᴴ������һ��MongoDB.log
if exist "D:\Program Files\MongoDB\Data\log\MongoDB.log" ( del "D:\Program Files\MongoDB\Data\log\MongoDB.log")

::����d��
D:
cd \Program Files\MongoDB\Server\3.4\bin
mongod -dbpath "D:\Program Files\MongoDB\Data\db" -logpath "D:\Program Files\MongoDB\Data\log\MongoDB.log" -install -serviceName "MongoDB"


echo ע��ɹ�


::��ʾlog�ļ�
cd D:\Program Files\MongoDB\Data\log

start MongoDB.log

pause

@echo on