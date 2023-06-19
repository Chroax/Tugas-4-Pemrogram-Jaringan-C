import json
import logging
import shlex

from file_interface import FileInterface

"""
* class FileProtocol bertugas untuk memproses 
data yang masuk, dan menerjemahkannya apakah sesuai dengan
protokol/aturan yang dibuat

* data yang masuk dari client adalah dalam bentuk bytes yang 
pada akhirnya akan diproses dalam bentuk string

* class FileProtocol akan memproses data yang masuk dalam bentuk
string
"""


class FileProtocol:
    def __init__(self):
        self.file = FileInterface()
    def proses_request(self,data=''):
        logging.warning(f"string diproses: {data}")
        data_split = shlex.split(data.lower())
        try:
            request = data_split[0].strip()
            logging.warning(f"memproses request: {request}")
            params = [x for x in data_split[1:]]
            response = getattr(self.file,request)(params)
            return json.dumps(response)
        except Exception:
            return json.dumps(dict(status='ERROR',data='request tidak dikenali'))

        
if __name__=='__main__':
    #contoh pemakaian
    file_protocol = FileProtocol()
    print(file_protocol.proses_request("LIST"))
    print(file_protocol.proses_request("GET pokijan.jpg"))
