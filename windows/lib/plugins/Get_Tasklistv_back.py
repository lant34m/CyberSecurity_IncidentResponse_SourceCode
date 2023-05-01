import subprocess

# Run tasklist command and format output as tsv
output = subprocess.run(["tasklist.exe", "/v", "/fo", "csv"], capture_output=True, text=True)
lines = output.stdout.strip().splitlines()[1:]
for line in lines:
    fields = line.strip().split(",")
    image_name = fields[0].strip('"')
    pid = fields[1]
    session_name = fields[2].strip('"')
    session_num = fields[3]
    mem_usage = fields[4].strip('"')
    status = fields[5].strip('"')
    user_name = fields[6].strip('"')
    cpu_time = fields[7].strip('"')
    window_title = fields[8].strip('"')
    print({
        "ImageName": image_name,
        "PID": pid,
        "SessionName": session_name,
        "SessionNum": session_num,
        "MemUsage": mem_usage,
        "Status": status,
        "UserName": user_name,
        "CPUTime": cpu_time,
        "WindowTitle": window_title
    })
