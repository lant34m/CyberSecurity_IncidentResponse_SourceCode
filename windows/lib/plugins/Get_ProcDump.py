import os
import subprocess
import gzip
import base64
from datetime import datetime

class Get_ProcDump:
    def __init__(self, proc_id=None):
        if not proc_id:
            proc_id = os.getpid()
        self.proc_id = proc_id
        self.date_str = datetime.now().strftime("%Y%m%d%H%M%S")
        self.outfile = f"{os.getcwd()}\\{os.environ['COMPUTERNAME']}_PId_{self.proc_id}_{self.date_str}.dmp"
        self.obj = {"Path": self.outfile, "PId": self.proc_id, "ProcessName": os.path.abspath(f"\\proc({self.proc_id})")}

    def dump(self):
        try:
            procdump_path = os.path.join(os.environ["SystemRoot"], "Procdump.exe")
            if not os.path.isfile(procdump_path):
                raise Exception("Procdump.exe not found")
            # Dump specified process memory to file on disk named $outfile
            subprocess.run([procdump_path, "/accepteula", str(self.proc_id), self.outfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            with open(self.outfile, "rb") as f:
                file_data = f.read()
                # Compress the file data using GZip
                gz_data = gzip.compress(file_data)
                # Base64 encode the compressed data and store it in our object
                self.obj["Base64EncodedGzippedBytes"] = base64.b64encode(gz_data).decode("utf-8")
        except Exception as e:
            print(f"Error dumping process memory: {str(e)}")
        finally:
            if os.path.isfile(self.outfile):
                os.remove(self.outfile)
        return self.obj
