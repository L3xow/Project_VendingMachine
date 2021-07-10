import pigpio



pi = pigpio.pi("192.168.43.18", 8888)

test = pi.connected

if test:

    h = pi.file_open("/home/pi/Desktop/test.py", 2 | 8)
    pi.file_write(h, "Hello World")

