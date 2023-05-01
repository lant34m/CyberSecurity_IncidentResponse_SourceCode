import os
import re
import socket
import subprocess
from typing import List, Tuple

class Netstat:
    def __init__(self):
        self.results = []

    def get_addr_port(self, addr_port: str) -> List[str]:
        if re.match(r'[0-9a-f]*:[0-9a-f]*:[0-9a-f%]*\]:[0-9]+', addr_port):
            addr_port = addr_port.split(']:')
            addr_port[0] += ']'
        else:
            addr_port = addr_port.split(':')
        return addr_port

    def run(self):
        netstat_command = ['netstat', '-nao']

        output = subprocess.run(netstat_command, capture_output=True, text=True)
        lines = output.stdout.splitlines()

        for line in lines:
            line = line.strip()
            if line and not re.match(r'Active |Proto ', line):
                if line.startswith('TCP'):
                    protocol, local_address, foreign_address, state, pid = re.split(r'\s{2,}', line)
                elif line.startswith('UDP'):
                    state = 'STATELESS'
                    protocol, local_address, foreign_address, pid = re.split(r'\s{2,}', line)
                else:
                    continue

                local_addr_port = self.get_addr_port(local_address)
                local_address = local_addr_port[0]
                local_port = local_addr_port[1]

                foreign_addr_port = self.get_addr_port(foreign_address)
                foreign_address = foreign_addr_port[0]
                foreign_port = foreign_addr_port[1]

                self.results.append({
                    'protocol': protocol,
                    'local_address': local_address,
                    'local_port': local_port,
                    'foreign_address': foreign_address,
                    'foreign_port': foreign_port,
                    'state': state,
                    'pid': pid
                })

    def print_results(self):
        for result in self.results:
            print(f"{result['protocol']}\t{result['local_address']}\t{result['local_port']}\t{result['foreign_address']}\t{result['foreign_port']}\t{result['state']}\t{result['pid']}")

