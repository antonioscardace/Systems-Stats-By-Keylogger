from .features import ExtractFeatures
from .ccsv import Csv

class ClientThread:
    def __init__(self, victim):
        self.__conn = victim
        self.__run()

    def __receive(self):
        try:
            data = self.__conn.recv(10240)
            self.__conn.close()
            return data.decode('utf8')

        except Exception as e:
            print("Error in receiving:", e)
            self.__conn.close()
            return None
        
    def __console_print(self, log):
        print('\n')
        print(log, flush=True)
            
    def __csv_print(self, fts):
        output = Csv()
        output.write_metadata(fts.get_uuid(), fts.get_window(), fts.get_timestamp_begin(), fts.get_timestamp_end(), fts.get_ip_address())
        output.write_log(fts.get_uuid(), fts.get_log_text())
        del output

    def __processing(self, new_log):
        features = ExtractFeatures(new_log)
        self.__console_print(new_log)
        self.__csv_print(features)
        del features
    
    def __run(self):
        log = self.__receive()
        if log is not None: self.__processing(log)