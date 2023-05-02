import subprocess

# 执行 PowerShell 命令 Get-NetRoute，并使用 Format-Table 命令来格式化输出
p = subprocess.Popen(["powershell", "Get-NetIPInterface | Format-Table -AutoSize"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 获取命令输出并将其解码为字符串
output, error = p.communicate()
output_str = output.decode('GBK', 'ignore')
print(output_str)
