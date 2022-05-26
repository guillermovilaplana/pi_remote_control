
# Streaming UDP
import socket
import time
from struct import pack

# Create a UDP socket
print(f'Creating UDP socket...')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host, port = '192.168.1.20', 65000
server_address = (host, port)

# Accel
import board
import busio
import adafruit_adxl34x

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

while True:
    values = (time.time(), *accelerometer.acceleration)
    print(values)
    message = pack('4d', *values)
    sock.sendto(message, server_address)
    time.sleep(1)
