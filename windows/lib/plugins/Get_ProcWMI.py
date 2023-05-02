import hashlib
import os
import wmi

class Get_ProcWMI:
    hashtypes = {
        "MD5": hashlib.md5,
        "SHA1": hashlib.sha1,
        "SHA256": hashlib.sha256,
        "SHA384": hashlib.sha384,
        "SHA512": hashlib.sha512,
        "RIPEMD160": hashlib.new("ripemd160"),
    }

    def __init__(self, hash_type="MD5"):
        self.hash_type = hash_type

    def compute_file_hash(self, file_path):
        if os.path.exists(file_path):
            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()
                    hash_obj = self.hashtypes[self.hash_type.upper()]()
                    hash_obj.update(file_data)
                    return hash_obj.hexdigest()
            except Exception as e:
                print(f"Error reading file: {file_path}. Exception: {str(e)}")
                return f"Invalid input file or path specified. {file_path}"
        else:
            return f"{file_path} is invalid or locked."

    def get_process_properties(self):
        c = wmi.WMI()
        for item in c.Win32_Process():
            if item.ExecutablePath:
                file_hash = self.compute_file_hash(item.ExecutablePath)
            else:
                file_hash = "Get-WmiObject query returned no executable path."

            try:
                domain, username, sid = item.GetOwner()
            except:
                domain = username = sid = "Unobtainable"

            username = f"{domain}\\{username}"

            item_properties = {
                "Process": item,
                "Hash": file_hash,
                "CommandLine": (item.CommandLine or "").replace("\n", " ").strip(),
                "Username": username,
                "SID": sid,
            }

            yield item_properties
