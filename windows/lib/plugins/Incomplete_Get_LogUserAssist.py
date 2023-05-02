import winreg
import subprocess
import re

def rot13(value):
    """Returns a Rot13 string of the input value"""
    newvalue = ""
    for char in value:
        charnum = ord(char)
        if char.isalpha():
            if char.islower():
                if charnum > ord('m'):
                    charnum -= 13
                else:
                    charnum += 13
            else:
                if charnum > ord('M'):
                    charnum -= 13
                else:
                    charnum += 13
        newvalue += chr(charnum)
    return newvalue

def get_userassist(userpath):
    """Returns a list of dictionaries containing UserAssist information"""
    userassist = []
    try:
        with winreg.ConnectRegistry(None, winreg.HKEY_USERS) as hkey_users:
            with winreg.OpenKey(hkey_users, userpath + "\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist", 0, winreg.KEY_READ) as key:
                for i in range(winreg.QueryInfoKey(key)[1]):
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name, 0, winreg.KEY_READ) as subkey:
                        count = winreg.QueryValueEx(subkey, "Count")[0]
                        for j in range(count):
                            value_name = "n" + str(j)
                            try:
                                value_data = winreg.QueryValueEx(subkey, value_name)[0]
                                value_data_rot13 = rot13(value_data)
                                if not value_data_rot13.startswith("UEME_"):
                                    known_folder = resolve_knownfolder_guid(value_data_rot13)
                                    userassist.append({
                                        "Subkey": subkey_name,
                                        "Value": value_data_rot13,
                                        "KnownFolder": known_folder,
                                        "Count": count
                                    })
                            except OSError:
                                pass
    except OSError:
        pass
    return userassist

def resolve_knownfolder_guid(value):
    """Returns the known folder name if the input value is a known folder GUID"""
    known_folders = {
        "DE61D971-5EBC-4F02-A3A9-6C82895E5C04": "AddNewPrograms",
        "724EF170-A42D-4FEF-9F26-B60E846FBA4F": "AdminTools"
    }
    guid_pattern = re.compile(r"[A-Fa-f0-9]{8}(?:-[A-Fa-f0-9]{4}){3}-[A-Fa-f0-9]{12}")
    guid_match = guid_pattern.search(value)
    if guid_match:
        guid = guid_match.group()
        if guid in known_folders:
            value = value.replace(guid, known_folders[guid])
            value = value.replace("{", "")
            value = value.replace("}", "")
    return value

def get_user_profiles():
    """Returns a list of user profiles"""
    user_profiles = []
    try:
        with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey_local_machine:
            with winreg.OpenKey(hkey_local_machine, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList", 0, winreg.KEY_READ) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name, 0, winreg.KEY_READ) as subkey:
                            userpath = winreg.QueryValueEx(subkey, "ProfileImagePath")[0]
                            usersid = subkey_name
                            user_profiles.append({
                                "userpath": userpath,
                                "usersid": usersid
                            })
                    except OSError:
                        pass
    except OSError:
        pass
    finally:
        return user_profiles

def main():
    """Main function"""
    user_profiles = get_user_profiles()
    for user_profile in user_profiles:
        userpath = user_profile["userpath"]
        usersid = user_profile["usersid"]
        try:
            subprocess.check_call(["reg.exe", "load", "hku\KansaTempHive", userpath + "\ntuser.dat"])
            userassist = get_userassist(usersid)
            for ua in userassist:
                print("Subkey: {0}, Value: {1}, KnownFolder: {2}, Count: {3}".format(ua["Subkey"], ua["Value"], ua["KnownFolder"], ua["Count"]))
        except subprocess.CalledProcessError:
            pass
        finally:
            subprocess.call(["reg.exe", "unload", "hku\KansaTempHive"], stderr=subprocess.DEVNULL)
