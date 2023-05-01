import subprocess

class Get_Prox:
    def __init__(self):
        # Update-TypeData to prevent deserialization issue
        subprocess.run(["powershell", "Update-TypeData -TypeName System.Diagnostics.Process -SerializationDepth 3 -Force"])

    def get_process_data(self):
        # Get process data
        output = subprocess.run(["powershell", "Get-Process"], capture_output=True, text=True)
        return output.stdout
