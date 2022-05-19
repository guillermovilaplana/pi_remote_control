import RPi.GPIO as gpio

import time

print('Starting')

servo_pin = 12

gpio.setmode(gpio.BCM)
gpio.setup(servo_pin, gpio.OUT)

pwm = gpio.PWM(servo_pin, 50)
#p.start(2.5)

dt = 1
dt2 = 0.3

x = 0.5/20
y = 2.5/20

def angle_to_percent(angle):
    start = 4
    end = 12.5
    ratio = (end-start)/180
    angle_as_percent = angle*ratio
    
    return start + angle_as_percent

angles = range(0, 180, 20)

pwm.start(angle_to_percent(0))

try:
    for a in angles:
        pwm.ChangeDutyCycle(angle_to_percent(a))
        time.sleep(1)
    time.sleep(10)

except KeyboardInterrupt:
    pwm.stop()
    gpio.cleanup()



# try:
#     while True:
#         p.ChangeDutyCycle(5)
#         time.sleep(dt2)
#         p.ChangeDutyCycle(0)
#         time.sleep(dt)
#         p.ChangeDutyCycle(7.5)
#         time.sleep(dt2)
#         p.ChangeDutyCycle(0)
#         time.sleep(dt)
#         p.ChangeDutyCycle(10)
#         time.sleep(dt2)
#         p.ChangeDutyCycle(0)
#         time.sleep(dt)
#         p.ChangeDutyCycle(12.5)
#         time.sleep(dt2)
#         p.ChangeDutyCycle(0)
#         time.sleep(dt)
#         p.ChangeDutyCycle(2.5)
#         time.sleep(dt2)
#         p.ChangeDutyCycle(0)
#         time.sleep(dt)
# except KeyboardInterrupt:
#     p.stop
#     gpio.cleanup()
#     
