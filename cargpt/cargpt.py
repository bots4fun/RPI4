import time
from drivegpt import chatGPT
from test_drive import Motor
import re

if __name__ == "__main__":
    try:
        interpret = chatGPT()
        car = Motor()
        user_input = chatGPT.listen()
        data = chatGPT.interpret_command(user_input)
        for command in data:
            value = int(command['value'])
            if command['action'] == 'move_forward':
                car.direction(value, value, value, value)
                time.sleep(2)
                car.stop()
            elif command['action'] == 'move_backward':
                car.direction(value * -1, value * -1, value * -1, value * -1)
                time.sleep(2)
                car.stop()
            elif command['action'] == 'turn_left':
                car.direction(-value, value, value, -value)
                time.sleep(1)
                car.stop()
            elif command['action'] == 'turn_right':
                car.direction(value, -value, -value, value)
                time.sleep(1)
                car.stop()
            elif command['action'] == 'stop':
                car.stop()

    except KeyboardInterrupt:
        print("Program stopped by User")