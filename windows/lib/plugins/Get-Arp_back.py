import subprocess
import re

if subprocess.run(["powershell","Get-NetNeighbor"], capture_output=True).returncode == 0:
    # PowerShell command Get-NetNeighbor exists, so use it to get ARP table
    output = subprocess.run(["powershell", "Get-NetNeighbor"], capture_output=True, text=True)
    lines = output.stdout.splitlines()
    lines = lines[3:]
    lines = lines[:-2]
    for line in lines:
        fields = line.strip().split(" ")
        print({
            "Interface": fields[2],
            "IpAddr": fields[0],
            "Mac": fields[3],
            "Type": fields[4]
        })
else:
    # PowerShell command Get-NetNeighbor does not exist, so use arp to get ARP table
    ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    arp_output = subprocess.run(["arp", "-a"], capture_output=True, text=True)
    lines = arp_output.stdout.splitlines()
    interface = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if match := re.match(rf"Interface: ({ip_pattern}).*", line):
            interface = match.group(1)
        elif match := re.match(rf"({ip_pattern})\s+([0-9A-Fa-f]{{2}}-[0-9A-Fa-f]{{2}}-[0-9A-Fa-f]{{2}}-[0-9A-Fa-f]{{2}}-[0-9A-Fa-f]{{2}}-[0-9A-Fa-f]{{2}})*\s+(dynamic|static)", line):
            ip_addr, mac, arp_type = match.groups()
            mac = mac if mac else ""
            print({
                "Interface": interface,
                "IpAddr": ip_addr,
                "Mac": mac,
                "Type": arp_type
            })
