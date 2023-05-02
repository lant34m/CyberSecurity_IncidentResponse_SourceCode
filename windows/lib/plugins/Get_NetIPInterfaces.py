import subprocess

class PowerShellCommand:
    def __init__(self, cmd):
        self.cmd = cmd

    def run(self):
        p = subprocess.Popen(["powershell", self.cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = p.communicate()
        return output.decode('utf-8')

class Get_NetIPInterfaces:
    def __init__(self):
        self.cmd = "Get-NetIPInterface | Format-Table -AutoSize"
        self.ps = PowerShellCommand(self.cmd)

    def run(self):
        return self.ps.run()
