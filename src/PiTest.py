import socket
from time import sleep


class client():

    def __init__(self):
        TCP_IP = socket.gethostname()
        TCP_PORT = 9999
        self.data = 0
        self.BUFF = 1000

        self.s = socket.socket()
        self.s.connect((TCP_IP, TCP_PORT))

    def get_data(self):
        self.data = self.s.recv(self.BUFF)
        print(self.data)
        print(self.data.decode('utf-8'))
        return self.data.decode('utf-8')

    def send_data(self, data):
        self.s.send(data.encode())
        print("data sent")




if __name__ == "__main__":
    c = client()
    data = 0
    while data == 0:
        print("asdf")
        data = c.get_data()
        sleep(10)
        #start rfid
        c.send_data("rfidcode")



