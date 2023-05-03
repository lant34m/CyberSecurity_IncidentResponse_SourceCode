import win32evtlog
import datetime
import time
import argparse

class Get_LogWinEvent:
    def __init__(self, logname):
        self.logname = logname

    def get_event_records(self, start_time=None):
        event_records = []
        hand = win32evtlog.OpenEventLog(None, self.logname)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total = win32evtlog.GetNumberOfEventLogRecords(hand)

        while True:
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            if not events:
                break

            for event in events:
                if start_time and event.TimeGenerated < start_time:
                    break
                event_records.append(event)

        win32evtlog.CloseEventLog(hand)
        return event_records

    def get_event_records_by_id(self, event_id, start_time=None):
        event_records = []
        hand = win32evtlog.OpenEventLog(None, self.logname)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total = win32evtlog.GetNumberOfEventLogRecords(hand)

        while True:
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            if not events:
                break

            for event in events:
                if start_time and event.TimeGenerated < start_time:
                    break
                if event.EventID == event_id:
                    event_records.append(event)

        win32evtlog.CloseEventLog(hand)
        return event_records

    def convert_event_log_record(self, event_record):
        event_time = datetime.datetime.fromtimestamp(time.mktime(event_record.TimeGenerated.timetuple()))
        event_time_str = event_time.strftime('%Y-%m-%d %H:%M:%S')
        event_source = event_record.SourceName
        event_id = event_record.EventID
        event_category = event_record.EventCategory
        event_type = event_record.EventType
        event_message = event_record.StringInserts
        return f'{event_time_str} {event_source} {event_id} {event_category} {event_type} {event_message}'

    def query_event_log(self, daysago=None, eventid=None):
        if daysago:
            start_time = datetime.datetime.now() - datetime.timedelta(days=daysago)
        else:
            start_time = None

        if eventid:
            event_records = self.get_event_records_by_id(eventid, start_time)
        else:
            event_records = self.get_event_records(start_time)

        for event_record in event_records:
            print(self.convert_event_log_record(event_record))
