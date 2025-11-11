import os
from dotenv import load_dotenv
import time
from test_drive import Motor
import re
import openai
from gtts import gTTS
import os, tempfile
import speech_recognition as sr
import json

class chatGPT:
    load_dotenv()	
    openai.api_key =os.getenv("OPEN_API_KEY")

    def interpret_command(user_input):
        prompt = f"Interpret the following command for a robotic car and return a JSON array with 'action' and 'value': '{user_input}'. Actions can be 'move_forward', 'move_backward', 'turn_left', 'turn_right', or 'stop'. Value is the speed or angle with default speed 2000."
        
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ],
        )
        
        result_text = response.choices[0].message.content
        cleaned = re.sub(r'```json|```', '', result_text).strip()
        
        try:
            data = json.loads(cleaned)
            return data
        except json.JSONDecodeError:
            print("Failed to parse JSON response:", result_text)
            return {"action": "stop", "message": "Invalid command"}

    def speak(text):
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as fp:
            tts = gTTS(text=text, lang='en')
            tts.save(fp.name)
            os.system(f"mpg123 -q {fp.name}")

    def listen():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 Listening...")
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            print("❓ Sorry, I did not understand that.")
            return ""
        except sr.RequestError as e:
            print(f"❗ Could not request results; {e}")
            return ""

    







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
                time.sleep(1)
                car.stop()
            elif command['action'] == 'move_backward':
                car.direction(value * -1, value * -1, value * -1, value * -1)
                time.sleep(1)
                car.stop()
            elif command['action'] == 'turn_left':
                car.direction(-value, value ,-value, value)
                time.sleep(1)
                car.stop()
            elif command['action'] == 'turn_right':
                car.direction(value, -value, value, -value)
                time.sleep(1)
                car.stop()
            if command['action'] == 'stop':
                car.stop()
       
        print(data)
    except KeyboardInterrupt:
        print("Program stopped by User")
