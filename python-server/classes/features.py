import json

class ExtractFeatures:
    def __init__(self, log):
        self.__log = json.loads(log)

    def get_uuid(self):
        return self.__log['uuid']
    
    def get_timestamp_begin(self):
        return self.__log['timestamp-start']

    def get_window(self):
        return self.__log['window-title']

    def get_log_text(self):
        return self.__log['log-text']

    def get_timestamp_end(self):
        return self.__log['timestamp-end']
    
    def get_ip_address(self):
        return self.__log['ip-address']