import pigpio

import time

print('Starting')

transmitter_pin = 22  # 27 ailerons
esc_pins = range(23, 27)

pi1 = pigpio.pi()
pi1.set_mode(transmitter_pin, pigpio.INPUT)

pis = [pigpio.pi() for i in range(4)]
[pi.set_mode(esc_pin, pigpio.OUTPUT) for pi, esc_pin in zip(pis, esc_pins)]
[pi.set_PWM_frequency(esc_pin, 50) for pi, esc_pin in zip(pis, esc_pins)]  # 20ms

# Transmitter signal
min_ms = 1.2  # 1.07
max_ms = 2

# ESC signal
# min_percent = 2.5 / 100
# max_percent = 12.5 / 100
min_pulse_width = 1000
max_pulse_width = 2000

# # Calibrate ESC
print('Calibrating ESCs ...')
[pi.set_servo_pulsewidth(esc_pin, max_pulse_width) for pi, esc_pin in zip(pis, esc_pins)]  # Maximum throttle.
time.sleep(2)
[pi.set_servo_pulsewidth(esc_pin, min_pulse_width) for pi, esc_pin in zip(pis, esc_pins)]  # Minimum throttle.
time.sleep(2)


def rpm_to_dutycycle(rpm):
    return int(min_pulse_width + rpm / 10 * (max_pulse_width - min_pulse_width))

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
        [pi.set_servo_pulsewidth(esc_pin, rpm_to_dutycycle(ms_to_rpm((tick - t) / 1000))) for pi, esc_pin in zip(pis, esc_pins)]
        # print((tick-t)/1000)
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
    # Stop ESCs
    [pi.set_servo_pulsewidth(esc_pin, 0) for pi, esc_pin in zip(pis, esc_pins)]

    cb1.cancel()
    cb2.cancel()

    pi1.stop()
    [pi.stop() for pi in pis]

    print('Finished')
