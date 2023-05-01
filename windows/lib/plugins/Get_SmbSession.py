import subprocess

class Get_SmbSession:
    def __init__(self):
        pass

    def get_smb_session(self):
        # Check if Get-SmbSession command exists
        if subprocess.run(["powershell", "Get-Command Get-SmbSession"], capture_output=True).returncode == 0:
            # Get-SmbSession command exists, so use it to get smb sessions
            output = subprocess.run(["powershell", "Get-SmbSession"], capture_output=True, text=True)
            if output.stdout:
                return output.stdout
            else:
                return "No SMB session data exists on the current system."
        else:
            return "Get-SmbSession command is not available on this system."
