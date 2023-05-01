import subprocess
import datetime

# Define registry key path and value name
key_path = 'HKLM:\system\currentcontrolset\control\session manager\memory management\prefetchparameters'
value_name = 'EnablePrefetcher'

# Get value of EnablePrefetcher from registry
cmd = f'reg query "{key_path}" /v "{value_name}"'
output = subprocess.check_output(cmd, shell=True)
prefetch_value = int(output.split()[-1].decode())

if prefetch_value in [1, 2, 3]:
    # List prefetch files and get their properties
    cmd = 'ls $env:windir\Prefetch\*.pf | select FullName, CreationTimeUtc, LastAccessTimeUtc, LastWriteTimeUtc'
    output = subprocess.check_output(['powershell.exe', '-Command', cmd])
    for line in output.decode().split('\n')[3:-1]:
        file_props = line.split()
        file_path = file_props[0]
        creation_time = datetime.datetime.strptime(file_props[1], '%Y-%m-%dT%H:%M:%S.%fZ')
        last_access_time = datetime.datetime.strptime(file_props[2], '%Y-%m-%dT%H:%M:%S.%fZ')
        last_write_time = datetime.datetime.strptime(file_props[3], '%Y-%m-%dT%H:%M:%S.%fZ')

        # Output file properties in TSV format
        print(f'{file_path}\t{creation_time}\t{last_access_time}\t{last_write_time}')
else:
    print(f'Prefetch not enabled on {os.environ["COMPUTERNAME"]}.')
