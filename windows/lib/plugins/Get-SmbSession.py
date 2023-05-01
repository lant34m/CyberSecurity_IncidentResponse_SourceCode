import subprocess

# Check if Get-SmbSession command exists
if subprocess.run(["powershell", "Get-Command Get-SmbSession"], capture_output=True).returncode == 0:
    # Get-SmbSession command exists, so use it to get smb sessions
    output = subprocess.run(["powershell", "Get-SmbSession"], capture_output=True, text=True)
    print(output.stdout)
