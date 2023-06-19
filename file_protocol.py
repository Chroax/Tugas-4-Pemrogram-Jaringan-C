import json
import logging

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
    def proses_string(self,string_datamasuk=''):
        logging.warning(f"string diproses: {string_datamasuk}")
        c = string_datamasuk.split(" ")
        try:
            c_command = c[0].strip()
            logging.warning(f"memproses request: {c_command}")
            if c_command=='list' or c_command=='LIST':
                return json.dumps(self.file.list())
            elif c_command=='get' or c_command=='GET':
                param1 = c[1].strip()
                return json.dumps(self.file.get(param1))
            elif c_command=='upload' or c_command=='UPLOAD':
                param1 = c[1].strip()
                param2 = c[2].strip()
                return json.dumps(self.file.post(param1, param2))
            elif c_command=='delete' or c_command=='DELETE':
                param1 = c[1].strip()
                return json.dumps(self.file.delete(param1))
            else:
                return json.dumps(dict(status='ERROR', data='request tidak dikenali'))
        except Exception:
            return json.dumps(dict(status='ERROR', data='request tidak dikenali'))


if __name__=='__main__':
    #contoh pemakaian
    fp = FileProtocol()
    print(fp.proses_string("LIST"))
    print(fp.proses_string("GET pokijan.jpg"))
    print(fp.proses_string("UPLOAD pokijan1.jpg pokijan1_base64.txt"))
    print(fp.proses_string("DELETE pokijan1.jpg"))
