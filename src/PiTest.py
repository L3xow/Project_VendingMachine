import socket


class client:

    def __init__(self):
        TCP_IP = 'localhost'
        TCP_PORT = 5005
        self.data = 0
        self.BUFF = 50

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((TCP_IP, TCP_PORT))

    def get_data(self):
        self.data = self.s.recv(self.BUFF)
        print(self.data)
        return self.data

    def send_data(self, data):
        self.s.send(data)




if __name__ == "__main__":
    c = client()
    c.send_data(c.get_data())
    c.send_data(c.get_data())