import os
import winreg
import subprocess
import codecs
from datetime import datetime
from collections import namedtuple
import win32security

def sid_to_ntaccount(sid_string):
    sid = win32security.ConvertStringSidToSid(sid_string)
    try:
        account_name, _, _ = win32security.LookupAccountSid(None, sid)
        return account_name
    except win32security.error:
        return None
def rot13(s):
    return codecs.encode(s, 'rot_13')

def get_reg_key_last_write_time(hkey, sub_key):
    return datetime.fromtimestamp(winreg.QueryInfoKey(hkey)[2] // 10**7 - 11644473600)

def resolve_known_folder_guid(guid):
    # You may need to implement a function to resolve known folder GUIDs
    return guid

def get_user_assist(regpath, userpath, useracct):
    with winreg.OpenKey(winreg.HKEY_USERS, regpath) as key:
        if winreg.QueryInfoKey(key)[0] > 0:
            for index in range(winreg.QueryInfoKey(key)[0]):
                sub_key_name = winreg.EnumKey(key, index)
                if sub_key_name == "UserAssist":
                    with winreg.OpenKey(key, sub_key_name) as user_assist_key:
                        for user_assist_index in range(winreg.QueryInfoKey(user_assist_key)[0]):
                            sub_key = winreg.EnumKey(user_assist_key, user_assist_index)
                            o = namedtuple('UserAssist', ['UserAcct', 'UserPath', 'Subkey', 'KeyLastWriteTime', 'Value', 'KnownFolder', 'Count'])
                            o.UserAcct = useracct
                            o.UserPath = userpath
                            o.KeyLastWriteTime = get_reg_key_last_write_time(user_assist_key, sub_key)
                            subkey = sub_key + "\\Count"
                            o.Subkey = "SOFTWARE" + subkey.split("SOFTWARE")[1]

                            with winreg.OpenKey(user_assist_key, subkey) as count_key:
                                for count_index in range(winreg.QueryInfoKey(count_key)[1]):
                                    value_name, value_data, _ = winreg.EnumValue(count_key, count_index)
                                    byte_array = bytearray(value_data[4:8])
                                    byte_array.reverse()
                                    o.Count = int.from_bytes(byte_array, 'little')
                                    o.Value = rot13(value_name)
                                    if o.Value.startswith("UEME_"):
                                        continue
                                    else:
                                        o.KnownFolder = resolve_known_folder_guid(o.Value)
                                        print(o)

# You may need to set the userpath and usersid variables before using them
userpath = "path\\to\\ntuser.dat"
usersid = "SID"

if os.path.exists(userpath):
    # Get the account name
    # You may need to implement a function to translate SID to NTAccount
    useracct = sid_to_ntaccount(usersid)

    regexe = subprocess.run(['reg.exe', 'load', 'hku\\KansaTempHive', f'{userpath}\\ntuser.dat'], capture_output=True, text=True)
    if "ERROR" not in regexe.stdout:
        get_user_assist("KansaTempHive\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer", userpath, useracct)
    else:
        uapath = f"{usersid}\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer"
        get_user_assist(uapath, userpath, useracct)
