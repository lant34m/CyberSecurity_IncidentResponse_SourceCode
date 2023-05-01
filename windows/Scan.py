# coding:utf-8
import os
import platform
from lib.core.option import *
import subprocess

# 功能：本程序旨在为安全应急响应人员对Linux主机排查时提供便利，实现主机侧安全Checklist的自动化，用于快速主机安全点排查。


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    # 导入platform库判断平台，分平台导入库
    main(path)
    # 接触ps1文件锁定
    subprocess.run(['powershell', 'ls', '-r', '*.ps1', '|', 'Unblock-File'])
    # 设置执行策略
    subprocess.run(['powershell', 'Set-ExecutionPolicy', 'AllSigned'])
    # 执行脚本
    subprocess.run(['powershell', '.\kansa.ps1', '-Target', '$env:COMPUTERNAME', '-ModulePath', '.\Modules', '-Verbose'])




