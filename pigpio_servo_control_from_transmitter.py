import pigpio

import time

print('Starting')

transmitter_pin = 27  # ailerons
servo_pin = 12  # servo

pi1 = pigpio.pi()

pi1.set_mode(transmitter_pin, pigpio.INPUT)

pi2 = pigpio.pi()

pi2.set_mode(servo_pin, pigpio.OUTPUT)
pi2.set_PWM_frequency(servo_pin, 50)  # 20ms

pwm_range = 40000
pi2.set_PWM_range(servo_pin, pwm_range)

# For transmitter signal
min_ms = 1
max_ms = 2

# For servo control signal
min_percent = 2.5 / 100
max_percent = 12.5 / 100


def angle_to_percent(angle):
    return int((min_percent + angle / 180 * (max_percent - min_percent)) * pwm_range)


def ms_to_angle(ms):
    return (ms - min_ms) * 180 / (max_ms - min_ms)


t = 0


def set_rising_time(gpio_pin, level, tick):
    global t
    t = tick


def print_delta_time(gpio_pin, level, tick):
    global t
    if t == 0:
        print('Missed rising edge')
    else:
        pi1.set_PWM_dutycycle(servo_pin, angle_to_percent(ms_to_angle((tick - t) / 1000)))
        print(ms_to_angle((tick-t)/1000))
        t = 0


try:
    cb1 = pi1.callback(transmitter_pin, pigpio.RISING_EDGE, set_rising_time)
    cb2 = pi1.callback(transmitter_pin, pigpio.FALLING_EDGE, print_delta_time)

    time.sleep(60)

except KeyboardInterrupt:
    print('Keyboard Interrupt, cleaning up...')

finally:
    cb1.cancel()
    cb2.cancel()

    pi1.stop()
    pi2.stop()

    print('Finished')
