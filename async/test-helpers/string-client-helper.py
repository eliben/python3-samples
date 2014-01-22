import socket
import sys
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 5566

messages = [b'\x05\x00\x00\x00abcde', b'\x03\x00\x00\x00345']

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_HOST, SERVER_PORT))

for line in messages:
    time.sleep(0.3)
    sock.send(line)
    data = sock.recv(1024)
    print('Client received:', repr(data))

time.sleep(1)
sock.close()



