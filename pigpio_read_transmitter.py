import pigpio

import time

print('Starting')

transmitter_pin = 22

pi1 = pigpio.pi()

pi1.set_mode(transmitter_pin, pigpio.INPUT)

t = 0


def set_rising_time(gpio_pin, level, tick):
    global t
    t = tick


def print_delta_time(gpio_pin, level, tick):
    global t
    if t == 0:
        print('Missed rising edge')
    else:
        print((tick-t)/1000)
        t = 0


cb1 = pi1.callback(transmitter_pin, pigpio.RISING_EDGE, set_rising_time)
cb2 = pi1.callback(transmitter_pin, pigpio.FALLING_EDGE, print_delta_time)

time.sleep(60)

cb1.cancel()
cb2.cancel()

pi1.stop()

print('Finished')

