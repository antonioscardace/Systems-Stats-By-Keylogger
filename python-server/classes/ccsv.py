import csv

class Csv:
    def __init__(self):
        pass

    def __write(self, path, row):
        with open(path, 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def write_metadata(self, uuid, window, ts_begin, ts_end, ip_address):
        self.__write('/usr/app/server/csv/metadata.csv', [uuid, window, ts_begin, ts_end, ip_address])

    def write_log(self, uuid, log):
        self.__write('/usr/app/server/csv/logs.csv', [uuid, log])