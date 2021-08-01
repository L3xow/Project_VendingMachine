"""
Dient lediglich zum Coden des Servers der auf dem RaspberryPi ausgeführt wird.
Wird nirgends im Mainprogramm aufgerufen oder verwendet.
"""

import socket
from time import *
#import mfrc522 as SimpleMFRC522


class server():
    """
    Stellt den Server Prozess als Thread dar. Verwaltet sämtliche TCP Angelegenheiten
    mit dem Raspberry Pi, um einen Scanbefehl zu erteilen und um den gescannten RFID
    Code zurückzugeben.

    :return:
    """
    def __init__(self):
#        self.reader = SimpleMFRC522()
        print("thread started..")
        self.ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 9999
        self.ls.bind(('', port))
        print("Server listening on port %s" % port)
        self.ls.listen(1)
        self.ls.settimeout(15)
        while True:
            if self.conn is None:
                try:
                    (self.conn, self.addr) = self.ls.accept()
                    print("client is at", self.addr[0], "on port", self.addr[1])

                except socket.timeout as e:
                    print("Waiting for Connection...")

                except Exception as e:
                    print("Connect exception: " + str(e))

            if self.conn != None:
                sleep(0.1)
                print("connected to " + str(self.conn) + "," + str(self.addr))
                self.conn.settimeout(15)
                self.rc = ""
                connect_start = time()  # actually, I use this for a timeout timer
                if self.rc != "done":
                    self.rc = ''
                    try:
                        self.rc = self.conn.recv(20).decode('utf-8')
                        if self.rc == "scan":
                            code, name = self.reader.read()
                            self.conn.send(b"code")
                    except Exception as e:
                        # we can wait on the line if desired
                        print("socket error: " + repr(e))

                    if len(self.rc):
                        print("got data", self.rc)
                        self.gotData = True
                        connect_start = time()  # reset timeout time
                    elif (self.running == 0) or (time() - connect_start > 30):
                        print("Tired of waiting on connection!")
                        self.rc = "done"

                print("closing connection")
                self.conn.close()
                self.conn = None
                print("connection closed.")

        # print("closing listener...")
        # # self running became 0
        # self.ls.close()