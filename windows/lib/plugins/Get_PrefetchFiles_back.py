import subprocess
import os
import zipfile
import base64
from datetime import datetime
import glob

PREFETCH_KEY_PATH = r'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters'
ENABLE_PREFETCHER_VALUE_NAME = 'EnablePrefetcher'
WINDIR = os.environ['WINDIR']
TEMP_DIR = os.environ['TEMP']

def get_base64_zip_stream(file_path):
    with open(file_path, 'rb') as f_in:
        return base64.b64encode(f_in.read()).decode()

def add_to_zip(zip_file, file_path):
    zip_file.write(file_path, os.path.basename(file_path))

def get_prefetch_files():
    result = subprocess.run(['powershell.exe', f'(Get-ItemProperty -Path "{PREFETCH_KEY_PATH}" -Name "{ENABLE_PREFETCHER_VALUE_NAME}")."{ENABLE_PREFETCHER_VALUE_NAME}"'],
                            stdout=subprocess.PIPE, check=True, text=True)
    prefetch_enabled = int(result.stdout.strip())
    if prefetch_enabled not in range(1, 4):
        return None

    computer_name = os.environ['COMPUTERNAME']
    zip_file_path = os.path.join(TEMP_DIR, f"{computer_name}-PrefetchFiles.zip")
    print("Prefetch files have been compressed into ZipFile", zip_file_path)
    with zipfile.ZipFile(zip_file_path, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in glob.glob(os.path.join(WINDIR, 'Prefetch', '*.pf')):
            add_to_zip(zip_file, file_path)

    zip_file_stats = os.stat(zip_file_path)
    return {
        'FullName': zip_file_path,
        'Length': zip_file_stats.st_size,
        'CreationTimeUtc': datetime.utcfromtimestamp(zip_file_stats.st_ctime).isoformat(),
        'LastAccessTimeUtc': datetime.utcfromtimestamp(zip_file_stats.st_atime).isoformat(),
        'LastWriteTimeUtc': datetime.utcfromtimestamp(zip_file_stats.st_mtime).isoformat(),
        'Content': get_base64_zip_stream(zip_file_path),
    }
