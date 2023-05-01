import subprocess
import re

class Get_Arp:

    def __init__(self):
        if subprocess.run(["powershell","Get-NetNeighbor"], capture_output=True).returncode == 0:
            # PowerShell command Get-NetNeighbor exists, so use it to get ARP table
            self.output = subprocess.run(["powershell", "Get-NetNeighbor"], capture_output=True, text=True)
            self.lines = self.output.stdout.splitlines()
            self.lines = self.lines[3:]
            self.lines = self.lines[:-2]
        else:
            # PowerShell command Get-NetNeighbor does not exist, so use arp to get ARP table
            self.ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
            arp_output = subprocess.run(["arp", "-a"], capture_output=True, text=True)
            self.lines = arp_output.stdout.splitlines()
        self.interface = None

    def parse_line(self, line):
        line = line.strip()
        if not line:
            return None
        if match := re.match(rf"Interface: ({self.ip_pattern}).*", line):
            self.interface = match.group(1)
        elif match := re.match(rf"({self.ip_pattern})\s+([0-9A-Fa-f]{{2}}-[0-9A-Fa-f]{{2}}-[0-9A-Fa-f]{{2}}-[0-9A-Fa-f]{{2}}-[0-9A-Fa-f]{{2}}-[0-9A-Fa-f]{{2}})*\s+(dynamic|static)", line):
            ip_addr, mac, arp_type = match.groups()
            mac = mac if mac else ""
            return {
                "Interface": self.interface,
                "IpAddr": ip_addr,
                "Mac": mac,
                "Type": arp_type
            }

    def get_table(self):
        table = []
        for line in self.lines:
            parsed_line = self.parse_line(line)
            if parsed_line:
                table.append(parsed_line)
        return table
