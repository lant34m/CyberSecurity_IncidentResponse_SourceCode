import os
import subprocess
import gzip
import base64
from datetime import datetime

def get_proc_dump(proc_id=None):
    if not proc_id:
        proc_id = os.getpid()
    date_str = datetime.now().strftime("%Y%m%d%H%M%S")
    outfile = f"{os.getcwd()}\\{os.environ['COMPUTERNAME']}_PId_{proc_id}_{date_str}.dmp"
    obj = {"Path": outfile, "PId": proc_id, "ProcessName": os.path.abspath(f"\\proc({proc_id})")}
    try:
        procdump_path = os.path.join(os.environ["SystemRoot"], "Procdump.exe")
        if not os.path.isfile(procdump_path):
            raise Exception("Procdump.exe not found")
        # Dump specified process memory to file on disk named $outfile
        subprocess.run([procdump_path, "/accepteula", str(proc_id), outfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        with open(outfile, "rb") as f:
            file_data = f.read()
            # Compress the file data using GZip
            gz_data = gzip.compress(file_data)
            # Base64 encode the compressed data and store it in our object
            obj["Base64EncodedGzippedBytes"] = base64.b64encode(gz_data).decode("utf-8")
    except Exception as e:
        print(f"Error dumping process memory: {str(e)}")
    finally:
        if os.path.isfile(outfile):
            os.remove(outfile)
    return obj
