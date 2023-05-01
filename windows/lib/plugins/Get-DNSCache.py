import importlib
import re
import subprocess

class DNSCache:

    def __init__(self):
        self.current_lang = __import__('locale').getdefaultlocale()[0][:2]
        if importlib.util.find_spec("GetDnsClientCache") is not None:
            # PowerShell command Get-DnsClientCache exists, so use it to get DNS cache entries
            self.output = subprocess.run(['powershell', 'Get-DnsClientCache'], capture_output=True, text=True)
            self.lines = self.output.stdout.splitlines()
        else:
            # PowerShell command Get-DnsClientCache does not exist, so use ipconfig to get DNS cache entries
            output = subprocess.run(['ipconfig', '/displaydns'], capture_output=True, text=True)
            self.lines = output.stdout.splitlines()[3:]

    def convert_encoding(self, from_enc, to_enc, string):
        # Convert encoding of the string from one encoding to another
        enc_from = __import__('codecs').lookup(from_enc)
        enc_to = __import__('codecs').lookup(to_enc)
        return enc_to.encode(string.encode(enc_from))[0].decode(enc_to)

    def parse_line(self, line):
        if not line.strip():
            return None
        if '----------------------------------------' in line:
            return None
        if any(s in line for s in ['Record Name', '记录名称']):
            name = line.split(':')[1].strip()
        elif any(s in line for s in ['Record Type', '记录类型']):
            record_type = line.split(':')[1].strip()
        elif any(s in line for s in ['Time To Live', '生存时间']):
            time_to_live = line.split(':')[1].strip()
        elif any(s in line for s in ['Data Length', '数据长度']):
            data_length = line.split(':')[1].strip()
        elif any(s in line for s in ['Section', '部分']):
            section = line.split(':')[1].strip()
        else:
            # Try to match type and data with a regular expression
            match = re.match(r'(?P<Type>[A-Za-z()\s]+)\s.*Record[\s|\.]+:\s(?P<Data>.*$)', line)
            if not match:
                return None
            data = match.group('Data')
            type_ = match.group('Type')
            if self.current_lang == 'ru':
                type_, data = re.match(r'(?P<Type>[^\s]+\s+\([^\)]+\))[\s\.]+:\s(?P<Data>.*$)', line).groups()
        return {
            'TimeToLive': time_to_live,
            'Caption': '',
            'Description': '',
            'ElementName': '',
            'InstanceId': '',
            'Data': data,
            'DataLength': data_length,
            'Entry': '',
            'Name': name,
            'Section': section,
            'Status': '',
            'Type': type_
        }

    def get_cache(self):
        cache = []
        for line in self.lines:
            parsed_line = self.parse_line(line)
            if parsed_line:
                cache.append(parsed_line)
        return cache
