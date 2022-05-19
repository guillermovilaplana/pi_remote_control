import time
import board
import busio
import adafruit_adxl34x

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

t = 0
zeroes = (0, 0, 0)

while True:
    a = [a-z for a, z in zip(accelerometer.acceleration, zeroes)]
    print(f'{a[0]:2f}   {a[1]:2f}   {a[2]:2f}')
    time.sleep(1)
    t += 1
    if t%5 == 0:
        zeroes = accelerometer.acceleration
        print(f'Zeroing with {zeroes} after {t}s.')

