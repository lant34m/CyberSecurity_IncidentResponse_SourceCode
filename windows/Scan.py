# coding:utf-8
import os
import platform
from lib.core.option import *
import subprocess
from lib.plugins.Get_Arp import *
from lib.plugins.Get_DNSCache import *
from lib.plugins.Get_Handle import *
from lib.plugins.Get_Netstat import *
from lib.plugins.Get_PrefetchListing import *
from lib.plugins.Get_PrefetchFiles import *
from lib.plugins.Get_Prox import *
from lib.plugins.Get_SmbSession import *

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


    #ARP 表
    arp_table = Get_Arp()
    table = arp_table.get_table()
    for row in table:
        print(row)

    #DNS Ccache缓存条目
    dns_cache = Get_DNSCache()
    cache_entries = dns_cache.get_cache()
    for entry in cache_entries:
        print(entry)

    #Netstat获取系统网络信息
    netstat = Get_Netstat()
    netstat.run()
    netstat.print_results()

    #读取Windows系统中的预存数据
    # 创建 PrefetchInfo 对象，指定注册表键路径和值名称
    prefetch_info = Get_PrefetchListing('HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters', 'EnablePrefetcher')
    # 打印 Prefetch 文件的信息
    prefetch_info.print_prefetch_files()

    #获取Windows进程的句柄信息
    handle_data = Get_Handle()
    results = handle_data.get_handle_data()
    for result in results:
        print(result)

    #获取Windows操作系统中的预取文件（Prefetch Files），并将它们打包为一个Zip文件
    pf = Get_PrefetchFiles()
    result = pf.get_prefetch_files()

    #获取当前系统中所有进程的数据
    pd = Get_Prox()
    output = pd.get_process_data()
    print(output)

    #获取当前系统所有smb信息
    smb = Get_SmbSession()
    output = smb.get_smb_session()
    print(output)











