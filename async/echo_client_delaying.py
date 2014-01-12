import socket
import sys
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 40404

message = [b'Hello network world', b'another message, mkay?']

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_HOST, SERVER_PORT))

for line in message:
    time.sleep(0.3)
    sock.send(line)
    data = sock.recv(1024)
    print('Client received:', repr(data))

time.sleep(4)
sock.close()                             # close socket to send eof to server


