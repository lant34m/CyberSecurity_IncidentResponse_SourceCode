import subprocess
import datetime
import os

# Define registry key path and value name
key_path = 'HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters'
value_name = 'EnablePrefetcher'

# Get value of EnablePrefetcher from registry
cmd = f'reg query "{key_path}" /v "{value_name}"'
print(cmd)

output = subprocess.check_output(cmd, shell=True)
print(output)
prefetch_value = int(output.split()[-1].decode(), 16)  # 转换为十进制
print(prefetch_value)

if prefetch_value in [1, 2, 3]:
    # List prefetch files and get their properties
    cmd = 'powershell.exe -Command "Get-ChildItem $env:windir\Prefetch\*.pf | Select-Object FullName, CreationTimeUtc, LastAccessTimeUtc, LastWriteTimeUtc | Format-Table -HideTableHeaders | Out-String -Width 4096"'
    output = subprocess.check_output(cmd, shell=True)
    for line in output.decode().split('\n'):
        file_props = line.split()
        if len(file_props) == 7:
            file_path = file_props[0]
            creation_time = file_props[1] + ' ' + file_props[2]
            creation_time = datetime.datetime.strptime(creation_time, '%Y/%m/%d %H:%M:%S')
            last_access_time = file_props[3] + ' '  + file_props[4]
            last_access_time = datetime.datetime.strptime(last_access_time, '%Y/%m/%d %H:%M:%S')
            last_write_time = file_props[5] + ' '  + file_props[6]
            last_write_time = datetime.datetime.strptime(last_write_time, '%Y/%m/%d %H:%M:%S')
            print(f'{file_path}\t{creation_time}\t{last_access_time}\t{last_write_time}')
else:
    print(f'Prefetch not enabled on {os.environ["COMPUTERNAME"]}.')
