import xml.etree.ElementTree as ET
import datetime
import collections
import argparse
import logging
import subprocess

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='Get log event data from Windows Event Logs.')
parser.add_argument('LogName', nargs='+', help='The name of the event log to acquire data from.')
parser.add_argument('--DaysAgo', type=int, help='How many days back to gather logs. If not specified, all logs will be gathered.')
parser.add_argument('--EventIDs', nargs='+', help='The event IDs to filter on, separated by spaces.')

args = parser.parse_args()

def Convert_EventLogRecord(LogRecord):
    results = []
    for record in LogRecord:
        logging.info(f"Processing event id {record.Id} from {record.LogName} log on {record.MachineName}")
        logging.info("Creating XML data")
        r = ET.fromstring(record.ToXml())

        h = collections.OrderedDict()
        h["LogName"] = record.LogName
        h["RecordType"] = record.LevelDisplayName
        h["TimeCreated"] = record.TimeCreated
        h["ID"] = record.Id

        if len(r.findall("./EventData/Data")) > 0:
            logging.info("Parsing event data")
            for data in r.findall("./EventData/Data"):
                if data.attrib.get("Name"):
                    name = data.attrib["Name"]
                    value = data.text
                else:
                    logging.info("No data property name detected")
                    name = "RawProperties"
                    value = data.text.split("\n")

                if "RawProperties" in h:
                    logging.info("Appending to RawProperties")
                    h["RawProperties"] += value
                else:
                    logging.info(f"Adding {name}")
                    h[name] = value

        else:
            logging.info("No event data to process")

        h["Message"] = record.Message
        h["Keywords"] = record.KeywordsDisplayNames
        h["Source"] = record.ProviderName
        h["Computername"] = record.MachineName

        logging.info("Creating custom object")
        results.append(h)
    return results

print(args.DaysAgo)
print(args.EventIDs)
print(args.LogName)

logrecord = {}
if args.DaysAgo is None:
    command = f"Get-WinEvent -LogName {args.LogName} -Oldest -MaxEvents 5"
    oldest_record = subprocess.run(["powershell.exe", "-Command", command], capture_output=True, text=True)
    start_date = datetime.datetime.strptime(oldest_record.split()[-1].decode('utf-8'), "%m/%d/%Y %I:%M:%S %p")
    end_date = datetime.datetime.now()
    span = (end_date - start_date).days
else:
    span = args.DaysAgo

start_time = datetime.datetime.now() - datetime.timedelta(days=span)

if args.EventIDs is None:
    for log in args.LogName:
        command = f"Get-WinEvent -FilterHashtable @{{LogName='{args.LogName}';StartTime='{start_time}'}}"
        logrecord = subprocess.run(["powershell.exe", "-Command", command], capture_output=True, text=True)
        print(logrecord.stdout)
        Convert_EventLogRecord(logrecord)
else:
    for log in args.LogName:
        for id in args.EventIDs:
            command = f"Get-WinEvent -FilterHashtable @{{LogName='{args.LogName}';StartTime='{start_time}';ID='{id}'}}"
            logrecord = subprocess.run(["powershell.exe", "-Command", command], capture_output=True, text=True)
            print(logrecord)
            Convert_EventLogRecord(logrecord)
