import os
import socket
import json
import base64
import logging

server_address=('0.0.0.0',7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        command_str += "\r\n\r\n"
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
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
        print("Gagal")
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
        print("Sukses")
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filename=""):
    if not os.path.exists(filename):
        print(f'File {filename} tidak ditemukan')
        return
    fp = open(filename,'rb')
    file_base64 = base64.b64encode(fp.read()).decode()
    command_str=f"UPLOAD {filename} {file_base64}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print(f'File {filename} berhasil diupload')
        return True
    else:
        print(f'File {filename} gagal diupload')
        return False  

def remote_delete(filename=""):
    command_str=f"DELETE {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print(f'File {filename} berhasil dihapus')
        return True
    else:
        print(f'File {filename} gagal dihapus')
        return False

if __name__=='__main__':
    server_address=('172.20.0.3',6666)
    while True:
        print("""
Welcome to Filey CLI:
1. LIST
2. GET [filename]
3. UPLOAD [filename]
4. DELETE [filename]
5. EXIT
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
