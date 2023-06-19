import os
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self):
        try:
            filelist = glob('*.*')
            return dict(status='OK',data=filelist)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def get(self,filename):
        try:
            if (filename == ''):
                return None
            fp = open(f"{filename}",'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK',data_namafile=filename,data_file=isifile)
        except Exception as e:
            return dict(status='ERROR',data=str(e))
    def post(self,filename,file_base64):
        try:
            bfile = base64.b64decode(file_base64)
            fp = open(f"{filename}",'wb+')
            fp.write(bfile)
            fp.close()
            return dict(status='OK',data=f'file {filename} berhasil diupload')
        except Exception as e:
            return dict(status='ERROR',data=str(e))
    def delete(self,filename):
        try:
            if (filename == ''):
                return None
            if not os.path.exists(filename):
                return dict(status='ERROR',data=f'file {filename} tidak ditemukan')
            os.remove(f"{filename}")
            return dict(status='OK',data=f'file {filename} berhasil dihapus')
        except Exception as e:
            return dict(status='ERROR',data=str(e))

if __name__=='__main__':
    f = FileInterface()
    print(f.list())
    print(f.get('pokijan.jpg'))
    print(f.post('pokijan1.jpg','pokijan1_base64.txt'))
    print(f.delete('pokijan1.jpg'))
