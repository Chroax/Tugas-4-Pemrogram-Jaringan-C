import os
import socket
import json
import base64
import logging

server_address=('172.16.16.102',8889)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        command_str += "\r\n\r\n"
        sock.sendall(command_str.encode())
        data_received="" #empty string
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False


def remote_list():
    command_str=f"LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print('Gagal mendapatkan list file')
        return False

    
def remote_get(filename=""):
    command_str=f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        print(f'Berhasil mendapatkan file {filename}')
        return True
    else:
        print(f'Gagal mendapatkan file {filename}')
        return False

    
def remote_upload(filename=""):
    fp = open(filename,'rb')
    file_base64 = base64.b64encode(fp.read()).decode()
    command_str=f"UPLOAD {filename} {file_base64}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print(f'Berhasil mengupload file {filename}')
        return True
    else:
        print(f'Gagal mengupload file {filename}')
        return False  

def remote_delete(filename=""):
    command_str=f"DELETE {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print(f'Berhasil menghapus file {filename}')
        return True
    else:
        print(f'Gagal menghapus file {filename}')
        return False

if __name__=='__main__':
    while True:
        print("""
+++++++++++++++++++++++++++++++
File Management CLI:
1. LIST
2. GET [filename]
3. UPLOAD [filename]
4. DELETE [filename]
5. EXIT
+++++++++++++++++++++++++++++++
Please input your command:
""")
        command = input()
        cmd_req = command.split(" ")
        if command == 'list' or command == 'LIST':
            remote_list()
        elif command == 'exit' or command == 'EXIT':
            break
        elif cmd_req[0] == 'get' or cmd_req[0] == 'GET':
            remote_get(cmd_req[1])
        elif cmd_req[0] == 'upload' or cmd_req[0] == 'UPLOAD':
            remote_upload(cmd_req[1])
        elif cmd_req[0] == 'delete' or cmd_req[0] == 'DELETE':
            remote_delete(cmd_req[1])
