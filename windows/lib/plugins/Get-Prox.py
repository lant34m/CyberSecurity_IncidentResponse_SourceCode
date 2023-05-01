import subprocess

# Update-TypeData to prevent deserialization issue
subprocess.run(["powershell", "Update-TypeData -TypeName System.Diagnostics.Process -SerializationDepth 3 -Force"])

# Get process data
output = subprocess.run(["powershell", "Get-Process"], capture_output=True, text=True)
print(output.stdout)
