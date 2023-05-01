import os
import re
import subprocess

class Get_Handle:
    def __init__(self):
        self.handle_path = os.path.join(os.environ["SystemRoot"], "handle.exe")
        self.results = []

    def _parse_data(self, data):
        for line in data:
            line = line.strip()
            if "pid:" in line:
                handle_id = handle_type = perms = name = None
                pattern = r"(?P<ProcessName>^[-a-zA-Z0-9_.]+) pid: (?P<PId>\d+) (?P<Owner>.+$)"

                if match := re.match(pattern, line):
                    process_name, proc_id, owner = match.group("ProcessName"), match.group("PId"), match.group("Owner")
            else:
                pattern = r"(?P<HandleId>^[a-f0-9]+): (?P<Type>\w+)"
                if match := re.match(pattern, line):
                    handle_id, handle_type = match.group("HandleId"), match.group("Type")
                    perms = name = None

                    if handle_type == "File":
                        pattern = r"(?P<HandleId>^[a-f0-9]+):\s+(?P<Type>\w+)\s+(?P<Perms>\([-RWD]+\))\s+(?P<Name>.*)"
                        if match := re.match(pattern, line):
                            perms, name = match.group("Perms"), match.group("Name")
                    else:
                        pattern = r"(?P<HandleId>^[a-f0-9]+):\s+(?P<Type>\w+)\s+(?P<Name>.*)"
                        if match := re.match(pattern, line):
                            name = match.group("Name")

                    if name is not None:
                        result = {
                            "ProcessName": process_name,
                            "ProcId": proc_id,
                            "HandleId": f"0x{handle_id}",
                            "Owner": owner,
                            "Type": handle_type,
                            "Perms": perms,
                            "Name": name,
                        }
                        self.results.append(result)

    def get_handle_data(self):
        if os.path.exists(self.handle_path):
            output = subprocess.run([self.handle_path, "/accepteula", "-a"], capture_output=True, text=True)
            data = output.stdout.splitlines()
            self._parse_data(data)
            return self.results
        else:
            raise FileNotFoundError(f"Handle.exe not found in {os.environ['SystemRoot']}.")

