from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from test_drive import Motor

app = FastAPI()
car = Motor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend can call API
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/motor/{action}")
def motor_control(action: str):
    if action == "forward":
        car.direction(3000, 3000, 3000, 3000)
    elif action == "backward":
        car.direction(-3000, -3000, -3000, -3000)
    elif action == "left":
        car.direction(-2000, 2000, -2000, 2000)
    elif action == "right":
        car.direction(2000, -2000, 2000, -2000)
    elif action == "stop":
        car.stop()
    return {"action": action}
