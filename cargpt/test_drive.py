import time
#import board
import sys
import tty
import termios
from pca9685_driver import Device

class Motor:
    def __init__(self, address=0x40, busnum=1, freq=50):
        self.freq = freq
        self.pwm = Device(address, busnum)
        self.pwm.set_pwm_frequency(freq)
    

    def duty_cycle(self, duty1, duty2, duty3, duty4):
        if duty1 > 4095:
            duty1 = 4095
        if duty1 < -4095:
            duty1 = -4095
        if duty2 > 4095:
            duty2 = 4095
        if duty2 < -4095:
            duty2 = -4095
        if duty3 > 4095:
            duty3 = 4095
        if duty3 < -4095:
            duty3 = -4095
        if duty4 > 4095:
            duty4 = 4095
        if duty4 < -4095:   
            duty4 = -4095
        return duty1, duty2, duty3, duty4

    def FL(self, duty):
        if duty > 0:
            self.pwm.set_pwm(1, duty)
        if duty < 0:
            self.pwm.set_pwm(0, abs(duty))
        if duty == 0:
            self.pwm.set_pwm(0, 0)
            self.pwm.set_pwm(1, 0)

    def FR(self, duty):
        if duty > 0 :
            self.pwm.set_pwm(7, duty)
        if duty < 0:
            self.pwm.set_pwm(6, abs(duty))
        if duty == 0:
            self.pwm.set_pwm(6, 0)
            self.pwm.set_pwm(7, 0)
    
    def BL(self, duty):
        if duty >0 :
            self.pwm.set_pwm(2, duty)
        if duty < 0:
            self.pwm.set_pwm(3, abs(duty))
        if duty == 0:
            self.pwm.set_pwm(2, 0)
            self.pwm.set_pwm(3, 0)
    
    def BR(self, duty):
        if duty > 0:
            self.pwm.set_pwm(5, duty)
        if duty < 0:
            self.pwm.set_pwm(4, abs(duty))
        if duty == 0:
            self.pwm.set_pwm(4, 0)
            self.pwm.set_pwm(5, 0)

    def direction(self, duty1, duty2, duty3, duty4):
        duty1, duty2, duty3, duty4 = self.duty_cycle(duty1, duty2, duty3, duty4)
        self.FL(duty1)
        self.FR(duty2)
        self.BL(duty3)
        self.BR(duty4)

    def stop(self): 
        self.FL(0)
        self.FR(0)
        self.BL(0)
        self.BR(0)

    def keyboard_control(self, speed):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            
            while True:
                ch = sys.stdin.read(1)
                if ch == 'w':
                    print("forward")
                    self.direction(speed, speed, speed, speed)
                elif ch == 's':
                    print("backward")
                    self.direction(-speed, -speed, -speed, -speed)
                elif ch == 'a':
                    self.direction(-speed, speed, speed, -speed) 
                elif ch == 'd': 
                    self.direction(speed, -speed, -speed, speed)
                elif ch == 'q':
                    self.stop()
                
        except KeyboardInterrupt:
            print("Program stopped by User")
            
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

   
    


if __name__ == "__main__":
    try:
        car = Motor()
        car.keyboard_control(3000)  

    except KeyboardInterrupt:
            print("Program stopped by User")

    finally:
        car.stop()