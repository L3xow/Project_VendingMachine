import socket
from time import sleep


TCP_IP = '127.0.0.1'
TCP_PORT = 5005

BUFF = 50

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print ('Conn', addr)
while True:
    data = conn.recv(BUFF)
    print(data.decode('utf-8'))
    stringdata = data.decode('utf-8')
    print(stringdata)
    conn.send(data)

    if (data.decode('utf-8') == b'5'):
        print("Dog")
