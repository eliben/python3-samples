import socket
import sys
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 40404

message = [b'first message', b'second message']

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_HOST, SERVER_PORT))

for line in message:
    time.sleep(0.3)
    sock.send(line)
    data = sock.recv(1024)
    print('Client received:', repr(data))

time.sleep(2)
sock.close()



