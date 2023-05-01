import subprocess
import re

# Check if handle.exe exists in SystemRoot
if subprocess.run(["powershell", "Test-Path", "$env:SystemRoot\\handle.exe"], capture_output=True).returncode == 0:
    # handle.exe exists, so use it to get handle data
    data = subprocess.run(["powershell", "$env:SystemRoot\\handle.exe", "/accepteula", "-a"], capture_output=True, text=True)
    lines = data.stdout.strip().splitlines()
    processes = {}
    for line in lines:
        line = line.strip()
        if " pid: " in line:
            # line contains process info
            process_info = re.match(r"^(?P<ProcessName>[-a-zA-Z0-9_.]+) pid: (?P<PId>\d+) (?P<Owner>.+)$", line)
            if process_info:
                process_name = process_info.group("ProcessName")
                pid = process_info.group("PId")
                owner = process_info.group("Owner")
                processes[pid] = {"ProcessName": process_name, "Owner": owner}
        else:
            # line contains handle info
            handle_info = re.match(r"^(?P<HandleId>[a-f0-9]+): (?P<Type>\w+)", line)
            if handle_info:
                handle_id = "0x" + handle_info.group("HandleId")
                handle_type = handle_info.group("Type")
                perms = ""
                name = ""
                if handle_type == "File":
                    # handle is a file
                    file_info = re.match(r"^[a-f0-9]+:\s+\w+\s+\((?P<Perms>[-RWD]+)\)\s+(?P<Name>.*)$", line)
                    if file_info:
                        perms = file_info.group("Perms")
                        name = file_info.group("Name")
                else:
                    # handle is not a file
                    non_file_info = re.match(r"^[a-f0-9]+:\s+\w+\s+(?P<Name>.*)$", line)
                    if non_file_info:
                        name = non_file_info.group("Name")
                if name:
                    process = processes.get(pid, {})
                    o = {
                        "ProcessName": process.get("ProcessName", ""),
                        "ProcId": pid,
                        "HandleId": handle_id,
                        "Owner": process.get("Owner", ""),
                        "Type": handle_type,
                        "Perms": perms,
                        "Name": name
                    }
                    print(o)
else:
    print("Handle.exe not found in $env:SystemRoot.")
