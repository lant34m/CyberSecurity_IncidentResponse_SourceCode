import os
import zipfile
import gzip
import base64
from datetime import datetime
import glob

def get_base64_gzipped_stream(file_path):
    with open(file_path, 'rb') as f_in:
        data = f_in.read()
    compressed = gzip.compress(data)
    return base64.b64encode(compressed).decode()

def add_to_zip(zip_file, file_path):
    zip_file.write(file_path, os.path.basename(file_path))

def get_prefetch_files():
    prefetch_enabled = int(os.popen('powershell "(Get-ItemProperty -Path Registry::\HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Memory Management\PrefetchParameters).EnablePrefetcher"').read().strip())
    if prefetch_enabled < 1 or prefetch_enabled > 3:
        return

    computer_name = os.environ['COMPUTERNAME']
    temp_dir = os.environ['TEMP']
    zip_file_path = os.path.join(temp_dir, f"{computer_name}-PrefetchFiles.zip")
    with zipfile.ZipFile(zip_file_path, mode='w') as zip_file:
        for file_path in glob.glob(os.path.join(os.environ['WINDIR'], 'Prefetch', '*.pf')):
            add_to_zip(zip_file, file_path)

    obj = {}
    zip_file_stats = os.stat(zip_file_path)
    obj['FullName'] = zip_file_path
    obj['Length'] = zip_file_stats.st_size
    obj['CreationTimeUtc'] = datetime.utcfromtimestamp(zip_file_stats.st_ctime).isoformat()
    obj['LastAccessTimeUtc'] = datetime.utcfromtimestamp(zip_file_stats.st_atime).isoformat()
    obj['LastWriteTimeUtc'] = datetime.utcfromtimestamp(zip_file_stats.st_mtime).isoformat()
    obj['Content'] = get_base64_gzipped_stream(zip_file_path)

    os.remove(zip_file_path)

    return obj
