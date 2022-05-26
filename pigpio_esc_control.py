import pigpio

import time

print('Starting')

esc_pin = 26

pi2 = pigpio.pi()
pi2.set_mode(esc_pin, pigpio.OUTPUT)
pi2.set_PWM_frequency(esc_pin, 50)  # 20ms

# Calibrate ESC
print('Calibrating ESC ...')
pi2.set_servo_pulsewidth(esc_pin, 2000)  # Maximum throttle.
time.sleep(2)
pi2.set_servo_pulsewidth(esc_pin, 1000)  # Minimum throttle.
time.sleep(2)


try:
    print('Starting at min throttle 1075...')
    pi2.set_servo_pulsewidth(esc_pin, 1075)
    time.sleep(10)

    print('Time is up, cleaning up...')

except KeyboardInterrupt:
    print('Keyboard Interrupt, cleaning up...')

finally:
    # Stop ESC
    pi2.set_servo_pulsewidth(esc_pin, 0)
    pi2.stop()

    print('Finished')
