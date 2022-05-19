import pigpio

import time

print('Starting')

transmitter_pin = 22  # 27 ailerons
esc_pin = 23  # 12 servo

pi1 = pigpio.pi()
pi1.set_mode(transmitter_pin, pigpio.INPUT)

pi2 = pigpio.pi()
pi2.set_mode(esc_pin, pigpio.OUTPUT)

pi2.set_PWM_frequency(esc_pin, 50)  # 20ms
pwm_range = 1  # 40000
# pi2.set_PWM_range(esc_pin, pwm_range)

# Transmitter signal
min_ms = 1.2 # 1.07
max_ms = 2

# ESC signal
# min_percent = 2.5 / 100
# max_percent = 12.5 / 100
min_percent = 1000
max_percent = 2000

# Calibrate ESC
print('Calibrating ESC ...')
# pi1.set_PWM_dutycycle(esc_pin, max_percent*pwm_range)
# time.sleep(2)
# pi1.set_PWM_dutycycle(esc_pin, min_percent*pwm_range)
# time.sleep(2)

pi1.set_servo_pulsewidth(esc_pin, 2000)  # Maximum throttle.
time.sleep(2)
pi2.set_servo_pulsewidth(esc_pin, 1000)  # Minimum throttle.
time.sleep(2)


def rpm_to_dutycycle(rpm):
    return int((min_percent + rpm / 10 * (max_percent - min_percent)) * pwm_range)


def ms_to_rpm(ms):
    return (ms - min_ms) * 10 / (max_ms - min_ms)


t = 0


def set_rising_time(gpio_pin, level, tick):
    global t
    t = tick


def set_output_dutycycle(gpio_pin, level, tick):
    global t
    if t == 0:
        print('Missed rising edge')
    else:
        # pi1.set_PWM_dutycycle(esc_pin, rpm_to_dutycycle(ms_to_rpm((tick - t) / 1000)))
        pi1.set_servo_pulsewidth(esc_pin, rpm_to_dutycycle(ms_to_rpm((tick - t) / 1000)))
        # print(rpm_to_dutycycle(ms_to_rpm((tick-t)/1000)))
        print((tick-t)/1000)
        t = 0


try:
    print('Starting callbacks ...')

    cb1 = pi1.callback(transmitter_pin, pigpio.RISING_EDGE, set_rising_time)
    cb2 = pi1.callback(transmitter_pin, pigpio.FALLING_EDGE, set_output_dutycycle)

    time.sleep(60)

    print('Time is up, cleaning up...')

except KeyboardInterrupt:
    print('Keyboard Interrupt, cleaning up...')

finally:
    # Stop ESC
    pi1.set_servo_pulsewidth(esc_pin, 0)

    cb1.cancel()
    cb2.cancel()

    pi1.stop()
    pi2.stop()

    print('Finished')
