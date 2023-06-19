import os
import socket
import json
import base64
import logging
import time

server_address=('172.16.16.101',8889)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        data_received=""
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
        print("Gagal mendapatkan list file")
        return False

def remote_get(filename=""):
    command_str=f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        #proses file dalam bentuk base64 ke bentuk bytes
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print(f"Gagal mendapatkan file {filename}")
        return False
    
def remote_post(filename=""):
    fp = open(filename,'rb')
    isifile = base64.b64encode(fp.read()).decode('utf-8')
    fp.close()
    command_str=f"POST {filename} {isifile}\n"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print(f"Berhasil mengupload file {filename}")
        return True
    else:
        print(hasil)
        print(f"Gagal mengupload file {filename}")
        return False

def remote_delete(filename=""):
    command_str=f"DELETE {filename}\n"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):    
        print(f"Berhasil menghapus file {filename}")
        return True
    else:
        print(f"Gagal menghapus file {filename}")
        return False

def manage_input(command, cmd_req):
    if command.lower() == 'list':
        remote_list()
    elif cmd_req[0].lower() == 'get':
        remote_get(cmd_req[1])
    elif cmd_req[0].lower() == 'upload':
        remote_post(cmd_req[1])
    elif cmd_req[0].lower() == 'delete':
        remote_delete(cmd_req[1])

if __name__=='__main__':
    print("++++++++++++++++++++++++++++++++++++")
    print("FILE MANAGEMENT CLI:")
    print("1. LIST")
    print("2. GET [filename]")
    print("3. UPLOAD [filename]")
    print("4. DELETE [filename]")
    print("++++++++++++++++++++++++++++++++++++")
    print("Input your command: ")
    command = input()
    cmd_req = command.split(" ")
    manage_input(command, cmd_req)
    
    