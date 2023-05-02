# Returns Get-NetRoute data
# OUTPUT tsv
import subprocess

route_data = subprocess.check_output(['Get-NetRoute'])
print(route_data.decode('utf-8'))
