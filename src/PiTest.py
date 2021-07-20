import errno
import socket
import sys
from time import sleep


class client():

    def __init__(self):
        TCP_IP = 'localhost'
        TCP_PORT = 9999
        self.data = 0
        self.BUFF = 4

        self.s = socket.socket()
        self.s.connect((TCP_IP, TCP_PORT))
        self.s.setblocking(1)
        sleep(1)

    def get_data(self):
        try:
            self.data = self.s.recv(self.BUFF)
            sleep(2)
        except socket.error as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                sleep(1)
                print("No Data was available")
            else:
                print(e)
        return self.data.decode('utf-8')

    def send_data(self, data):
        self.s.send(data.encode())
        print("data sent")




if __name__ == "__main__":
    c = client()
    data = 0
    while True:
        sleep(2)
        print("connncetefdsf")
        while data == 0:
         data = c.get_data()
         print("asdf")
         c.send_data("rfidcode")
         data = 0



