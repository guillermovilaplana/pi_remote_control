import board
import adafruit_fxos8700
import adafruit_fxas21002c
import time

i2c = board.I2C()
fxos = adafruit_fxos8700.FXOS8700(i2c)
fxas = adafruit_fxas21002c.FXAS21002C(i2c)

while True:
    print('Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*fxos.accelerometer))
    print('Magnetometer (uTesla): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*fxos.magnetometer))
    print('Gyroscope (radians/s): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(*fxas.gyroscope))
    time.sleep(1)