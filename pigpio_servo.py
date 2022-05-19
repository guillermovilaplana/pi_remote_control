import pigpio

import time

print('Starting')

servo_pin = 12

pi1 = pigpio.pi()

pi1.set_mode(servo_pin, pigpio.OUTPUT)
pi1.set_PWM_frequency(servo_pin, 50)

pwm_range = 40000
pi1.set_PWM_range(servo_pin, pwm_range)

min_percent = 2.5/100 #500
max_percent = 12.5/100 #2500


def angle_to_percent(angle):
    return int((min_percent + angle/180*(max_percent - min_percent))*pwm_range)


for a in range(1, 180, 1):
    pi1.set_PWM_dutycycle(servo_pin, angle_to_percent(a+1))
#     pi1.set_servo_pulsewidth(servo_pin, angle_to_percent(a))
    time.sleep(0.01)

pi1.stop()
