
from __future__ import division
import time

import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()


# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096


# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000  # 1,000,000 us per second
    pulse_length //= 60  # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096  # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)


# Set frequency to 60hz
pwm.set_pwm_freq(60)

print('Moving servo on channel 0, press Ctrl-C to quit...')

half = 345
pwm.set_pwm(0, 0, half)
pwm.set_pwm(1, 0, half)
pos0 = half
pos1 = half

#While true, the program opens the file "move1.txt"
#if the bd1.py program detects there is something within 15cm of the ultrasonic sensor
#it will edit the move1.txt file and input the word "back"
while True:
    f = open('move1.txt', 'r')
    movement = f.read()
    f.close()
    if movement == 'back':#If the file contains "back" command, then the servo will move back slightly
        pos0 = pos0 + 10
        pwm.set_pwm(0, 0, pos0)
        f = open('move1.txt', 'w')
        f.write("")#And reset the file to be empty
        f.close()
    elif movement == 'half': #If the file is empty however, the program will make sure the servo is back at its default postion
        print('half')
        if pos0 < half:
            print('half1')
            while pos0 < half:
                pos0 = pos0 + 10
                pwm.set_pwm(0, 0, pos0)
                time.sleep(0.1)
        elif pos0 > half:
            print('half2')
            while pos0 > half:
                pos0 = pos0 - 1
                pwm.set_pwm(0, 0, pos0)
                time.sleep(0.1)
        f = open('move1.txt', 'w')
        f.write("")
        f.close()
    elif 'forward' in movement.lower(): #Forward is also a command, however this has to be manually added any wont occur
        movement = movement.split(' ')#automatically
        movement = movement[1]
        goal = int(pos0) + int(movement)
        while pos0 < goal:
            pos0 = pos0 - 1
            pwm.set_pwm(0, 0, pos0)
            time.sleep(0.01)
        f = open('move1.txt', 'w')
        f.write("")
        f.close()




