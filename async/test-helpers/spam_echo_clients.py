import socket
import sys
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 40404

sockets = []
msg = b'first message'

for i in range(20):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    sockets.append(sock)
    time.sleep(0.1)

for sock in sockets:
    sock.send(msg)
    time.sleep(0.1)

for sock in sockets:
    data = sock.recv(1024)
    if data != msg:
        print('Error! No reply to', sock.getsockname())
    time.sleep(0.1)

for sock in sockets:
    sock.close()
    time.sleep(0.1)

