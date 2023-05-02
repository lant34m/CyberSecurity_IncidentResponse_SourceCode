import os
import hashlib
import psutil
from collections import namedtuple
from datetime import datetime


class Get_ProcsNModules:
    def __init__(self):
        self.hash_table = {}

    def compute_file_hash(self, file_path, hash_type="MD5"):
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"{file_path} is invalid or locked.")

        try:
            with open(file_path, "rb") as file:
                file_data = file.read()
        except PermissionError:
            return "Permission denied"

        if hash_type.upper() == "MD5":
            hasher = hashlib.md5()
        elif hash_type.upper() == "SHA1":
            hasher = hashlib.sha1()
        elif hash_type.upper() == "SHA256":
            hasher = hashlib.sha256()
        elif hash_type.upper() == "SHA384":
            hasher = hashlib.sha384()
        elif hash_type.upper() == "SHA512":
            hasher = hashlib.sha512()
        else:
            raise ValueError("Invalid hash type selected.")

        hasher.update(file_data)
        return hasher.hexdigest()

    def run(self):
        Output = namedtuple("Output", ["Name", "ParentPath", "Hash", "ProcessName", "ProcPID", "CreateUTC", "LastAccessUTC", "LastWriteUTC"])
        for process in psutil.process_iter():
            try:
                main_module = process.exe()
                modules = [module.path for module in process.memory_maps()]
                curr_pid = process.pid

                for module in modules:
                    name = os.path.basename(module)
                    parent_path = os.path.dirname(module)

                    if module in self.hash_table:
                        file_hash = self.hash_table[module]
                    else:
                        file_hash = self.compute_file_hash(module)
                        self.hash_table[module] = file_hash

                    process_name = os.path.basename(main_module)

                    create_utc = datetime.fromtimestamp(os.path.getctime(module)).strftime('%Y-%m-%d %H:%M:%S')
                    last_access_utc = datetime.fromtimestamp(os.path.getatime(module)).strftime('%Y-%m-%d %H:%M:%S')
                    last_write_utc = datetime.fromtimestamp(os.path.getmtime(module)).strftime('%Y-%m-%d %H:%M:%S')

                    o = Output(name, parent_path, file_hash, process_name, curr_pid, create_utc, last_access_utc, last_write_utc)
                    print(o)

            except (psutil.AccessDenied, FileNotFoundError):
                pass
