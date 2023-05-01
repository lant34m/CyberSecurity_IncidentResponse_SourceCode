import hashlib
import os
import re
import win32com.client
import pythoncom
import datetime, pywintypes

def compute_file_hash(file_path, hash_type="MD5"):
    hash_algo = None
    if hash_type == "MD5":
        hash_algo = hashlib.md5()
    elif hash_type == "SHA1":
        hash_algo = hashlib.sha1()
    elif hash_type == "SHA256":
        hash_algo = hashlib.sha256()
    elif hash_type == "SHA384":
        hash_algo = hashlib.sha384()
    elif hash_type == "SHA512":
        hash_algo = hashlib.sha512()
    elif hash_type == "RIPEMD160":
        hash_algo = hashlib.new("ripemd160")
    else:
        return "Invalid hash type selected."

    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                hash_algo.update(data)
        return hash_algo.hexdigest()
    else:
        print(f"{file_path} is invalid or locked.")
        raise ValueError(f"Invalid input file or path specified. {file_path}")

try:
    pythoncom.CoInitialize()
    wmi_service = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    ccm_namespace = wmi_service.ConnectServer(".", "root\\CCM\\SoftwareMeteringAgent")
    recent_apps = ccm_namespace.ExecQuery("Select * from CCM_RecentlyUsedApps")
except pywintypes.com_error as e:
    if "WMI Namespace root\\CCM\\SoftwareMeteringAgent does not exist." in str(e):
        raise ValueError("WMI Namespace root\\CCM\\SoftwareMeteringAgent does not exist.")
    else:
        raise e

# Set up the time format template.
time_format = "%Y%m%d%H%M%S.%f%z"

for recent_app in recent_apps:
    if recent_app.FolderPath:
        binary_path = os.path.join(recent_app.FolderPath, recent_app.ExplorerFileName)
        sha1_hash = compute_file_hash(binary_path, hash_type="SHA1")
        md5_hash = compute_file_hash(binary_path, hash_type="MD5")
    else:
        sha1_hash = "Get-WmiObject query returned no executable path."
        md5_hash = "Get-WmiObject query returned no executable path."

    # Fix the timezone marker to match a parsable format and reformat the
    # timestamp to comply with ISO 8601.
    last_used_time = recent_app.LastUsedTime.replace(
        re.search(r"\+(\d)(\d{2})$", recent_app.LastUsedTime).group(),
        lambda m: f"+{m.group(1)}:{m.group(2)}",
    )

    try:
        iso_last_used_time = (
            datetime.datetime.strptime(last_used_time, time_format)
            .astimezone(datetime.timezone.utc)
            .isoformat()
        )
    except ValueError:
        iso_last_used_time = "Unable to parse time string"

    recent_app.IsoLastUsedTime = iso_last_used_time
    recent_app.Sha1Hash = sha1_hash
    recent_app.Md5Hash = md5_hash

    print(recent_app) # output each result as a dictionary-like object
