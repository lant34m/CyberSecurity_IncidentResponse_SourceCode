import subprocess
import datetime
import os

class Get_PrefetchListing:
    def __init__(self, key_path, value_name):
        self.key_path = key_path
        self.value_name = value_name

    def get_prefetch_value(self):
        cmd = f'reg query "{self.key_path}" /v "{self.value_name}"'
        output = subprocess.check_output(cmd, shell=True)
        prefetch_value = int(output.split()[-1].decode(), 16)
        return prefetch_value

    def print_prefetch_files(self):
        prefetch_value = self.get_prefetch_value()
        if prefetch_value in [1, 2, 3]:
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
